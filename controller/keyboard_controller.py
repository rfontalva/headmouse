from .abstract_controller import AbstractController

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

    def wink(self):
        if self.strategy["type"] == "letters":
            self.strategy = {'type': 'numbers', 'left': '4', 'right': '6', 'up': '8', 'down': '2'}    
        else:
            self.strategy = {'type': 'letters', 'left': 'a', 'right': 'd', 'up': 'w', 'down': 's'}

    def mouth_twitch(self):
        # print("twitch")
        pass
