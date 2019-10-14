import os
from flask import Flask, jsonify
from cfenv import AppEnv

import logging
from cf_logging import flask_logging

#imports for user authorization
from flask import request

# import classifer
import pickle
from sklearn import neighbors

app = Flask(__name__)
env = AppEnv()

flask_logging.init(app, logging.INFO)
logger = logging.getLogger('route.logger')

#assign port for Flask application to run on
port = int(os.environ.get('PORT', 3000))
hana = env.get_service(name='hdi_db')

#access credentials of uaa service
# uaa_service = env.get_service(name='openSAPHANA-uaa').credentials

@app.route('/train')
def train():
    model_save_path="./trained_knn_model.clf"
    n_neighbors=2
    knn_algo='ball_tree'

    X = [[0., 1.],[1.,0.],[1.,1.],[0.,0.]]
    y = [0,0,1,1]

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return jsonify({"output": 'Training complete!'})

@app.route('/predict')
def predict():
    knn_clf=None
    model_path="./trained_knn_model.clf"

    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    output = knn_clf.predict([[1.,1.]])

    return jsonify({'output': output.tolist()})

@app.route('/')
def hello():
    return 'hello'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
