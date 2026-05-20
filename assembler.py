"""assembler.py

Provides a minimal context assembler used by ProvenanceGate. The assembler
collects labeled pieces of text (chunks) that include an explicit `Trust`
tier. The primary security policy here is ordering and provenance: higher
trust content (e.g. `SYSTEM`) is placed before lower-trust content so that
the prompt sent to an LLM clearly separates authoritative system instructions
from retrieved or tool-generated text.

The assembler formats all collected chunks into a single system-style message
that can be passed to an LLM client. This design makes it easy to audit the
prompt and reduces the risk that an LLM will treat retrieved content as
runtime instructions intended to override system-level directives.
"""

from enum import IntEnum


class Trust(IntEnum):
    """Ordered trust tiers used to tag context chunks.

    Lower numeric value == higher trust. The assembler sorts by this value so
    system prompts are presented first in the assembled message.
    """
    SYSTEM = 0      # highest trust
    USER = 1
    RETRIEVED = 2
    TOOL = 3        # lowest trust


class Chunk:
    """Small container holding a piece of text with an associated trust tag.

    Attributes:
        content: The raw text of the chunk.
        trust: A `Trust` enum indicating provenance/authority.
    """
    def __init__(self, content: str, trust: Trust):
        self.content = content
        self.trust = trust

    def __repr__(self):
        # Keep representation compact for logs while exposing trust tier
        return f"[{self.trust.name}] {self.content[:60]}"


class ContextAssembler:
    """Collects `Chunk` instances and assembles them into LLM messages.

    Security notes:
    - Chunks are sorted by `Trust` value so SYSTEM content always precedes
      lower-trust inputs.
    - Non-system chunks are labeled in the assembled system message so the
      LLM receives explicit provenance markers (e.g., `[RETRIEVED INPUT]`).
    """
    def __init__(self):
        self.chunks: list[Chunk] = []

    def add(self, content: str, trust: Trust):
        """Add a chunk of text with its trust level.

        This method intentionally accepts raw strings only; callers should
        perform any sanitization or normalization before calling `add()` if
        required by their application.
        """
        self.chunks.append(Chunk(content, trust))

    def assemble(self) -> list[dict]:
        """Return a list of messages suitable for an LLM API.

        The assembler returns a single `system`-role message that contains the
        concatenated system prompt followed by labeled lower-trust inputs.
        Keeping everything in one system message makes it easier to enforce
        ordering and to audit the final prompt that will be sent to an LLM.
        """
        # Sort by trust to ensure higher-trust content appears first
        sorted_chunks = sorted(self.chunks, key=lambda c: c.trust.value)
        messages = []

        system_parts = []
        for chunk in sorted_chunks:
            if chunk.trust == Trust.SYSTEM:
                # System-level instructions are included verbatim
                system_parts.append(chunk.content)
            else:
                # Label lower-trust inputs so the LLM sees provenance metadata
                label = f"[{chunk.trust.name} INPUT — trust level {chunk.trust.value}]"
                system_parts.append(f"{label}\n{chunk.content}")

        messages.append({
            "role": "system",
            "content": "\n\n".join(system_parts)
        })

        return messages