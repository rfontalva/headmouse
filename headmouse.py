"""
The HeadMouse module provides an interface by opening the web camera and 
detecting the user's face to control the mouse by tilting the head using 
the tip of the nose as reference point.
It can also be customized to trigger different functions instead of a mouse
click when the user winks.
To use the module it's necessary to have the file shape_predictor_68_face_landmarks.dat
Compressed: 
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

Uncompressed:
https://github.com/rfontalva/dlib_shape_predictor_68_face_landmarks/tree/master
"""

import cv2
import numpy as np
import dlib
from typing import TypeVar
from .headmouse_singleton import HeadMouseSingleton
from .headmouse_utils import eye_aspect_ratio
from .controller.mouse_controller import MouseController
from .controller.abstract_controller import AbstractController

AbstractController_ = TypeVar('AbstractController_', bound=AbstractController)

class HeadMouse(metaclass=HeadMouseSingleton):
    """
    Parameters:

    sensitivity (int): Determines how fast and precisely the mouse pointer
    will move, default is 0.3.
    use_right_eye (bool): Which eye will be used to trigger the wink
    command.
    use_mouth_twitch (bool): Whether mouth movements will be
    evaluated or not.
    """
    def __init__(self, predictor_path, sensitivity=None, use_right_eye=True, use_mouth_twitch=False, camera_path=None):
        self.detector = dlib.get_frontal_face_detector()
        self.cap = cv2.VideoCapture(0)
        if camera_path:
            self.cap.open(camera_path)
        if not self.cap.isOpened():
            raise Exception(f'No camera available')
        self.predictor = dlib.shape_predictor(predictor_path)
        self.is_calibrated = False
        self.nose_y = 0
        self.nose_x = 0
        self.center = [self.nose_x, self.nose_y]
        self.coef_sens = sensitivity or 0.3
        self.controller = MouseController(self.coef_sens)
        self.wink_function = None
        self.use_mouth_twitch = use_mouth_twitch
        self.mouth_twitched_function = None
        self.thresh_x = self.thresh_y = 5
        if use_right_eye:
            self.eye_points = list(range(36, 42))
        else:
            self.eye_points = list(range(42, 48))
        self.nose_point = 34
        self.mouth_right_points = [55, 65]
        self.ear_thresh = 0.2
        self.ear_consec_frames = 2
        self.eye_counter = 0
        self.prev_mouth_position = [0, 0]

    def refresh(self):
        """
        It should be called at least at the same frequency at which the web camera 
        refreshes. Setting use_mouse to false allows to test
        the rest of functionalities without having the mouse pointer attached to the
        movement of the users' head.
        """
        ret, self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame, 1)
        if ret:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            rects = self.detector(gray, 0)
            for rect in rects:
                landmarks = np.matrix(
                    [[p.x, p.y] for p in self.predictor(self.frame, rect).parts()])
                self._update_nose_position(landmarks)
                if self.is_calibrated == False:
                    self.center = [self.nose_x, self.nose_y]
                    self.is_calibrated = True
                self._mouth_processing(landmarks)
                self._eye_processing(landmarks)
                self._update_position()

    def quit(self):
        self.cap.release()

    def calibrate(self):
        """
        The next time self.refresh gets called, the point of reference from which
        the pointer is moved will be readjusted to where the user's nose is. 
        """
        self.is_calibrated = False

    def on_eye_closed(self, function):
        """
        Override what happens when the user winks.
        Function must be defined and passed as an argument without 
        parenthesis. Example:
        def myFunction: 
            pass
        HeadMouse.on_eye_closed(myFunction)
        """
        self.wink_function = function

    def on_mouth_twitched(self, function):
        """
        Override what happens when the user winks.
        Function must be defined and passed as an argument without 
        parenthesis. Example:
        def myFunction: 
            pass
        HeadMouse.on_mouth_twitched(myFunction)
        """
        self.mouth_twitched_function = function

    def override_controller(self, controller: AbstractController_):
        """
        Controller must be an object of a class that implements the
        AbstractController interface.
        """
        if not isinstance(controller, AbstractController):
            raise Exception("controller object must implement AbstractController interface")
        self.controller = controller

    def _mouth_processing(self, landmarks):
        """
        rcp: right corner points
        rel: relative
        """
        if self.use_mouth_twitch:
            self.mouth_right_corner = landmarks[self.mouth_right_points]
            right_corner_position = self.mouth_right_corner[0]
            rcp_x = right_corner_position[:, 0]
            rcp_y = right_corner_position[:, 1]
            rel_rcp_x = int(rcp_x - self.nose_x)
            rel_rcp_y = int(self.nose_y - rcp_y)
            print(rel_rcp_x, rel_rcp_y)
            if self.prev_mouth_position[0] not in range(rel_rcp_x - 2, rel_rcp_y + 2):
                if self.mouth_twitched_function is not None:
                    self.mouth_twitched_function()
                else:
                    self.controller.mouth_twitch()
                self.prev_mouth_position[0] = rel_rcp_x

    def _update_position(self):
        rel_x_mov = self.coef_sens * (self.nose_x - self.center[0])
        rel_y_mov = self.coef_sens * (self.nose_y - self.center[1])
        #right
        if rel_x_mov > self.thresh_x:
            self.controller.right(self.nose_x, self.center)
        #left
        if rel_x_mov < -self.thresh_x:
            self.controller.left(self.nose_x, self.center)
        #down
        if rel_y_mov > self.thresh_y:
            self.controller.down(self.nose_y, self.center)
        #up
        if rel_y_mov < -self.thresh_y:
            self.controller.up(self.nose_y, self.center)

    def _eye_processing(self, landmarks):
        """
        ear: eye aspect ratio
        """
        self.eye = landmarks[self.eye_points]
        ear = eye_aspect_ratio(self.eye)
        if ear < self.ear_thresh:
            self.eye_counter += 1
        else:
            if self.eye_counter >= self.ear_consec_frames:
                if self.wink_function is not None:
                    self.wink_function()
                else:
                    self.controller.wink()
            self.eye_counter = 0

    def _update_nose_position(self, landmarks):
        nose = landmarks[self.nose_point]
        nose_position = nose[0]
        self.nose_x = nose_position[:, 0]
        self.nose_y = nose_position[:, 1]

    def show_image(self):
        cv2.imshow('My window', self.frame)

    def destroy_window(self):
        cv2.destroyAllWindows()

    def update_threshold(self, value_x, value_y):
        """
        Defines how much the user has to move from the reference
        point for the movement to be valid
        """
        self.thresh_x = value_x
        self.thresh_y = value_y
