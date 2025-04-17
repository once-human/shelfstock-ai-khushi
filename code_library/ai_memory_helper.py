from typing import List, Dict

"""
ai_memory_helper.py

👋 About this file:
This module helps you manage AI "memory"—a list of messages that tracks the full conversation between
the user and the assistant. This is important because OpenAI's chat models use the entire message history
to decide what to say next.

You can think of memory as the "chat log" or "context" that the AI reads before responding.

✨ What you can do with this file:
- Start a new memory with a custom system prompt and optional personality/context
- Add new messages as the conversation continues
- Access or print the full message history for debugging or reuse

📚 Example use case:
You’re building a voice assistant that remembers your tone, personality, and previous messages. 
This helper keeps everything organized so the assistant responds the way you expect.
"""

def init_message_history(
    system_prompt: str,
    additional_context: List[Dict[str, str]] = []
) -> List[Dict[str, str]]:
    """
    Initializes message history (a.k.a. memory) with a system prompt and optional extra context.

    Args:
        system_prompt: A message that tells the AI what kind of assistant it is.
        additional_context: Optional list of system/user messages to set personality, user info, or examples.

    Returns:
        A list of message dictionaries, representing the beginning of the conversation memory.

    Example:
        >>> init_message_history(
                "You are a friendly assistant who speaks like a poet.",
                [{"role": "system", "content": "The user enjoys creative writing."}]
            )
    """
    print("[init_message_history] Initializing memory...")

    memory = [{"role": "system", "content": system_prompt}]
    memory.extend(additional_context)

    print(f"[init_message_history] Memory initialized with {len(memory)} messages.")
    return memory


def append_to_memory(
    memory: List[Dict[str, str]],
    role: str,
    content: str
) -> None:
    """
    Adds a new message to memory.

    Args:
        memory: The current list of messages (conversation history).
        role: The role of the message ("user", "assistant", or "system").
        content: The actual message text.

    Returns:
        None (modifies memory in-place)

    Example:
        >>> append_to_memory(memory, "user", "Can you summarize that?")
    """
    print(f"[append_to_memory] Adding a message from '{role}' to memory.")
    memory.append({"role": role, "content": content})


def get_memory(
    memory: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """
    Returns the current memory.

    Args:
        memory: The message history.

    Returns:
        The full message history as a list of dictionaries.

    Example:
        >>> current = get_memory(memory)
        >>> print(current[-1]["content"])
    """
    print(f"[get_memory] Memory has {len(memory)} messages.")
    return memory