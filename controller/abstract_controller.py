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
    def wink(self, *args, **kwargs):
        pass

    @abstractmethod
    def mouth_twitch(self, *args, **kwargs):
        pass
