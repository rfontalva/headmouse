import cv2
import numpy as np
import requests
from pynput.mouse import (
    Button,
    Controller,
)
import os
import dlib
from scipy.spatial import distance as dist

# DEFINES
COEFSENS = 0.3

RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
NOSE_POINT = 34
# MOUTH_OUTLINE_POINTS = list(range(48, 61))
# MOUTH_INNER_POINTS = list(range(61, 68))

EYE_AR_THRESH = 0.2
EYE_AR_CONSEC_FRAMES = 2

COUNTER_LEFT = 0
COUNTER_RIGHT = 0

CALIBRATE = 0


###

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


dir = os.path.dirname(__file__)
PREDICTOR_PATH = os.path.join(dir, "shape_predictor_68_face_landmarks.dat")


def download_file(url):
    print('downloading...')
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    print('download complete')
    return local_filename


class HeadMouse(object):
    def __init__(self):
        global PREDICTOR_PATH
        self.detector = dlib.get_frontal_face_detector()
        self.cap = cv2.VideoCapture(0)
        if not os.path.exists(PREDICTOR_PATH):
            download_file('https://github.com/AKSHAYUBHAT/TensorFace/raw/master/openface/models/dlib/shape_predictor_68_face_landmarks.dat')
        self.predictor = dlib.shape_predictor(PREDICTOR_PATH)
        self.cal = 0
        self.nose_y = 0
        self.nose_x = 0
        self.center = [self.nose_x, self.nose_y]
        self.mouse = Controller();
        self.function = None

    def refresh(self, useMouse=True):
        global NOSE_POINT, CALIBRATE, EYE_AR_CONSEC_FRAMES, COUNTER_RIGHT, EYE_AR_THRESH
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = self.detector(gray, 0)
            for rect in rects:
                landmarks = np.matrix([[p.x, p.y] for p in self.predictor(frame, rect).parts()])
                self.left_eye = landmarks[LEFT_EYE_POINTS]  # El ojo  derecho es el left y viceversa, porque la imagen esta espejada
                self.right_eye = landmarks[RIGHT_EYE_POINTS]
                ear_right = eye_aspect_ratio(self.right_eye)
                nose = landmarks[NOSE_POINT]
                nose_position = nose[0]
                self.nose_x = nose_position[:, 0]
                self.nose_y = nose_position[:, 1]
                if self.cal == CALIBRATE:
                    self.center = [self.nose_x, self.nose_y]
                    self.cal = not (CALIBRATE)
                if useMouse:
                    self.mouse.position = (self.mouse.position[0] + COEFSENS * (self.nose_x - self.center[0]), self.mouse.position[1] + COEFSENS * (self.nose_y - self.center[1]))
                if ear_right < EYE_AR_THRESH:
                    COUNTER_RIGHT += 1
                else:
                    if COUNTER_RIGHT >= EYE_AR_CONSEC_FRAMES:
                        if self.function is not None:
                            self.function()
                        elif useMouse:
                            self.mouse.click(Button.left, 1)
                    COUNTER_RIGHT = 0

    def refresh_mouse(self):
        global COEFSENS
        self.mouse.position = (self.mouse.position[0] + COEFSENS * (self.nose_x - self.center[0]), self.mouse.position[1] + COEFSENS * (self.nose_y - self.center[1]))

    def quit(self):
        self.cap.release()

    def get_position(self):
        return self.nose_x, self.nose_y

    def calibrate(self):
        global CALIBRATE
        self.cal = CALIBRATE

    def onRightEye_closed(self, function):
        self.function = function
