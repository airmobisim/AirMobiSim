from abc import ABC, abstractmethod

class Baseapp(ABC):
    @abstractmethod
    def doSomething(self):
        pass
