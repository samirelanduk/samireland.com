import re

def split(raw_text):
    text = re.sub("\r\n", "\n", raw_text)
    text = re.sub("[\n]{2,}", "\n\n", text)
    return text.split("\n\n")


def process_hyperlink(samdown):
    text = samdown.split("](")[0][1:]
    link = samdown.split("](")[1][:-1].split()[0]
    newpage = "newpage" in samdown.split("](")[1][:-1]
    return '<a href="%s"%s>%s</a>' % (
     link, ' target="_blank"' if newpage else "", text
    )


def process_block(block):
    hyperlink_pattern = "\[.+?\]\(.+?\)"
    hyperlinks = re.findall(hyperlink_pattern, block)[::-1]
    block = re.sub(hyperlink_pattern, "\x00", block)

    while block.count("**") >= 2:
        block = block.replace("**", "<b>", 1)
        block = block.replace("**", "</b>", 1)

    while block.count("*") >= 2:
        block = block.replace("*", "<em>", 1)
        block = block.replace("*", "</em>", 1)

    while block.count("_") >= 2:
        block = block.replace("_", "<u>", 1)
        block = block.replace("_", "</u>", 1)

    while "\x00" in block:
        block = block.replace("\x00", process_hyperlink(hyperlinks.pop()), 1)

    return "<p>%s</p>" % block


def process_samdown(raw_text):
    return "\n".join([process_block(block) for block in split(raw_text)])
