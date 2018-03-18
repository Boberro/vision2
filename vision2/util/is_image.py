from PIL import Image


def is_image(file):
    try:
        image = Image.open(file)
    except IOError:
        return False
    return True
