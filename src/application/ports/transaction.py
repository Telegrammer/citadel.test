from abc import ABC, abstractmethod


class Transaction(ABC):

    @abstractmethod
    async def complete(self): ...

    @abstractmethod
    async def cancel(self): ...
