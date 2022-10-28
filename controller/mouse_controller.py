from .abstract_controller import AbstractController
from pynput.mouse import Button, Controller

class MouseController(AbstractController):
    def __init__(self, coef_sens) -> None:
        self.mouse = Controller()
        self.coef_sens = coef_sens

    def left(self, x, center):
        self.mouse.position = (self.mouse.position[0] + self.coef_sens *
            (x - center[0]), self.mouse.position[1])

    def right(self, x, center):
        self.mouse.position = (self.mouse.position[0] + self.coef_sens * (
            x - center[0]), self.mouse.position[1])
        
    def up(self, y, center):
        self.mouse.position = (
            self.mouse.position[0], self.mouse.position[1] + self.coef_sens * (y - center[1]))

    def down(self, y, center):
        self.mouse.position = (self.mouse.position[0], self.mouse.position[1] + self.coef_sens * (y - center[1]))

    def right_wink(self):
        self.mouse.click(Button.left, 1)

    def center(self):
        pass

    def left_wink(self):
        pass

    def mouth_twitch(self):
        pass

    def update_coef_sens(self, value):
        self.coef_sens = value
