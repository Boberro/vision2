def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('upload_image', '/upload_image')
    config.add_route('single_image', '/img/{uid}')
    config.add_route('uploaded_file', '/uploaded_files/{uid}')
