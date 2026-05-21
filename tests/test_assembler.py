from assembler import ContextAssembler, Trust


def test_assembler_orders_and_labels():
    ca = ContextAssembler()
    ca.add("System instructions: be helpful.", Trust.SYSTEM)
    ca.add("This is retrieved doc.", Trust.RETRIEVED)
    ca.add("User question here.", Trust.USER)

    messages = ca.assemble()
    assert isinstance(messages, list)
    assert messages and messages[0]["role"] == "system"
    content = messages[0]["content"]
    # System content should appear verbatim first
    assert "System instructions: be helpful." in content
    # Retrieved and user chunks should be labeled with their trust tier
    assert "[RETRIEVED INPUT" in content
    assert "[USER INPUT" in content
