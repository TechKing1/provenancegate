"""mock_llm.py — Drop-in mock for a real LLM client.

Produces deterministic, realistic-looking responses based on simple keyword
matching so ProvenanceGate demos run fully offline with no API key needed.

The mock is intentionally simple and deterministic so demo outputs are
reproducible; do not use this mock in production. To test with a real model,
swap `MockLLMClient` with the real `google.genai.Client` (see README).
"""

import re


class MockResponse:
    """Mimics the response object returned by google.genai.

    Only exposes a `.text` attribute which the demo code uses.
    """

    def __init__(self, text: str):
        self.text = text


class MockModels:
    """Container exposing a `generate_content` API similar to google.genai."""

    def generate_content(self, model: str, contents: str, **kwargs) -> MockResponse:
        # The mock ignores `model` and returns a deterministic response based
        # on simple pattern matching of the prompt contents.
        return MockResponse(_generate(contents))


class MockLLMClient:
    """Drop-in replacement for google.genai.Client used in demos.

    This thin wrapper provides a `.models.generate_content()` method so the
    rest of the codebase can stay identical whether a mock or real client is
    used.
    """

    def __init__(self, **kwargs):
        self.models = MockModels()


# ---------------------------------------------------------------------------
# Response generation logic
# ---------------------------------------------------------------------------

# A list of (pattern, response) tuples. The first matching pattern determines
# the returned response. Patterns are intentionally broad to produce useful
# demo outputs (factual answers, summaries, etc.).
_RESPONSES = [
    # Factual / geography
    (
        re.compile(r"capital of france", re.IGNORECASE),
        "The capital of France is **Paris**. It is located in north-central France "
        "along the Seine River and serves as the country's political, economic, and "
        "cultural centre.",
    ),
    # Financial summary
    (
        re.compile(r"q3|quarterly|revenue|earnings|financial", re.IGNORECASE),
        "**Q3 2025 Financial Summary**\n\n"
        "Revenue grew 12% year-over-year to $4.2 billion, driven primarily by cloud "
        "services and enterprise contract expansions. Operating margin improved to "
        "18.3%, reflecting disciplined cost management. The outlook for Q4 remains "
        "positive given continued momentum in both segments.",
    ),
    # Generic summarise
    (
        re.compile(r"summar", re.IGNORECASE),
        "Here is a concise summary of the document:\n\n"
        "The document covers operational updates and project milestones. Key points "
        "include system stability, ongoing deliverables, and next-quarter targets. "
        "No anomalies or escalations were flagged in this reporting period.",
    ),
    # Generic question
    (
        re.compile(r"what|how|why|when|where|who", re.IGNORECASE),
        "Based on the context provided, the answer is straightforward. "
        "The relevant information indicates the expected outcome aligns with "
        "standard enterprise guidelines. Please let me know if you need "
        "further clarification on any specific aspect.",
    ),
]

# A safe fallback response when no pattern matches. Keeps demo output clean.
_FALLBACK = (
    "I have processed your request using the available context. "
    "The information provided appears consistent with established guidelines. "
    "No issues were detected in the current interaction."
)


def _generate(prompt: str) -> str:
    """Return a deterministic response based on simple pattern matching."""
    for pattern, response in _RESPONSES:
        if pattern.search(prompt):
            return response
    return _FALLBACK
