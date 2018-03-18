import time
from pyramid.static import QueryStringConstantCacheBuster


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=1)
    config.add_cache_buster('vision2:static/', QueryStringConstantCacheBuster(str(int(time.time()))))  # TODO: remove me
    config.add_route('home', '/')
    config.add_route('upload_image', '/upload_image/')
    config.add_route('single_image', '/img/{uid}/')
    config.add_route('delete_image', '/img/{uid}/delete/')
    config.add_route('uploaded_file', '/uploaded_files/{uid}/')
    config.add_route('uploaded_file_thumbnail', '/uploaded_files/{uid}/thumbnail/')
    config.add_route('single_image_vision_data', '/img/{uid}/vision_data.json')
