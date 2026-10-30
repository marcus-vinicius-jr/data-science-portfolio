"""WHO Malaria RAG Assistant - local Streamlit chat.

Runs the configuration recommended by the evaluation in notebooks/05_llm_rag_pdf_chatbot.ipynb:
OpenAI `text-embedding-3-small` retrieval (top 5 chunks) + `gpt-4.1-mini` with the grounding prompt.

Usage (from the repository root or from this folder):
    streamlit run 05_llm_rag_pdf_chatbot/app.py

The OpenAI API key is read only from a `.env` file (OPENAI_API_KEY=...) or the environment of the person running the app.
Every question is paid by that person's own key; the app is meant to run locally, not to be published with someone else's key.
"""
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"   # Chroma telemetry off

import re
import urllib.request
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv, find_dotenv
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

# --- Configuration (same values as the notebook) ------------------------------
PROJECT_DIR = Path(__file__).resolve().parent
DATA_RAW = PROJECT_DIR / "data" / "raw"
CHROMA_DIR = PROJECT_DIR / "data" / "processed" / "chroma"
COLLECTION = "openai_te3_small"

GEN_MODEL = "gpt-4.1-mini"
EMB_MODEL = "text-embedding-3-small"
GEN_K = 5
CHUNK_SIZE, CHUNK_OVERLAP = 1000, 150
PRICES = {"input": 0.40, "output": 1.60}   # gpt-4.1-mini, USD per 1M tokens (list price at the time of writing)

DOCS = {
    "who_guidelines_malaria": {
        "label": "WHO Guidelines for malaria",
        "url": "https://iris.who.int/server/api/core/bitstreams/d3c6488b-3ee6-41cb-960f-ddf0202cd74d/content",
    },
    "world_malaria_report_2025": {
        "label": "World malaria report 2025",
        "url": "https://iris.who.int/server/api/core/bitstreams/be20b8dc-cbfa-42a6-ad17-7679ceb75360/content",
    },
    "wmr_2025_executive_summary": {
        "label": "WMR 2025 executive summary",
        "url": ("https://cdn.who.int/media/docs/default-source/malaria/world-malaria-reports/"
                "world-malaria-report-2025-executive-summary-eng.pdf?sfvrsn=154ea8d5_26&download=true"),
    },
}

# Grounding prompt: identical to the notebook, so the app reproduces the evaluated behaviour
ABSTAIN_TEXT = "Not found in the provided documents."
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an assistant for the head of a national malaria control programme. "
     "Answer the question using ONLY the numbered context passages from WHO documents. "
     "Cite the source of every factual claim with the document label and page shown in the passage header, "
     "in the form [World malaria report 2025, p. 24] or [WHO Guidelines for malaria, p. 17]. "
     "Never cite passage numbers such as [1] or [2]. "
     f"If the passages do not contain the answer, reply exactly: '{ABSTAIN_TEXT}' "
     "Do not use outside knowledge. Be concise (at most 120 words)."),
    ("human", "Context passages:\n\n{context}\n\nQuestion: {question}"),
])

# Sidebar shortcuts; the last one has no answer in the documents, to show the abstention
EXAMPLE_QUESTIONS = [
    "How many malaria cases were estimated worldwide in 2024?",
    "How should adults and children with severe malaria be treated?",
    "What dosing schedule does WHO recommend for malaria vaccines in children?",
    "What does WHO recommend about mass ivermectin administration?",
]

# PDF extraction artefacts: chart labels extracted as glyph names, and the guidelines' repeated page footer
GLYPH_RE = re.compile(r"/[a-z]+\.tnum")
FOOTER_RE = re.compile(r"WHO guidelines for malaria - \d+ \w+ \d{4} - World Health Organization \(WHO\)\s*\d+ of \d+")


# --- Pipeline -------------------------------------------------------------------
def clean_text(text):
    """Remove extraction artefacts and collapse whitespace."""
    text = GLYPH_RE.sub("", text)
    text = FOOTER_RE.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_chunks():
    """Download the PDFs if needed and reproduce the notebook's cleaning and chunking (same chunk ids)."""
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    page_docs = []
    for doc_id, meta in DOCS.items():
        path = DATA_RAW / f"{doc_id}.pdf"
        if not path.exists():
            req = urllib.request.Request(meta["url"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=300) as r:
                path.write_bytes(r.read())
        for i, page in enumerate(PdfReader(path).pages, start=1):
            text = clean_text(page.extract_text() or "")
            if len(text) >= 50:
                page_docs.append(Document(page_content=text, metadata={"doc": doc_id, "page": i}))
    chunks = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP).split_documents(page_docs)
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = f"c{i:05d}"
    return chunks


# Cached: Streamlit reruns the script on every interaction, so the clients are created only once
@st.cache_resource
def open_vector_store():
    return Chroma(collection_name=COLLECTION, embedding_function=OpenAIEmbeddings(model=EMB_MODEL, max_retries=6),
                  persist_directory=str(CHROMA_DIR), collection_metadata={"hnsw:space": "cosine"})


@st.cache_resource
def get_llm():
    return ChatOpenAI(model=GEN_MODEL, temperature=0, seed=42, max_retries=6, timeout=120)


