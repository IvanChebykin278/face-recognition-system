from app import app
from flask import request, jsonify
from allowed import allowed_file
from lib.trained.training_0_0_2 import training
from lib.search.search_0_0_2 import predict
import os
import PIL
import pickle
import uuid
import time

PATH = os.getcwd()

@app.route('/train')
def train():
    if request.method == 'GET':
        classifier = training(train_dir="./train_dir", n_neighbors=2)

        with open("./trained_knn_model.clf", 'wb') as f:
            pickle.dump(classifier, f)

        return jsonify({"success": True, "msg": 'classifier created successfully'})

    return jsonify({"success": False, "msg": 'request method is not GET'})

@app.route('/predict', methods=['GET', 'POST'])
def search_faces_on_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"success": False, "msg": 'File not found'})

        file = request.files['image']
       
        if file.filename == '':
            return jsonify({"success": False, "msg": 'File name is enpty'})

        if file and allowed_file(file.filename):
            # return 'none'
            start = time.time()
            with open("./trained_knn_model.clf", 'rb') as f:
                classifier = pickle.load(f)
            print(" - open knn_clf time = {}".format(time.time()-start))
            
            start = time.time()
            predictions = predict(image=file, knn_clf=classifier)
            print(" - predict = {}".format(time.time()-start))
            print(predictions)
            return "seccess"

    return jsonify({"success": False, "msg": 'Request method is not POST'})

@app.route('/append', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        train_dir_path = os.path.join(PATH, "train_dir")
        print(os.path.isdir(train_dir_path))

        if not os.path.isdir(train_dir_path):
            try:
                os.mkdir(train_dir_path)
            except OSError:
                return {
                    "seccess": False,
                    "msg": 'failed to create directory ' + train_dir_path
                }

        images_dir_path = os.path.join(train_dir_path, uuid.uuid4().hex)

        if os.path.isdir(images_dir_path):
            return {
                "seccess": False,
                "msg": images_dir_path + ' is exists'
            }

        try:
            os.mkdir(images_dir_path)
        except OSError:
            return {
                "seccess": False,
                "msg": 'failed to create directory ' + images_dir_path
            }

        for name in request.files:
            file = request.files[name]
            image = PIL.Image.open(file)
            image.save(os.path.join(images_dir_path, file.filename))

        return jsonify({"success": True, "msg": 'training images added successfully'})

    return jsonify({"success": False, "msg": 'request method is not POST'})

if __name__ == '__main__':
    app.run(debug=True)