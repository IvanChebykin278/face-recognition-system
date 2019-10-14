import face_recognition
import numpy as np
import cv2
import uuid
import time
from flask import jsonify

def predict(file_stream):
    
    # remove декодирование изображений
    vanya_image = face_recognition.load_image_file("ivan.jpg")
    vanya_face_encoding = face_recognition.face_encodings(vanya_image)[0]

    artem_image = face_recognition.load_image_file("artem.jpg")
    artem_face_encoding = face_recognition.face_encodings(artem_image)[0]

    vova_image = face_recognition.load_image_file("vova.jpg")
    vova_face_encoding = face_recognition.face_encodings(vova_image)[0]

    # вытягиваем из базы данные кодированных лиц (всех) и помощаем их в массив извесных лиц
    # p.s скорее всего это нужно сделать до того как обрадимся с сервису
    # что бы не тянуть данный при каждом фрейме

    start = time.time()

    known_face_encodings = [
        # данные который мы достали из базы
        # при это здесь должны быть только массивы с числами
        vanya_face_encoding,
        artem_face_encoding,
        vova_face_encoding
    ]

    known_face_ids = [
        # имена лиц
        # то есть id которые указывают на конкретного сотрудника/зайца в базе
        'vanya',
        'artem',
        'vova'
    ]

    face_locations = []
    unknown_face_locations = []
    face_encodings = []
    unknown_face_encodings = []
    face_ids = []

    # генерируем индивидуальный id для неизвестного лица
    id_unknown_faces = []

    frame = face_recognition.load_image_file(file_stream)

    # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        face_id = uuid.uuid4().hex

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            face_id = known_face_ids[best_match_index]
        else:
            unknown_face_encodings.append(face_encoding)
            id_unknown_faces.append(face_id)

        face_ids.append(face_id)
    
    if len(id_unknown_faces) != 0 and len(unknown_face_encodings) != 0:
        # отправляем в базу данных неизвестные лица и их кодировки
        # отправляем в базу нужный ивент
        return jsonify({"seccess": True, "msg": 'found unkown face(s)', "face": face_ids,"time":time.time()-start})

    return jsonify({"seccess":True,"msg": face_ids, "time":time.time()-start})