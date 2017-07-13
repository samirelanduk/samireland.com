def process_image_block(block):
    from media.models import MediaFile
    imagename, title = block.split("[")[-1][:-1], ""
    if "@" in imagename:
        imagename, *chunks = imagename.split("@")
        title = "@".join(chunks)
    image = MediaFile.objects.all().filter(mediatitle=imagename).first()
    return "<figure><img src='/{}' title='{}'></figure>".format(
     image.mediafile.url if image else imagename, title
    )


def process_video_block(block):
    from media.models import MediaFile
    videoname = block.split("[")[-1][:-1]
    video = MediaFile.objects.all().filter(mediatitle=videoname).first()
    return "<video src='/{}' controls></video>".format(
     video.mediafile.url if video else videoname
    )
