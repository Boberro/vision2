# -*- coding: utf-8 -*-
import os
import uuid
import shutil
from pyramid.view import view_config
from vision2.models import UploadedImage
import transaction
from pyramid.httpexceptions import HTTPFound
from vision2.util import get_vision_data, crop_image
import json


@view_config(route_name='upload_image')
def store_image_action_view(request):
    uploads_directory = request.registry.settings.get('vision2.uploads_directory', '/tmp')
    temp_uploads_directory = request.registry.settings.get('vision2.temp_uploads_directory', '/tmp')

    filename = request.POST['image'].filename

    input_file = request.POST['image'].file

    uid = '%s' % uuid.uuid4()

    file_path = os.path.join(uploads_directory, uid)
    temp_file_path = os.path.join(temp_uploads_directory, '~' + uid)
    thumb_path = os.path.join(uploads_directory, 'thumb_' + uid)

    input_file.seek(0)
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)

    os.rename(temp_file_path, file_path)

    input_file.seek(0)
    face_detection_data, cropping_data = get_vision_data(request, input_file)
    input_file.seek(0)
    crop_image(input_file, cropping_data, thumb_path)

    with transaction.manager:
        file_record = UploadedImage(
            filename=filename,
            uid=uid,
            face_data=json.dumps(face_detection_data),
        )
        request.dbsession.add(file_record)

    return HTTPFound(request.route_path('single_image', uid=uid))
