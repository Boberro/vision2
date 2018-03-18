import os
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2.service_account import Credentials


def get_vision_data(request, image_data):
    key_path = request.registry.settings.get('vision2.service_key_path', None)
    credentials = Credentials.from_service_account_file(key_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image_data.seek(0)
    image = types.Image(content=image_data.read())

    face_detection_data = _detect_faces(client, image)

    cropping_data = _detect_cropping(client, image)

    return face_detection_data, cropping_data


def _detect_faces(client, image):
    response = client.face_detection(image=image)
    error = response.error
    faces = response.face_annotations
    data = []
    for face in faces:
        vertices = []
        for v in face.fd_bounding_poly.vertices:
            vertices.append({
                "x": v.x,
                "y": v.y,
            })

        emotions = [
            ("anger", face.anger_likelihood),
            ("joy", face.joy_likelihood),
            ("sorrow", face.sorrow_likelihood),
            ("surprise", face.surprise_likelihood)
        ]
        possible_dominant_emotion = sorted(emotions, key=lambda x: x[1], reverse=True)[0]
        if possible_dominant_emotion[1] > 3:
            dominant_emotion = possible_dominant_emotion[0]
        else:
            dominant_emotion = "neutral"

        roll = face.roll_angle

        data.append({
            "vertices": vertices,
            "dominant_emotion": dominant_emotion,
            "roll": roll,
        })
    return data


def _detect_cropping(client, image):
    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.0])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    vertices = []
    for v in hints[0].bounding_poly.vertices:
        vertices.append({
            "x": v.x,
            "y": v.y,
        })

    return vertices
