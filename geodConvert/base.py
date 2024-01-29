from abc import ABC, abstractmethod
from dataclasses import dataclass

# @dataclass
# class

class ConversionBase(ABC):
    @abstractmethod
    def reverse(self):
        pass


