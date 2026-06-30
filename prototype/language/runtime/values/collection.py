from .reference import ReferenceValue
from .base import RuntimeValue
from abc import abstractmethod
from typing import Any

class CollectionValue(ReferenceValue):
    
    @abstractmethod
    def length(self) -> RuntimeValue:
        pass
        
    @abstractmethod
    def get(self, key: RuntimeValue) -> RuntimeValue:
        pass
        
    @abstractmethod
    def set(self, key: RuntimeValue, value: RuntimeValue):
        pass
        
    @abstractmethod
    def append(self, value: RuntimeValue):
        pass
        
    @abstractmethod
    def remove(self, key: RuntimeValue):
        pass
        
    @abstractmethod
    def contains(self, value: RuntimeValue) -> RuntimeValue:
        pass
        
    @abstractmethod
    def iterate(self):
        pass
