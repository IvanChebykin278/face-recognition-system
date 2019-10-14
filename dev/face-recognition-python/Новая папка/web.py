import face_recognition
from flask import Flask, request, redirect, jsonify, Response
import numpy as np
import cv2
import uuid
import time

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# пока не очень понятно ка кименно будет производится обработка 
# или покаетом фреймов или по одному
def detect_faces_in_frame(file_stream):

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


def encodings_face_in_image(file_stream):
    img = face_recognition.load_image_file(file_stream)
    encoding = face_recognition.face_encodings(img)[0]

    # todo: Отправка данных кодировки в базу данных
    # todo: Проверка на успешность отправки
    # if(db.isconnected()):
    #     return jsonify({"seccess": True,"msg":'data sent successfully'})
    # else:
    #     return jsonify({"seccess": False,"msg":'data sent not successfully'})

    return jsonify({"seccess": True,"encoding": encoding.tolist()})

@app.route('/insert', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"success": False, "msg": 'File not found'})

        file = request.files['image']
       
        if file.filename == '':
            return jsonify({"success": False, "msg": 'File name is enpty'})

        if file and allowed_file(file.filename):
            return encodings_face_in_image(file)

    return jsonify({"success": False, "msg": 'Request method is not POST'})

@app.route('/search', methods=['GET', 'POST'])
def search_faces_on_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"success": False, "msg": 'File not found'})

        file = request.files['image']
       
        if file.filename == '':
            return jsonify({"success": False, "msg": 'File name is enpty'})

        if file and allowed_file(file.filename):
            return detect_faces_in_frame(file)

    return jsonify({"success": False, "msg": 'Request method is not POST'})
    

if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)