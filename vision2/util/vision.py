import os
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2.service_account import Credentials


def get_vision_data(request, image_data):
    key_path = request.registry.settings.get('vision2.service_key_path', None)
    credentials = Credentials.from_service_account_file(key_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = types.Image(content=image_data.read())
    response = client.face_detection(image=image)
    error = response.error
    if error:
        print "Error:"
        print error
    faces = response.face_annotations
    data = []
    for face in faces:
        print "Face:"

        vertices = []
        for v in face.fd_bounding_poly.vertices:
            vertices.append({
                "x": v.x,
                "y": v.y,
            })

        emotions = [
            ("joy", face.joy_likelihood),
            ("sorrow", face.sorrow_likelihood),
            ("anger", face.anger_likelihood),
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
