# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.response import FileResponse
from pyramid.httpexceptions import HTTPNotFound
import os


@view_config(route_name='uploaded_file')
def uploaded_file_static_view(request):
    uid = request.matchdict.get('uid', None)
    if uid is None:
        return HTTPNotFound()

    uploads_directory = request.registry.settings.get('vision2.uploads_directory', '/tmp')
    path = os.path.join(uploads_directory, uid)

    response = FileResponse(
        path,
        request=request,
        content_type='image/jpeg'
    )
    return response


@view_config(route_name='uploaded_file_thumbnail')
def uploaded_file_thumbnail_static_view(request):
    uid = request.matchdict.get('uid', None)
    if uid is None:
        return HTTPNotFound()

    uploads_directory = request.registry.settings.get('vision2.uploads_directory', '/tmp')
    path = os.path.join(uploads_directory, 'thumb_' + uid)

    response = FileResponse(
        path,
        request=request,
        content_type='image/jpeg'
    )
    return response
