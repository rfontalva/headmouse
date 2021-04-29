"""
El módulo HeadMouse pretende ser una herramienta aumentativa, usada para
nivelar las oportunidades de acceso a una computadora para aquellos que no
poseen las habilidades motrices para manejar un mouse.
La herramienta provee una interfaz abriendo la cámara web de la computadora,
mediante la cual se detecta la cara del usuario y se controla el cursor con
la inclinación de la cabeza, tomando la punta de la nariz como referencia.
También puede ser personalizado para disparar funciones distintas al click
cuando el usuario guiña el ojo.

The HeadMouse module is meant to be an augmentative tool, used to level the
opportunities of access to a computer to those without the motor capabilities
to handle a mouse.
The tool provides an interface by opening the web camera and detecting the
user's face to control the mouse by tilting the head using the tip of the
nose as reference.
It can also be customized to trigger different functions instead of a mouse
click when the user winks.
"""

import cv2
import numpy as np
import os
import sys
import dlib
from pynput.mouse import Button, Controller
from HeadMouse_utils import eye_aspect_ratio


class Singleton(type):
    """
    Meteclase, declarada para evitar la creación de dos o más objetos de la clase
    HeadMouse, dado que la camara es un recurso que no puede ser compartido y esto 
    dispararía un error.

    Metaclass, declared to prevent the creation of two or more objects of the 
    HeadMouse class, since the camera resource can't be shared and this would 
    trigger an error.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HeadMouse(object, metaclass=Singleton):
    """
    Parameters:
    is_right (bool): Determina a que ojo se le asignará el comando de guiño.
    use_mouth_twitch (bool): Determina si se evaluarán o no los movimientos
    de la boca.
    sensitivity (int): Determina la velocidad y precisión con la cual se
    moverá el cursor.

    is_right (bool): Determines which eye will be used to trigger the wink
    command.
    use_mouth_twitch (bool): Determines whether mouth movements will be
    evaluated or not.
    sensitivity (int): Determines how fast and precisely the mouse pointer
    will move, default is 0.3.
    """
    def __init__(self, is_right=True, use_mouth_twitch=False, sensitivity=None):
        dir = os.path.dirname(__file__)
        predictor_path = (f"{dir}/shape_predictor_68_face_landmarks.dat")
        self.detector = dlib.get_frontal_face_detector()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception(f'No camera available')
            sys.exit(1)
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
        """
        Para el uso correcto debe ser llamado por lo menos a la misma frecuencia
        de refresco de la cámara. Setear use_mouse como False permite evaluar el
        resto de funcionalidades sin que el cursor siga el movimiento de la cabeza.

        For the correct use, refresh must be called at least at the same frequency
        at which the web camera refreshes. Setting use_mouse to false allows to test
        the rest of functionalities without having the mouse pointer attached to the
        movement of the users' head.
        """
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
                self.eye_processing(landmarks, use_mouse)
                if use_mouse:
                    self.update_mouse_position()

    def quit(self):
        self.cap.release()

    def calibrate(self):
        """
        La proxima vez que se llame a self.refresh se ajustará el punto de
        referencia desde el cual el usuario mueve el cursor a donde esté en ese
        momento su nariz.

        The next time self.refresh gets called the point of refference from which
        the pointer is moved will be readjusted to where the user nose's is. 
        """
        self.is_calibrated = False

    def on_eye_closed(self, function):
        """
        La función debe definirse y se le pasa como argumento el nombre
        sin parentesis. Ejemplo: 
        def myFunction: 
            pass
        HeadMouse.on_eye_closed(myFunction)
        Strategy pattern para hacer al módulo más versatil.

        Function must be defined and passed as an argument without 
        parenthesis. Example: 
        def myFunction: 
            pass
        HeadMouse.on_eye_closed(myFunction)
        Strategy pattern to make the module more versatile.
        """
        self.function = function

    def on_mouth_twitched(self, function):
        """
        La función debe definirse y se le pasa como argumento el nombre
        sin parentesis. Ejemplo: 
        def myFunction: 
            pass
        HeadMouse.on_mouth_twitched(myFunction)
        Strategy pattern para hacer al módulo más versatil.

        Function must be defined and passed as an argument without 
        parenthesis. Example: 
        def myFunction: 
            pass
        HeadMouse.on_mouth_twitched(myFunction)
        Strategy pattern to make the module more versatile.
        """
        self.mouth_twitched_function = function

    def mouth_processing(self, landmarks):
        """
        Meta: private
        rcp: relative right corner points
        rel: relative
        """
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
            self.mouse.position = (self.mouse.position[0] + self.coef_sens * (
                self.nose_x - self.center[0]), self.mouse.position[1])
        if np.absolute(rel_y_mov) > 2:
            new_mouse_y = self.mouse.position[1] + rel_y_mov
            self.mouse.position = (
                self.mouse.position[0], self.mouse.position[1] + self.coef_sens * (self.nose_y - self.center[1]))

    def eye_processing(self, landmarks, use_mouse):
        """
        Meta: private
        ear: eye aspect ratio
        """
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
