import face_recognition
from flask import Flask, request, redirect, jsonify, Response

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def detect_faces_in_image(file_stream):
    img = face_recognition.load_image_file(file_stream)
    encoding = face_recognition.face_encodings(img)[0]

    # todo: Отправка данных кодировки в базу данных
    # todo: Проверка на успешность отправки
    # if(db.isconnected()):
    #     return jsonify({"seccess": True,"msg":'data sent successfully'})
    # else:
    #     return jsonify({"seccess": False,"msg":'data sent not successfully'})

    return jsonify({"seccess": True,"encoding": encoding.tolist()})

@app.route('/', methods=['GET', 'POST'])
def upload_image():
     # Check if a valid image file was uploaded
    print(request.form.tolist())
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"success": False, "msg": 'File not found'})

        file = request.files['image']
       
        if file.filename == '':
            return jsonify({"success": False, "msg": 'File name is enpty'})

        if file and allowed_file(file.filename):
            return detect_faces_in_image(file)

    return jsonify({"success": False, "msg": 'Request method is not POST'})

if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)