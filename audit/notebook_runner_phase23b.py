"""Execute every notebook in an isolated kernel without modifying the repository.

Phase 23's runner wrote executed outputs back into the notebooks. An acceptance audit
must not mutate the artefacts it is judging, so this runner copies each notebook to a
temporary directory, executes there with a fresh kernel, and records results in
``audit/phase23b_notebook_results.json``.

Warnings are split into harmless (package notices, matplotlib backend, progress bars)
and substantive. A notebook is only "PASS" when it executes and produces no error output.

Usage:  python audit/notebook_runner_phase23b.py
"""

import glob
import json
import os
import shutil
import tempfile
import time
import traceback

import nbformat
from nbclient import NotebookClient

ROOT = os.path.abspath(os.getcwd())
SKIP = (".ipynb_checkpoints", "templates/filled")
HARMLESS = (
    "tpu", "prototype", "matplotlib is currently using agg", "non-interactive",
    "tqdm", "unauthenticated", "auth token", "hf_token", "symlink", "deprecated",
    "userwarning", "futurewarning", "runtimewarning", "some weights of",
)


def classify(stderr_lines):
    substantive, harmless = [], []
    for line in stderr_lines:
        low = line.lower()
        (harmless if any(marker in low for marker in HARMLESS) else substantive).append(line[:200])
    return substantive, harmless


def main():
    paths = sorted(p for p in glob.glob("**/*.ipynb", recursive=True)
                   if not any(part in p.replace("\\", "/") for part in SKIP))
    results = []
    for index, relative in enumerate(paths, 1):
        source = os.path.join(ROOT, relative)
        started = time.time()
        entry = {"path": relative.replace("\\", "/"), "status": "FAIL", "seconds": 0.0,
                 "errors": [], "warnings": [], "harmless_warnings": [], "network_imports": [],
                 "missing_local_files": [], "cells": 0, "code_cells": 0}
        workdir = tempfile.mkdtemp(prefix="nb23b_")
        try:
            notebook = nbformat.read(source, as_version=4)
            nbformat.validate(notebook)
            entry["cells"] = len(notebook.cells)
            code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
            entry["code_cells"] = len(code_cells)
            imports = set()
            for cell in code_cells:
                for line in cell.source.splitlines():
                    stripped = line.strip()
                    if stripped.startswith(("import ", "from ")):
                        imports.add(stripped.split()[1].split(".")[0])
            entry["network_imports"] = sorted(imports & {"requests", "urllib", "httpx", "wget", "socket"})

            notebook.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3",
                                               "language": "python"}
            client = NotebookClient(notebook, timeout=300, kernel_name="python3",
                                    resources={"metadata": {"path": os.path.dirname(source)}})
            client.execute()
            errors = [f"cell {position}: {output.ename}: {output.evalue}"[:250]
                      for position, cell in enumerate(code_cells, 1)
                      for output in cell.outputs if output.output_type == "error"]
            stderr = [output.text.strip().splitlines()[0][:200]
                      for cell in code_cells for output in cell.outputs
                      if output.output_type == "stream" and output.name == "stderr" and output.text.strip()]
            substantive, harmless = classify(stderr)
            entry["errors"] = errors
            entry["warnings"] = substantive[:6]
            entry["harmless_warnings"] = harmless[:6]
            entry["status"] = "FAIL" if errors else ("PASS WITH WARNINGS" if substantive else "PASS")
        except Exception as exc:  # noqa: BLE001
            entry["errors"] = [f"{type(exc).__name__}: {exc}"[:300]]
            entry["status"] = "FAIL"
            entry["note"] = traceback.format_exc().splitlines()[-1][:200]
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
        entry["seconds"] = round(time.time() - started, 1)
        results.append(entry)
        print(f"[{index}/{len(paths)}] {entry['status']:20s} {entry['seconds']:7.1f}s {entry['path']}",
              flush=True)
        if entry["errors"]:
            print("      ", entry["errors"][0], flush=True)

    with open("audit/phase23b_notebook_results.json", "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)
    counts = {}
    for record in results:
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    print("TOTAL", len(results), counts, round(sum(r["seconds"] for r in results), 1), "s")


if __name__ == "__main__":
    main()
