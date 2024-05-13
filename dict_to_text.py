def dict_to_text(dictionary, indent=0):
    text = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            text += "  " * indent + f"{key}:\n"
            text += dict_to_text(value, indent + 1)
        elif isinstance(value, list):
            text += "  " * indent + f"{key}:\n"
            for item in value:
                if isinstance(item, dict):
                    text += dict_to_text(item, indent + 1)
                else:
                    text += "  " * (indent + 1) + f"- {item}\n"
        else:
            text += "  " * indent + f"{key}: {value}\n"
    return text


