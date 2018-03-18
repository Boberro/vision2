from PIL import Image


def crop_image(image_stream, vertices, path, width=256):
    image = Image.open(image_stream)

    min_x = sorted(vertices, key=lambda v: v['x'])[0]['x']
    max_x = sorted(vertices, key=lambda v: v['x'], reverse=True)[0]['x']
    min_y = sorted(vertices, key=lambda v: v['y'])[0]['y']
    max_y = sorted(vertices, key=lambda v: v['y'], reverse=True)[0]['y']

    thumb = image.crop((min_x, min_y, max_x, max_y))
    thumb.thumbnail((width, width))
    thumb.save(path, format="jpeg")
    return thumb
