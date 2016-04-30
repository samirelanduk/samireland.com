import re

def split(raw_text):
    text = re.sub("\r\n", "\n", raw_text)
    text = re.sub("[\n]{2,}", "\n\n", text)
    return text.split("\n\n")


def process_block(block):
    while block.count("**") >= 2:
        block = block.replace("**", "<b>", 1)
        block = block.replace("**", "</b>", 1)

    while block.count("*") >= 2:
        block = block.replace("*", "<em>", 1)
        block = block.replace("*", "</em>", 1)

    while block.count("_") >= 2:
        block = block.replace("_", "<u>", 1)
        block = block.replace("_", "</u>", 1)

    return "<p>%s</p>" % block


def process_samdown(raw_text):
    return "\n".join([process_block(block) for block in split(raw_text)])
