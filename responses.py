from random import choice

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == "":
        return "You didn't say anything!"
    elif "hello" in lowered:
        return "Hi there! How can I help?"
    else:
        return choice(["I don't understand that.", "Could you clarify?", "I'm not sure what you mean."])
