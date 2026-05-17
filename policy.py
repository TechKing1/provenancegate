from assembler import Chunk, Trust

class PolicyViolation(Exception):
    pass

RULES = {
    # RETRIEVED and TOOL chunks cannot contain instruction-like patterns
    # that attempt to override system behavior
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
    def __init__(self, strict: bool = True):
        self.strict = strict
        self.violations: list[str] = []

    def check(self, chunks: list[Chunk]) -> bool:
        self.violations = []

        for chunk in chunks:
            if chunk.trust in (Trust.RETRIEVED, Trust.TOOL, Trust.USER):
                for pattern in RULES["instruction_override_patterns"]:
                    if pattern.lower() in chunk.content.lower():
                        violation = (
                            f"Policy violation in [{chunk.trust.name}] chunk: "
                            f"detected pattern '{pattern}'"
                        )
                        self.violations.append(violation)
                        if self.strict:
                            raise PolicyViolation(violation)

        return len(self.violations) == 0

    def report(self) -> list[str]:
        return self.violations