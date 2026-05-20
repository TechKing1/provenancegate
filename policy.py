"""policy.py

PolicyEngine implements simple, auditable rules intended to catch
straightforward prompt-injection attempts embedded in lower-trust inputs.

The engine is intentionally conservative: it uses precompiled regular
expressions to detect exact phrase patterns that indicate an attempt to
override or replace system-level instructions. This makes the behavior
deterministic and easy to review for academic/demo purposes.
"""

import re
from assembler import Chunk, Trust


class PolicyViolation(Exception):
    """Raised when a policy rule is violated and strict mode is enabled."""
    pass


RULES = {
    # RETRIEVED and TOOL chunks cannot contain instruction-like patterns
    # that attempt to override system behavior. This list represents
    # canonical phrases that are commonly-used in naive prompt-injection
    # examples. Keep the list small and auditable for explainability.
    "instruction_override_patterns": [
        "ignore previous instructions",
        "ignore all instructions",
        "disregard your system prompt",
        "you are now",
        "new instructions:",
        "system:",
        "assistant:",
    ]
}


class PolicyEngine:
    """PolicyEngine scans chunks for instruction-override patterns.

    Args:
        strict: If True, the engine raises a `PolicyViolation` on the first
            detected match (blocking mode). If False, violations are recorded
            but execution continues (audit mode).
    """
    def __init__(self, strict: bool = True):
        self.strict = strict
        self.violations: list[str] = []
        
        # Pre-compile the regex pattern for O(N) evaluation. We escape each
        # pattern to avoid accidental regex metacharacter interpretation, and
        # then join with alternation for a single scan over the text.
        escaped_patterns = [re.escape(p) for p in RULES["instruction_override_patterns"]]
        combined_pattern = "|".join(escaped_patterns)
        self._compiled_rule = re.compile(f"({combined_pattern})", re.IGNORECASE)

    def check(self, chunks: list[Chunk]) -> bool:
        """Scan provided chunks and enforce rules.

        Security logic:
        - We scan `USER`, `RETRIEVED`, and `TOOL` chunks because these are
          considered lower-trust sources that should not contain runtime
          instructions intended to override the system prompt.
        - Matches are deduplicated per-chunk and appended to `self.violations`.
        - In strict mode, the first match raises `PolicyViolation` to block
          the request immediately; in non-strict mode the violations are
          reported but processing may continue.

        Returns True if no violations were found, otherwise False.
        """
        self.violations = []

        for chunk in chunks:
            # We treat USER input as lower-trust for the purposes of these
            # instruction-override rules; some deployments may change this.
            if chunk.trust in (Trust.RETRIEVED, Trust.TOOL, Trust.USER):
                # Find all unique matches in the chunk content
                matches = set(m.group(1).lower() for m in self._compiled_rule.finditer(chunk.content))
                
                for match in matches:
                    violation = (
                        f"Policy violation in [{chunk.trust.name}] chunk: "
                        f"detected pattern '{match}'"
                    )
                    self.violations.append(violation)
                    if self.strict:
                        # Strict mode: block immediately and raise for the
                        # caller to handle (e.g., present a blocked message).
                        raise PolicyViolation(violation)

        return len(self.violations) == 0

    def report(self) -> list[str]:
        """Return the list of recorded violations (if any)."""
        return self.violations