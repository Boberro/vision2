from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from vision2.models import UploadedImage
import json
import os
import transaction
import random


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

    thumbnail_query = request.dbsession.query(UploadedImage).filter(UploadedImage.id != image.id)
    number_of_thumbnails = min(4, thumbnail_query.count())
    thumbnails = random.sample(thumbnail_query.all(), number_of_thumbnails)

    return {
        "image": image,
        "thumbnails": thumbnails,
    }


@view_config(route_name='single_image_vision_data', renderer='string')
def get_vision_data_view(request):
    uid = request.matchdict.get('uid', None)

    image = request.dbsession.query(UploadedImage).filter(
        UploadedImage.uid == uid
    ).first()

    return image.face_data


@view_config(route_name='delete_image')
def delete_image_action(request):
    uid = request.matchdict.get('uid', None)

    with transaction.manager:
        request.dbsession.query(UploadedImage).filter(
            UploadedImage.uid == uid
        ).delete()

    uploads_directory = request.registry.settings.get('vision2.uploads_directory', '/tmp')
    file_path = os.path.join(uploads_directory, uid + '.jpg')
    thumb_path = os.path.join(uploads_directory, 'thumb_' + uid + '.jpg')

    try:
        os.remove(file_path)
        os.remove(thumb_path)
    except OSError:
        pass

    raise HTTPFound(request.route_path('home'))
