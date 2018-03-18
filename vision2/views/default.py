from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from vision2.models import UploadedImage
import json


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    return {}


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
