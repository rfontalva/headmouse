from .abstract_controller import AbstractController
from pynput.keyboard import Controller

class KeyboardController(AbstractController):
    def __init__(self) -> None:
        self.keyboard = Controller()
        self.strategy = {'type': 'letters', 'left': 'a', 'right': 'd', 'up': 'w', 'down': 's'}

    def left(self, x, center):
        self.keyboard.press(self.strategy['left'])

    def right(self, x, center):
        self.keyboard.press(self.strategy['right'])
        
    def up(self, y, center):
        self.keyboard.press(self.strategy['up'])

    def down(self, y, center):
        self.keyboard.press(self.strategy['down'])

    def right_wink(self):
        if self.strategy["type"] == "letters":
            self.strategy = {'type': 'numbers', 'left': '4', 'right': '6', 'up': '8', 'down': '2'}    
        else:
            self.strategy = {'type': 'letters', 'left': 'a', 'right': 'd', 'up': 'w', 'down': 's'}

    def center(self):
        pass

    def left_wink(self):
        pass

    def mouth_twitch(self):
        pass

    def update_coef_sens(self):
        pass
