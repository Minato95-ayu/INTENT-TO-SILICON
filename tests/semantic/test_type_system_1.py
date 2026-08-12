import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aayu.compiler.semantic.types import (
    Type, PrimitiveType, UnionType, OptionalType, make_nullable,
    T_INT, T_FLOAT, T_STRING, T_BOOL, T_ANY, T_NULL
)
from aayu.compiler.semantic.type_checker import TypeChecker
from aayu.compiler.semantic.errors import TypeError

class TestTypeSystemChunk1(unittest.TestCase):
    
    def test_primitive_assignability(self):
        # Int -> Int = True
        self.assertTrue(T_INT.is_assignable_to(T_INT))
        # Int -> Float = False
        self.assertFalse(T_INT.is_assignable_to(T_FLOAT))
        # String -> Any = True
        self.assertTrue(T_STRING.is_assignable_to(T_ANY))
        # Any -> Int = False (Assignability is one-way generally, though for runtime Any it might bypass, structurally false)
        self.assertFalse(T_ANY.is_assignable_to(T_INT))
        
    def test_union_assignability(self):
        # Union creation
        u1 = UnionType(T_INT, T_STRING)
        
        # Int -> Int|String = True
        self.assertTrue(T_INT.is_assignable_to(u1))
        # String -> Int|String = True
        self.assertTrue(T_STRING.is_assignable_to(u1))
        # Float -> Int|String = False
        self.assertFalse(T_FLOAT.is_assignable_to(u1))
        
        # Int|String -> Int|String = True
        self.assertTrue(u1.is_assignable_to(u1))
        
        # Int|String -> Int = False
        self.assertFalse(u1.is_assignable_to(T_INT))
        
        # Int|String -> Int|String|Float = True
        u2 = UnionType(T_INT, T_STRING, T_FLOAT)
        self.assertTrue(u1.is_assignable_to(u2))
        
        # Int|String|Float -> Int|String = False
        self.assertFalse(u2.is_assignable_to(u1))
        
    def test_nullable_assignability(self):
        # Int? -> Union<Int, Null>
        nullable_int = make_nullable(T_INT)
        
        # Int -> Int? = True
        self.assertTrue(T_INT.is_assignable_to(nullable_int))
        # Null -> Int? = True
        self.assertTrue(T_NULL.is_assignable_to(nullable_int))
        # Float -> Int? = False
        self.assertFalse(T_FLOAT.is_assignable_to(nullable_int))
        
        # Int? -> Int = False
        self.assertFalse(nullable_int.is_assignable_to(T_INT))
        
    def test_optional_assignability(self):
        opt_int = OptionalType(T_INT)
        
        # Optional<Int> -> Optional<Int> = True
        self.assertTrue(opt_int.is_assignable_to(OptionalType(T_INT)))
        
        # Optional<Int> -> Optional<String> = False
        self.assertFalse(opt_int.is_assignable_to(OptionalType(T_STRING)))
        
        # Int -> Optional<Int> = False (Must be boxed in Some())
        self.assertFalse(T_INT.is_assignable_to(opt_int))

if __name__ == "__main__":
    unittest.main()
