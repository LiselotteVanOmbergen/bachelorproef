def dict_to_text(dictionary, indent=0):
    text = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            text += "  " * indent + f"{key.capitalize()}:\n"
            text += dict_to_text(value, indent + 1)
        elif isinstance(value, list):
            text += "  " * indent + f"{key.capitalize()}**:\n"
            for item in value:
                if isinstance(item, dict):
                    text += dict_to_text(item, indent + 1)
                else:
                    text += "  " * (indent + 1) + f"- {item}\n"
        else:
            # Check if the value is a string and contains newline characters
            if isinstance(value, str) and "\n" in value:
                # If yes, split the value by newline and add each part separately
                parts = value.split("\n")
                for part in parts:
                    text += "  " * indent + f"{key.capitalize()}: {part}\n"
            else:
                # If no newline characters or if the value is not a string, add the value normally
                text += "  " * indent + f"{key.capitalize()}: {value}\n"
    return text
