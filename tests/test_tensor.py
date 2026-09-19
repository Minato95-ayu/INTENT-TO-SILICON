# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.types.tensor import TensorType
from runtime.vm.handlers.math_engine import AayuTensor

def test_tensor():
    print("--- 1. Testing Broadcasting Rules (Semantic Analyzer Phase) ---")
    t1 = TensorType("Float32", (1000, 1))
    t2 = TensorType("Float32", (1, 500))
    print(f"{t1} + {t2} => Broadcasted Shape: {t1.get_broadcasted_shape(t2)}")
    
    print("\n--- 2. Testing Zero-Copy Tensor (VM / Runtime Phase) ---")
    # Simulate a 3x3 matrix allocated in contiguous 1D memory
    raw_memory = [1.0, 2.0, 3.0, 
                  4.0, 5.0, 6.0, 
                  7.0, 8.0, 9.0]
    
    matrix = AayuTensor(raw_memory, (3, 3))
    print(f"Original Matrix: {matrix}")
    print(f"Element at (1, 2) [Row 1, Col 2]: {matrix.get_element((1, 2))}") # Should be 6.0
    
    print("\n[Zero-Copy Slicing]")
    # Slice the bottom-right 2x2 block
    slice_view = matrix.slice_view(starts=(1, 1), ends=(3, 3))
    print(f"Sliced View: {slice_view}")
    print(f"Element at (0, 0) of Slice (maps to 1,1 of original): {slice_view.get_element((0, 0))}") # Should be 5.0
    print(f"Element at (1, 1) of Slice (maps to 2,2 of original): {slice_view.get_element((1, 1))}") # Should be 9.0
    
    print("\n[Zero-Copy Transpose]")
    transposed = matrix.transpose()
    print(f"Transposed View: {transposed}")
    print(f"Element at (1, 2) of Transposed Matrix (maps to 2,1 of original): {transposed.get_element((1, 2))}") # Should be 8.0

if __name__ == "__main__":
    test_tensor()
