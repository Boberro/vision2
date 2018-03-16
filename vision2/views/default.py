from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPServerError
from vision2.models import UploadedImage


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    return {}


@view_config(route_name='single_image', renderer='../templates/single_image.jinja2')
def single_image_view(request):
    uid = request.matchdict.get('uid', None)
    if uid is None:
        return HTTPNotFound()

    image = request.dbsession.query(UploadedImage).filter(
        UploadedImage.uid == uid
    ).first()

    if image is None:
        return HTTPServerError()

    return {
        "image": image,
    }
