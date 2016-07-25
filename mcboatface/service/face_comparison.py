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


class FaceComparisonService (object):
    def __init__(self, *args, **kwargs):
        self.dlibFacePredictor = os.path.join(
            dlibModelDir,
            kwargs.get(
                'dlibFacePredictor',
                "shape_predictor_68_face_landmarks.dat"))

        self.networkModel = os.path.join(
            openfaceModelDir,
            kwargs.get('openfaceModelDir', "nn4.small2.v1.t7"))

        self.imgDim = kwargs.get('imgDim', 96)
        self.align = openface.AlignDlib(self.dlibFacePredictor)
        self.net = openface.TorchNeuralNet(self.networkModel, self.imgDim)

    def get_all_representations(imgPath):
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
                args.imgDim, rgbImg, bb,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if alignedFace is None:
                continue
            representations.append(self.net.forward(alignedFace))
        return rep

    def get_image_representation(imgPath):
        bgrImg = cv2.imread(imgPath)
        if bgrImg is None:
            raise Exception("Unable to load image: {}".format(imgPath))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        bb = self.align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            return None

        alignedFace = self.align.align(
            args.imgDim, rgbImg, bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            return None

        rep = self.net.forward(alignedFace)
        return rep

    def compare_representations(repr1, repr2):
        d = repr1 - repr2
        return np.dot(d, d)
