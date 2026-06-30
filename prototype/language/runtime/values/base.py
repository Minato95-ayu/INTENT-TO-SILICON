from abc import ABC, abstractmethod
from typing import Any

class RuntimeValue(ABC):
    @abstractmethod
    def type_name(self) -> str:
        pass

    @abstractmethod
    def truthy(self) -> bool:
        pass

    @abstractmethod
    def equals(self, other: 'RuntimeValue') -> bool:
        pass

    def compare(self, other: 'RuntimeValue') -> int:
        raise Exception(f"Cannot compare {self.type_name()} with {other.type_name()}")

    def add(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot add {other.type_name()} to {self.type_name()}")
        
    def sub(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot subtract {other.type_name()} from {self.type_name()}")
        
    def mul(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot multiply {self.type_name()} by {other.type_name()}")
        
    def div(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot divide {self.type_name()} by {other.type_name()}")

    @abstractmethod
    def clone(self) -> 'RuntimeValue':
        pass

    @abstractmethod
    def stringify(self) -> str:
        pass

    @abstractmethod
    def to_python(self) -> Any:
        pass
