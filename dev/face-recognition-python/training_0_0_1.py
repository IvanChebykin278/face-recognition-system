import face_recognition
import numpy as np
import cv2
import uuid
import time
from flask import jsonify

def training(file_stream):
    
    img = face_recognition.load_image_file(file_stream)
    encoding = face_recognition.face_encodings(img)[0]

    # todo: Отправка данных кодировки в базу данных
    # todo: Проверка на успешность отправки
    # if(db.isconnected()):
    #     return jsonify({"seccess": True,"msg":'data sent successfully'})
    # else:
    #     return jsonify({"seccess": False,"msg":'data sent not successfully'})

    return jsonify({"seccess": True,"encoding": encoding.tolist()})