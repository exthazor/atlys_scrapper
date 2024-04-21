from abc import ABC, abstractmethod

class NotificationInterface(ABC):
    @abstractmethod
    async def send(self, message: str):
        pass
