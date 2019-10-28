from app import app
from flask import request, jsonify
from allowed import allowed_file
from lib.search.search_0_0_1 import predict
from lib.trained.training_0_0_1 import training

@app.route('/insert', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"success": False, "msg": 'File not found'})

        file = request.files['image']
       
        if file.filename == '':
            return jsonify({"success": False, "msg": 'File name is enpty'})

        if file and allowed_file(file.filename):
            # return 'none'
            print(file)
            return training(file)

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
            # return 'none'
            print(file)
            return predict(file)

    return jsonify({"success": False, "msg": 'Request method is not POST'})

if __name__ == '__main__':
    app.run(debug=True)