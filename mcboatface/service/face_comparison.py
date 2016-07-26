import time
import argparse
import cv2
import itertools
import os

import numpy as np
np.set_printoptions(precision=2)

import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'trained_models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')


class FaceRepresentationService (object):
    def __init__(self, *args, **kwargs):
        """Initialises the service with the defined params."""
        # Ideally we would hava a hash of the trained model
        self.dlib_face_predictor = kwargs.get(
            'dlib_face_predictor',
            "shape_predictor_68_face_landmarks.dat")

        self.dlib_face_predictor_path = os.path.join(
                    dlibModelDir,
                    self.dlib_face_predictor)

        self.network_model = kwargs.get(
            'openfaceModelDir', "nn4.small2.v1.t7")

        self.network_model_path = os.path.join(
            openfaceModelDir,
            self.network_model)

        self.img_dim = kwargs.get('img_dim', 96)
        self.align = openface.AlignDlib(self.dlib_face_predictor_path)
        self.net = openface.TorchNeuralNet(
            self.network_model_path, self.img_dim)

    def get_all_representations(self, imgPath):
        """Return the feature space of all faces in the picture"""
        bgrImg = cv2.imread(imgPath)
        if bgrImg is None:
            raise Exception("Unable to load image: {}".format(imgPath))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        bbs = self.align.getAllFaceBoundingBoxes(rgbImg)
        if bbs is None:
            return

        representations = []

        for bb in bbs:
            alignedFace = self.align.align(
                self.img_dim, rgbImg, bb,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if alignedFace is None:
                continue
            representations.append(self.net.forward(alignedFace))

        return representations

    def get_image_representation(self, imgPath):
        """Return the feature space of the main face in the picture."""
        bgrImg = cv2.imread(imgPath)
        if bgrImg is None:
            raise Exception("Unable to load image: {}".format(imgPath))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        bb = self.align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            return None

        alignedFace = self.align.align(
            self.img_dim, rgbImg, bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            return None

        rep = self.net.forward(alignedFace)
        return rep

    def compare_representations(self, repr1, repr2):
        """Return the dot product distance between two faces"""
        d = repr1 - repr2
        return np.dot(d, d)


    def get_absolute_representation(self, repr1):
        """Return a representation of the face and the generation params."""
        return {
            'representation': list(repr1),
            'face_predictor': self.dlib_face_predictor,
            'img_dim': self.img_dim,
            'network_model': self.network_model
        }
