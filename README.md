# ProvenanceGate - Practical Research Project

ProvenanceGate is a small educational/demo project that demonstrates a
lightweight defense against straightforward prompt-injection attacks in
Retrieval-Augmented Generation (RAG) pipelines. The project is intentionally
minimal and uses a deterministic mock LLM so the demos run fully offline.

## Requirements
- Python 3.10 or later (3.13 recommended if available).
- The Python packages listed in `requirements.txt` (see below).
- Optional: `fpdf` if you want to generate the PDF report with
	`generate_submission.py`.

The repository includes a minimal `requirements.txt`:

```
google-genai>=2.0.0
python-dotenv>=1.0.0
```

Note: The demo uses the bundled `MockLLMClient` by default so you do not
need a real API key to run the provided examples. If you intend to test
against a real model, add the appropriate SDK to `requirements.txt` and set
the required environment variables as described below.

## Installation
Create and activate a virtual environment, then install dependencies:

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Windows (CMD):
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Optional (to generate the PDF report):
```powershell
pip install fpdf
```

## Environment
If you replace the mock client with a real LLM client, store credentials
in a `.env` file at the project root (the repo loads `.env` using
`python-dotenv`). For example:

```
GEMINI_API_KEY=your_api_key_here
```

`main.py` currently uses `MockLLMClient`. To use a real client, replace the
client initialization in `main.py`:

```py
# Replace this line:
client = MockLLMClient()

# With the real client, for example (pseudo-code):
import google.genai as genai
client = genai.Client()
```

Refer to your chosen provider's SDK docs for the exact initialization steps.

## Running the Demos
The project includes two small demos.

- Main pipeline demo (demonstrates `run()` with clean and injection cases):
```powershell
python main.py
```

- RAG demo (compares naive concatenation vs ProvenanceGate):
```powershell
python rag_demo.py
```

Outputs are printed to stdout. To capture a short log file (Windows examples):

CMD redirection (quick):
```cmd
mkdir logs
python rag_demo.py > logs\rag_demo.log 2>&1
```

PowerShell transcript (captures everything):
```powershell
Start-Transcript -Path .\logs\rag_demo.log
python .\rag_demo.py
Stop-Transcript
```

Programmatic logging (inside Python):
See the example in the project notes — you can also call `run()` from a
small wrapper that writes the returned string to a file.

## What the demos show
- `rag_demo.py` shows how naive concatenation of system prompt + retrieved
	document can be exploited by embedding instruction-like phrases in the
	retrieved text.
- The ProvenanceGate pipeline tags inputs with explicit `Trust` tiers and
	runs `PolicyEngine.check()` before contacting the LLM. In strict mode the
	engine blocks requests containing canonical override phrases.

## Files of interest
- `assembler.py` — ContextAssembler and `Trust` tiers (labels and ordering).
- `policy.py` — PolicyEngine: regex-based detection of instruction overrides.
- `mock_llm.py` — Deterministic mock LLM used for offline demos.
- `main.py` — `run()` entry point that assembles context, enforces policy,
	and calls the LLM client.
- `rag_demo.py` — Convenience demo comparing naive vs protected RAG.
- `generate_submission.py` — Simple PDF and zip helper (optional).

## Capturing a short log for submission
Run a demo and redirect stdout/stderr to a log as shown above, then open
the resulting `logs\*.log` file and copy the first 20–50 lines into your
submission as the "short log file".

## Notes and next steps
- The project's pattern-based policy is intentionally conservative and
	explainable, but it can be bypassed by paraphrased or semantically
	crafted injections. For production use consider adding an LLM-based intent
	classifier or provenance scoring on retrieved documents.

If you want, I can also:
- Add `fpdf` to `requirements.txt` so `generate_submission.py` works out of
	the box.
- Run the demos and capture short logs in `logs/` for you.

## Development & Testing

Use the included `requirements-dev.txt` to install developer tools for
testing and linting.

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Windows (CMD):
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

Run tests with `pytest`:
```powershell
python -m pytest -q
```

Run linting with `ruff`:
```powershell
ruff check .
```

Quick combined check:
```powershell
python -m pytest -q && ruff .
```

The `requirements-dev.txt` includes `pytest` and `ruff` for lightweight
developer workflows.