def build_index(vs):
    """Embed all chunks with OpenAI and store them in Chroma (billed to the user's key)."""
    chunks = build_chunks()
    for start in range(0, len(chunks), 256):
        batch = chunks[start:start + 256]
        vs.add_documents(batch, ids=[c.metadata["chunk_id"] for c in batch])
    return len(chunks)


def format_context(docs):
    """Number the passages and label each one with its document and page, as in the notebook."""
    return "\n\n".join(f"[{i}] ({DOCS[d.metadata['doc']]['label']}, p. {d.metadata['page']})\n{d.page_content}"
                       for i, d in enumerate(docs, start=1))


def answer_question(vs, llm, question):
    """Retrieve the top 5 chunks, generate a grounded answer and return it with its sources and token usage."""
    docs = vs.similarity_search(question, k=GEN_K)
    resp = llm.invoke(RAG_PROMPT.format_messages(context=format_context(docs), question=question))
    usage = resp.usage_metadata or {}
    sources = [{"label": DOCS[d.metadata["doc"]]["label"], "page": d.metadata["page"], "text": d.page_content}
               for d in docs]
    cost = (usage.get("input_tokens", 0) * PRICES["input"] + usage.get("output_tokens", 0) * PRICES["output"]) / 1e6
    return {"answer": resp.content, "sources": sources, "cost": cost}


def md_safe(text):
    """Escape '$' so Streamlit does not render amounts such as 'US$ 3.9 billion' as LaTeX."""
    return text.replace("$", r"\$")


# --- UI -------------------------------------------------------------------------
def render_answer(result):
    """Answer text plus an expandable list with the text of each retrieved passage."""
    st.markdown(md_safe(result["answer"]))
    with st.expander(f"Sources ({len(result['sources'])} retrieved passages)"):
        for i, s in enumerate(result["sources"], start=1):
            st.markdown(f"**[{i}] {s['label']}, p. {s['page']}**")
            st.caption(md_safe(s["text"][:700] + ("..." if len(s["text"]) > 700 else "")))


def main():
    st.set_page_config(page_title="WHO Malaria RAG Assistant", page_icon="🦟", layout="centered")
    load_dotenv(find_dotenv(usecwd=True))

    st.title("WHO Malaria RAG Assistant")
    st.caption("Answers only from the WHO guidelines for malaria and the World malaria report 2025, with the document and "
               "page cited. Ask in English. Each question is independent (no conversation memory). "
               "Always verify the cited pages before using an answer.")

    # 1. No key: explain how to set one up and stop (the app only ever uses the user's own key)
    if not os.getenv("OPENAI_API_KEY"):
        st.error("No OpenAI API key found.")
        st.markdown("Create a `.env` file at the repository root with your own key and restart the app:\n\n"
                    "```text\nOPENAI_API_KEY=sk-...\n```\n\n"
                    "Questions are billed to that key (about US\\$ 0.0006 per question).")
        st.stop()

    # 2. No index yet (e.g. right after cloning): offer to build it
    vs = open_vector_store()
    n_chunks = vs._collection.count()
    if n_chunks == 0:
        st.warning("The OpenAI index has not been built yet.")
        st.markdown("Building it downloads the three WHO PDFs and embeds 3,305 chunks with "
                    f"`{EMB_MODEL}`: about 1 minute and about US\\$ 0.01, billed to your key. "
                    "Running the notebook also builds it.")
        if st.button("Build the index"):
            with st.spinner("Downloading PDFs and embedding chunks..."):
                n_chunks = build_index(vs)
            st.success(f"Index built: {n_chunks} chunks.")
            st.rerun()
        st.stop()

    # 3. Session state survives reruns: chat history and running cost
    llm = get_llm()
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("session_cost", 0.0)

    # 4. Sidebar: configuration, session cost, example questions
    with st.sidebar:
        st.header("About")
        st.markdown(f"- **Retrieval:** `{EMB_MODEL}`, top {GEN_K} chunks\n"
                    f"- **Generation:** `{GEN_MODEL}`, temperature 0\n"
                    f"- **Index:** {n_chunks:,} chunks from 727 pages\n"
                    "- **Evaluation:** 92.3% fully correct, 0 incorrect, 6/6 abstentions on unanswerable questions "
                    "(see the notebook)")
        st.metric("Cost of this session (your key)", f"US$ {st.session_state.session_cost:.4f}")
        if st.button("Clear conversation"):
            st.session_state.messages = []
            st.rerun()
        st.header("Try an example")
        for q in EXAMPLE_QUESTIONS:
            if st.button(q, use_container_width=True):
                st.session_state.pending_question = q

    # 5. Redraw the conversation so far
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(md_safe(msg["content"]))
            else:
                render_answer(msg["content"])

    # 6. New question, typed in the chat box or clicked in the sidebar
    question = st.chat_input("Ask a question about the WHO malaria documents")
    question = question or st.session_state.pop("pending_question", None)
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(md_safe(question))
        with st.chat_message("assistant"):
            with st.spinner("Searching the documents..."):
                result = answer_question(vs, llm, question)
            render_answer(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
        st.session_state.session_cost += result["cost"]
        st.rerun()


if __name__ == "__main__":
    main()
