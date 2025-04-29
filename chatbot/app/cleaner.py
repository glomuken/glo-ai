import re

def remove_chat_metadata(chat_data):
    date_time = r"(\d+\/\d+\/\d+,\s\d+:\d+)"  # e.g., "9/16/22, 06:34"
    dash_whitespace = r"\s-\s"  # " - "
    username = r"([\w\s]+)"  # e.g., "Martin"
    metadata_end = r":\s"  # ": "
    pattern = date_time + dash_whitespace + username + metadata_end
    cleaned_data = re.sub(pattern, "", chat_data)
    return tuple(cleaned_data.split("\n"))

def remove_non_message_text(export_text_lines):
    messages = export_text_lines[1:-1]

    filter_out_msgs = ("<Media omitted>",)
    return tuple((msg for msg in messages if msg not in filter_out_msgs))

def clean_corpus(chat_file):
    """
    Reads chat data from a file, cleans it, and returns a list of (question, reply) tuples.

    Args:
        chat_file (file obj): An opened file object containing chat data.

    Returns:
        list: A list of tuples containing cleaned conversation data.
    """
    chat_data = chat_file.read().decode()
    message_corpus = remove_chat_metadata(chat_data)
    cleaned_corpus = remove_non_message_text(message_corpus)
    return [(line.split(":", 1)[0].strip(), line.split(":", 1)[1].strip()) for line in cleaned_corpus]