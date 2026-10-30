"""Free, key-less checks run by CI on every push (no OpenAI calls, no cost).

The full evaluation (re-running the notebook with the OpenAI API) is a separate, manually triggered CI job.
Run locally with:  pytest 05_llm_rag_pdf_chatbot/tests
"""
import ast
import csv
import json
from pathlib import Path

import pytest

PROJECT = Path(__file__).resolve().parents[1]
NOTEBOOK = PROJECT / "notebooks" / "05_llm_rag_pdf_chatbot.ipynb"
EVAL_CSV = PROJECT / "eval" / "eval_questions.csv"
APP = PROJECT / "app.py"


# --- Evaluation set -------------------------------------------------------------
def load_eval():
    with open(EVAL_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_eval_set_structure():
    rows = load_eval()
    assert set(rows[0]) == {"qid", "category", "question", "reference_answer", "evidence", "key_terms"}
    assert len(rows) == 45
    assert len({r["qid"] for r in rows}) == 45, "question ids must be unique"
    counts = {c: sum(r["category"] == c for r in rows) for c in {r["category"] for r in rows}}
    assert counts == {"guideline_recommendation": 19, "report_statistic": 20, "unanswerable": 6}


def test_eval_set_labels_are_consistent():
    for r in load_eval():
        if r["category"] == "unanswerable":
            assert not r["evidence"] and not r["key_terms"], r["qid"]
        else:
            assert r["evidence"].strip() and r["key_terms"].strip() and r["reference_answer"].strip(), r["qid"]


# --- Notebook -------------------------------------------------------------------
def test_notebook_executed_cleanly():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    assert code_cells and all(c.get("execution_count") for c in code_cells), "notebook must be fully executed"
    errors = [o for c in code_cells for o in c.get("outputs", []) if o.get("output_type") == "error"]
    assert not errors, "notebook contains error outputs"
    assert not any("RESULTS PLACEHOLDER" in "".join(c["source"]) for c in nb["cells"])


def test_no_api_key_in_versioned_files():
    for path in [NOTEBOOK, EVAL_CSV, APP, PROJECT / "README.md", PROJECT / "README_pt-BR.md"]:
        text = path.read_text(encoding="utf-8")
        assert "sk-proj-" not in text, f"possible API key in {path.name}"


# --- Chat app -------------------------------------------------------------------
def test_app_is_valid_python():
    ast.parse(APP.read_text(encoding="utf-8"))


def test_app_without_key_shows_setup_message(tmp_path, monkeypatch):
    """Without OPENAI_API_KEY the app must explain how to configure it and stop, never call the API."""
    from streamlit.testing.v1 import AppTest

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)                      # no .env reachable from here
    at = AppTest.from_file(str(APP), default_timeout=60).run()
    assert not at.exception
    assert [e.value for e in at.error] == ["No OpenAI API key found."]
    assert len(at.chat_input) == 0, "chat must not start without a key"
