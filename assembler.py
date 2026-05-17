from enum import IntEnum

class Trust(IntEnum):
    SYSTEM = 0      # highest trust
    USER = 1
    RETRIEVED = 2
    TOOL = 3        # lowest trust

class Chunk:
    def __init__(self, content: str, trust: Trust):
        self.content = content
        self.trust = trust

    def __repr__(self):
        return f"[{self.trust.name}] {self.content[:60]}"

class ContextAssembler:
    def __init__(self):
        self.chunks: list[Chunk] = []

    def add(self, content: str, trust: Trust):
        self.chunks.append(Chunk(content, trust))

    def assemble(self) -> list[dict]:
        """
        Assembles chunks into a message list for the LLM API,
        sorted by trust level (highest trust first).
        Each chunk is labeled with its trust tier in the prompt.
        """
        sorted_chunks = sorted(self.chunks, key=lambda c: c.trust.value)
        messages = []

        system_parts = []
        for chunk in sorted_chunks:
            if chunk.trust == Trust.SYSTEM:
                system_parts.append(chunk.content)
            else:
                label = f"[{chunk.trust.name} INPUT — trust level {chunk.trust.value}]"
                system_parts.append(f"{label}\n{chunk.content}")

        messages.append({
            "role": "system",
            "content": "\n\n".join(system_parts)
        })

        return messages