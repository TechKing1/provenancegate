"""
mock_llm.py — Drop-in mock for a real LLM client.

Produces deterministic, realistic-looking responses based on simple keyword
matching so ProvenanceGate demos run fully offline with no API key needed.
"""

import re


class MockResponse:
    """Mimics the response object returned by google.genai."""
    def __init__(self, text: str):
        self.text = text


class MockModels:
    def generate_content(self, model: str, contents: str, **kwargs) -> MockResponse:
        return MockResponse(_generate(contents))


class MockLLMClient:
    """Drop-in replacement for google.genai.Client."""
    def __init__(self, **kwargs):
        self.models = MockModels()


# ---------------------------------------------------------------------------
# Response generation logic
# ---------------------------------------------------------------------------

_RESPONSES = [
    # Factual / geography
    (r"capital of france",
     "The capital of France is **Paris**. It is located in north-central France "
     "along the Seine River and serves as the country's political, economic, and "
     "cultural centre."),

    # Financial summary
    (r"q3|quarterly|revenue|earnings|financial",
     "**Q3 2025 Financial Summary**\n\n"
     "Revenue grew 12% year-over-year to $4.2 billion, driven primarily by cloud "
     "services and enterprise contract expansions. Operating margin improved to "
     "18.3%, reflecting disciplined cost management. The outlook for Q4 remains "
     "positive given continued momentum in both segments."),

    # Generic summarise
    (r"summar",
     "Here is a concise summary of the document:\n\n"
     "The document covers operational updates and project milestones. Key points "
     "include system stability, ongoing deliverables, and next-quarter targets. "
     "No anomalies or escalations were flagged in this reporting period."),

    # Generic question
    (r"what|how|why|when|where|who",
     "Based on the context provided, the answer is straightforward. "
     "The relevant information indicates the expected outcome aligns with "
     "standard enterprise guidelines. Please let me know if you need "
     "further clarification on any specific aspect."),
]

_FALLBACK = (
    "I have processed your request using the available context. "
    "The information provided appears consistent with established guidelines. "
    "No issues were detected in the current interaction."
)


def _generate(prompt: str) -> str:
    lowered = prompt.lower()
    for pattern, response in _RESPONSES:
        if re.search(pattern, lowered):
            return response
    return _FALLBACK
