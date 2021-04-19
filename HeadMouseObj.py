import cv2
import numpy as np
import os
import dlib
from pynput.mouse import Button, Controller
from HeadMouse_utils import eye_aspect_ratio


class HeadMouse(object):
    def __init__(self, is_right=True, use_mouth_twitch=False, sensitivity=None):
        dir = os.path.dirname(__file__)
        predictor_path = os.path.join(
            dir, "shape_predictor_68_face_landmarks.dat")
        self.detector = dlib.get_frontal_face_detector()
        self.cap = cv2.VideoCapture(0)
        self.predictor = dlib.shape_predictor(predictor_path)
        self.is_calibrated = False
        self.nose_y = 0
        self.nose_x = 0
        self.center = [self.nose_x, self.nose_y]
        self.mouse = Controller()
        self.function = None
        self.mouth_twitched_function = None
        self.coef_sens = sensitivity or 0.3
        if is_right:
            self.eye_points = list(range(36, 42))
        else:
            self.eye_points = list(range(42, 48))
        self.nose_point = 34
        self.mouth_right_points = [55, 65]
        self.ear_thresh = 0.2
        self.ear_consec_frames = 2
        self.eye_counter = 0
        self.prev_mouth_position = [0, 0]
        self.use_mouth_twitch = use_mouth_twitch

    def refresh(self, use_mouse=True):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = self.detector(gray, 0)
            for rect in rects:
                landmarks = np.matrix(
                    [[p.x, p.y] for p in self.predictor(frame, rect).parts()])
                self.update_nose_position(landmarks)
                if self.is_calibrated == False:
                    self.center = [self.nose_x, self.nose_y]
                    self.is_calibrated = True
                self.mouth_processing(landmarks)
                self.eye_processing(landmarks)
                if use_mouse:
                    self.update_mouse_position()   

    def quit(self):
        self.cap.release()

    def get_position(self):
        return self.nose_x, self.nose_y

    def get_center(self):
        return self.center

    def calibrate(self):
        self.is_calibrated = False

    def on_eye_closed(self, function):
        self.function = function

    def on_mouth_twitched(self, function):
        self.mouth_twitched_function = function

    def mouth_processing(self, landmarks):
        if self.use_mouth_twitch:
            self.mouth_right_corner = landmarks[self.mouth_right_points]
            right_corner_position = self.mouth_right_corner[0]
            rcp_x = right_corner_position[:, 0]
            rcp_y = right_corner_position[:, 1]
            rel_rcp_x = int(rcp_x - self.nose_x)
            rel_rcp_y = int(self.nose_y - rcp_y)
            if self.prev_mouth_position[0] not in range(rel_rcp_x - 2, rel_rcp_y + 2):
                if self.mouth_twitched_function is not None:
                    self.mouth_twitched_function()
                self.prev_mouth_position[0] = rel_rcp_x

    def update_mouse_position(self):
        rel_x_mov = self.coef_sens * (self.nose_x - self.center[0])
        rel_y_mov = self.coef_sens * (self.nose_y - self.center[1])
        if np.absolute(rel_x_mov) > 2:
            new_mouse_x = self.mouse.position[0] + rel_x_mov
            self.mouse.position = (self.mouse.position[0] + self.coef_sens * (self.nose_x - self.center[0]), self.mouse.position[1])
        if np.absolute(rel_y_mov) > 2:
            new_mouse_y = self.mouse.position[1] + rel_y_mov
            self.mouse.position = (self.mouse.position[0], self.mouse.position[1] + self.coef_sens * (self.nose_y - self.center[1]))

    def eye_processing(self, landmarks):
        self.eye = landmarks[self.eye_points]
        ear = eye_aspect_ratio(self.eye)
        if ear < self.ear_thresh:
            self.eye_counter += 1
        else:
            if self.eye_counter >= self.ear_consec_frames:
                if self.function is not None:
                    self.function()
                elif use_mouse:
                    self.mouse.click(Button.left, 1)
            self.eye_counter = 0

    def update_nose_position(self, landmarks):
        nose = landmarks[self.nose_point]
        nose_position = nose[0]
        self.nose_x = nose_position[:, 0]
        self.nose_y = nose_position[:, 1]
