from PIL import Image


def save_as_jpeg(image_stream, path):
    image = Image.open(image_stream)
    image.save(path, format='jpeg')
