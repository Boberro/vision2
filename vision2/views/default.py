from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from vision2.models import UploadedImage
import json
import os
import transaction


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    thumbnails = request.dbsession.query(UploadedImage).all()
    return {
        "thumbnails": thumbnails,
    }


@view_config(route_name='single_image', renderer='../templates/single_image.jinja2')
def single_image_view(request):
    uid = request.matchdict.get('uid', None)

    image = request.dbsession.query(UploadedImage).filter(
        UploadedImage.uid == uid
    ).first()

    if image is None:
        raise HTTPNotFound()

    return {
        "image": image,
    }


@view_config(route_name='single_image_vision_data', renderer='json')
def get_vision_data_view(request):
    uid = request.matchdict.get('uid', None)

    image = request.dbsession.query(UploadedImage).filter(
        UploadedImage.uid == uid
    ).first()

    data = json.loads(image.face_data)

    return data


@view_config(route_name='delete_image')
def delete_image_action(request):
    uid = request.matchdict.get('uid', None)

    with transaction.manager:
        request.dbsession.query(UploadedImage).filter(
            UploadedImage.uid == uid
        ).delete()

    uploads_directory = request.registry.settings.get('vision2.uploads_directory', '/tmp')
    file_path = os.path.join(uploads_directory, uid)
    thumb_path = os.path.join(uploads_directory, 'thumb_' + uid)

    try:
        os.remove(file_path)
        os.remove(thumb_path)
    except OSError:
        pass

    raise HTTPFound(request.route_path('home'))
