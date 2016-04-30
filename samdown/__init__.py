import re

def split(raw_text):
    text = re.sub("\r\n", "\n", raw_text)
    text = re.sub("[\n]{2,}", "\n\n", text)
    return text.split("\n\n")
