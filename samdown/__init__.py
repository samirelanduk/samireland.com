import re

def split(raw_text):
    text = re.sub("\r\n", "\n", raw_text)
    text = re.sub("[\n]{2,}", "\n\n", text)
    return text.split("\n\n")


def process_hyperlink(linkmarkup):
    text = linkmarkup.split("](")[0][1:]
    link = linkmarkup.split("](")[1][:-1].split()[0]
    newpage = "newpage" in linkmarkup.split("](")[1][:-1]
    return '<a href="%s"%s>%s</a>' % (
     link, ' target="_blank"' if newpage else "", text
    )


def process_block(block):
    if re.match("^\[.+?\]\(.+?\)$", block):
        return process_special_block(block)
    else:
        return process_normal_block(block)


def process_normal_block(block):
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


def process_special_block(block):
    block_type = block.split("](")[0][1:]
    block_arg = block.split("](")[1][:-1]
    if block_type == "YOUTUBE":
        return '<div class="youtube"><iframe src="//www.youtube.com/embed/%s" \
        frameborder="0" allowfullscreen></iframe></div>' % block_arg

    elif block_type == "IMAGE":
        filename = block_arg.split()[:1][0]
        args = " ".join(block_arg.split()[1:])
        args = re.findall('[AC]:".*?"', args)
        args = {arg[0]: arg[3:-1] for arg in args}
        return '<figure><img src="/static/images/%s"%s>%s</figure>' % (
         filename,
         ' title="%s"' % args["A"] if "A" in args else "",
         "<figcaption>%s</figcaption>"  % args["C"] if "C" in args else ""
        )
    else:
        return ""

def process_samdown(raw_text):
    return "\n".join([process_block(block) for block in split(raw_text)])
