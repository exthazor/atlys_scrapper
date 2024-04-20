from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    async def save(self, data):
        pass

    @abstractmethod
    async def load(self):
        pass
