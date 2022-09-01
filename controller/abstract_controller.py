from abc import ABCMeta, abstractmethod

class AbstractController(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def left(self, *args, **kwargs):
        pass

    @abstractmethod
    def right(self, *args, **kwargs):
        pass

    @abstractmethod
    def up(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def down(self, *args, **kwargs):
        pass

    @abstractmethod
    def center(self, *args, **kwargs):
        pass

    @abstractmethod
    def right_wink(self, *args, **kwargs):
        pass

    @abstractmethod
    def left_wink(self, *args, **kwargs):
        pass

    @abstractmethod
    def mouth_twitch(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_coef_sens(self, *args, **kwargs):
        pass
