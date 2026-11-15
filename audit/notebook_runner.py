import glob, json, os, time, traceback

import nbformat
from nbclient import NotebookClient

root = os.path.abspath(os.getcwd())
paths = sorted(p for p in glob.glob("**/*.ipynb", recursive=True)
               if ".ipynb_checkpoints" not in p and not p.startswith("templates"))

results = []
for i, path in enumerate(paths, 1):
    nb_path = os.path.join(root, path)
    started = time.time()
    entry = {"path": path.replace("\\", "/"), "status": "FAIL", "seconds": 0.0,
             "errors": [], "warnings": [], "imports": [], "network": []}
    try:
        nb = nbformat.read(nb_path, as_version=4)
        nbformat.validate(nb)
        code = [c for c in nb.cells if c.cell_type == "code"]
        entry["cells"] = len(nb.cells)
        entry["code_cells"] = len(code)
        imports = set()
        for c in code:
            for line in c.source.split("\n"):
                ls = line.strip()
                if ls.startswith(("import ", "from ")):
                    imports.add(ls.split()[1].split(".")[0])
        entry["imports"] = sorted(imports)
        entry["network"] = sorted(i for i in imports if i in {"requests", "urllib", "httpx", "socket", "wget"})
        nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
        client = NotebookClient(nb, timeout=300, kernel_name="python3",
                                resources={"metadata": {"path": os.path.dirname(nb_path)}})
        client.execute()
        errs = [o for c in code for o in c.outputs if o.output_type == "error"]
        entry["errors"] = [f"{e.ename}: {e.evalue}"[:200] for e in errs]
        stderr = [o.text.strip().split("\n")[0][:160] for c in code for o in c.outputs
                  if o.output_type == "stream" and o.name == "stderr" and o.text.strip()]
        entry["warnings"] = stderr[:5]
        entry["status"] = "FAIL" if errs else ("PASS WITH WARNINGS" if stderr else "PASS")
        try:
            nbformat.write(nb, nb_path)
            entry["note"] = "outputs refreshed"
        except Exception as exc:  # noqa: BLE001
            entry["note"] = f"write failed: {exc}"
    except Exception as exc:  # noqa: BLE001
        entry["status"] = "FAIL"
        entry["errors"] = [f"{type(exc).__name__}: {exc}"[:300]]
        entry["note"] = traceback.format_exc().splitlines()[-1][:200]
    entry["seconds"] = round(time.time() - started, 1)
    results.append(entry)
    print(f"[{i}/{len(paths)}] {entry['status']:20s} {entry['seconds']:7.1f}s {entry['path']}", flush=True)
    if entry["errors"]:
        print("     ", entry["errors"][0], flush=True)

with open("_nb_regression.json", "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=2)

counts = {}
for r in results:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
print("TOTAL", len(results), counts, round(sum(r["seconds"] for r in results), 1), "s", flush=True)
