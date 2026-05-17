# ProvenanceGate - Practical Research Project

## External Dependencies / Libraries Required
This project requires Python 3.10+.
The required external dependencies are specified in `requirements.txt`:
- `google-genai>=2.0.0`
- `python-dotenv>=1.0.0`

## Installation
Run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Code
The project uses a mocked LLM client, meaning no API key is required to run the demo. It runs entirely offline.

To run the main execution pipeline demo, which shows clean interactions and injection attempts:
```bash
python main.py
```

To run the Retrieval-Augmented Generation (RAG) demo, which compares naive RAG against ProvenanceGate-protected RAG:
```bash
python rag_demo.py
```
