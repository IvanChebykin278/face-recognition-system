import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import time
import cv2

def predict(image, knn_clf=None, distance_threshold=0.6):
    """
    Recognizes faces in given image using a trained KNN classifier
    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """

    if knn_clf is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf")

    # Load image file and find face locations
    start = time.time()
    X_img = face_recognition.load_image_file(image)
    print(" - face_recognition.load_image_file = {}".format(time.time()-start))

    start = time.time()
    small_frame = cv2.resize(X_img, (0, 0), fx=0.2, fy=0.2)
    rgb_small_frame = small_frame[:, :, ::-1]
    print(" - small_frame, rgb_small_frame = {}".format(time.time()-start))

    start = time.time()
    X_face_locations = face_recognition.face_locations(small_frame)
    print(" - X_face_locations = {}".format(time.time()-start))

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge X_img
    start = time.time()
    faces_encodings = face_recognition.face_encodings(rgb_small_frame, known_face_locations=X_face_locations)
    print(" - faces_encodings = {}".format(time.time()-start))

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

