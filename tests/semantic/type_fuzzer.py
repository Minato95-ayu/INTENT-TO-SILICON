import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aayu.compiler.semantic.types import (
    Type, PrimitiveType, UnionType, OptionalType, make_nullable,
    T_INT, T_FLOAT, T_STRING, T_BOOL, T_CHAR, T_BYTE, T_VOID, T_NEVER, T_ANY, T_NULL
)

PRIMITIVES = [T_INT, T_FLOAT, T_STRING, T_BOOL, T_CHAR, T_BYTE, T_VOID, T_NEVER, T_ANY, T_NULL]

def generate_random_type(depth=0, max_depth=5):
    if depth >= max_depth:
        return random.choice(PRIMITIVES)
        
    choice = random.randint(0, 3)
    if choice == 0:
        return random.choice(PRIMITIVES)
    elif choice == 1:
        # Union
        num_types = random.randint(2, 5)
        types = [generate_random_type(depth + 1, max_depth) for _ in range(num_types)]
        return UnionType(*types)
    elif choice == 2:
        # Optional
        return OptionalType(generate_random_type(depth + 1, max_depth))
    elif choice == 3:
        # Nullable
        return make_nullable(generate_random_type(depth + 1, max_depth))

def run_fuzzer(iterations=10000):
    print(f"Starting Type System Fuzzing: {iterations} random complex types...")
    crashes = 0
    
    for i in range(iterations):
        t1 = generate_random_type(max_depth=5)
        t2 = generate_random_type(max_depth=5)
        
        try:
            # We just want to ensure these operations do not throw an exception or infinite loop
            _ = t1.is_assignable_to(t2)
            _ = t2.is_assignable_to(t1)
            _ = t1 == t2
            _ = hash(t1)
            _ = hash(t2)
            _ = str(t1)
        except Exception as e:
            crashes += 1
            print(f"CRASH ON:\nT1: {t1}\nT2: {t2}\nError: {e}")
            
    print(f"Fuzzing Complete. Crashes: {crashes}")
    with open(os.path.join(os.path.dirname(__file__), "type_fuzzer_report.txt"), "w") as f:
        f.write(str(crashes))
    return crashes == 0

if __name__ == "__main__":
    success = run_fuzzer()
    sys.exit(0 if success else 1)
