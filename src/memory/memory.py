# Maximum number of recent messages to keep in memory
MAX_HISTORY = 10

# Stores conversation history during runtime
chat_history = []


# Adds a user or assistant message into memory
def add_to_history(role, message):
    # Prevent empty memory entries
    if not role or not message:
        return

    # Allow only valid roles
    if role not in ["user", "assistant"]:
        return

    chat_history.append({"role": role, "message": message})

    # Remove oldest message if memory exceeds limit
    if len(chat_history) > MAX_HISTORY:
        chat_history.pop(0)


# Returns the full conversation history
def get_history():
    return chat_history


# Clears the entire conversation memory
def clear_history():
    chat_history.clear()


# Converts conversation history into prompt-friendly text
def format_history():
    # Handle empty history safely
    if not chat_history:
        return ""

    formatted = ""

    for chat in chat_history:
        role = chat["role"]
        message = chat["message"]

        formatted += f"{role}: {message}\n"

    return formatted
