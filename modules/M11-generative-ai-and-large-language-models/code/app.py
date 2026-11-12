"""app.py -- a Streamlit demo of the retrieval-augmented assistant (M11, LAB-11-02 / MP-11).

Two ways to run it:

    streamlit run app.py                 # browser UI on http://localhost:8501
    python app.py "What is the deposit?"  # one question in the terminal

Everything runs locally: MiniLM embeds the corpus, flan-t5-small writes the
answer. No API key, no network call after the models are cached, and no data
leaves the machine.

The UI deliberately shows the retrieved context and the grounding score next to
the answer. A RAG demo that hides its sources teaches the wrong lesson.
"""

from __future__ import annotations

import sys


def answer_once(question: str) -> None:
    from rag import RAGSystem

    system = RAGSystem()
    out = system.answer(question)
    print(f"question : {out['question']}")
    print(f"answer   : {out['answer']}")
    print(f"sources  : {out['docs']}")
    print(f"support  : {out['support']:.2f}   refused: {out['refused']}   "
          f"latency: {out['seconds']:.2f}s")
    print(f"context  : {out['context'][:300]}...")


def run_ui() -> None:
    import streamlit as st

    from rag import RAGSystem

    st.set_page_config(page_title="Northfield handbook assistant", page_icon="book")
    st.title("Northfield handbook assistant")
    st.caption("Retrieval-augmented generation, fully local. Answers come only from the "
               "24 handbook documents in `corpus/`.")

    @st.cache_resource(show_spinner="Building the index...")
    def get_system():
        return RAGSystem()

    system = get_system()
    question = st.text_input("Your question",
                             value="How much is the accommodation deposit?")
    k = st.slider("Chunks retrieved", 1, 5, 3)

    if st.button("Ask") and question.strip():
        out = system.answer(question, k=k)
        st.subheader("Answer")
        if out["refused"]:
            st.warning(out["answer"])
        else:
            st.success(out["answer"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Grounding score", f"{out['support']:.2f}")
        c2.metric("Latency", f"{out['seconds']:.2f} s")
        c3.metric("Sources", len(out["docs"]))

        st.subheader("Retrieved context")
        st.text(out["context"])
        st.caption("Sources: " + ", ".join(out["docs"]))
        st.info("Every answer above is generated from this context only. If the context "
                "does not contain the answer, the correct behaviour is to say so - the "
                "grounding score is a warning sign, not a guarantee.")

    with st.expander("How this works"):
        st.markdown(
            "1. The question is embedded with `all-MiniLM-L6-v2` (384 dimensions).\n"
            "2. Dense scores are fused with BM25 scores and the top candidates are "
            "reranked by late interaction.\n"
            "3. The best chunks are packed into a context of at most 1,200 characters.\n"
            "4. `flan-t5-small` answers with greedy decoding, instructed to refuse "
            "when the context is insufficient.\n"
            "5. The grounding score is the share of answer content words found in the "
            "context.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        answer_once(" ".join(sys.argv[1:]))
    else:
        try:
            run_ui()
        except ImportError:
            print("Streamlit is not installed. Run: pip install streamlit")
            print("Or use the command line: python app.py \"your question\"")
