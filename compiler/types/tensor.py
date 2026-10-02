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

from typing import Tuple, List

class TensorType:
    """
    Semantic Type representation for AI/ML Tensors in AAYU.
    Tracks dtype (Float32/Float64) and Shape during compilation.
    """
    def __init__(self, dtype: str, shape: Tuple[int, ...]):
        self.dtype = dtype
        self.shape = shape
        self.is_differentiable = False  # Set to true for Requires Grad (Autodiff)

    def can_broadcast_to(self, target_shape: Tuple[int, ...]) -> bool:
        """
        Validates if this tensor can be broadcasted into the target shape.
        E.g., (1, 5) can broadcast to (10, 5), but (10, 5) cannot broadcast to (1, 5).
        """
        if len(self.shape) > len(target_shape):
            return False
            
        # Right-align shapes
        ndim = len(target_shape)
        shape1 = (1,) * (ndim - len(self.shape)) + self.shape
        
        for s1, s2 in zip(shape1, target_shape):
            # To broadcast shape1 to target_shape, dimensions must match, OR shape1's dim must be 1.
            if s1 != s2 and s1 != 1:
                return False
        return True

    def get_broadcasted_shape(self, other: 'TensorType') -> Tuple[int, ...]:
        """Returns the resulting shape after mutually broadcasting two tensors (e.g. for Addition)."""
        ndim = max(len(self.shape), len(other.shape))
        shape1 = (1,) * (ndim - len(self.shape)) + self.shape
        shape2 = (1,) * (ndim - len(other.shape)) + other.shape
        
        for s1, s2 in zip(shape1, shape2):
            if s1 != s2 and s1 != 1 and s2 != 1:
                raise TypeError(f"Cannot mutually broadcast tensors of shapes {self.shape} and {other.shape}")
                
        result_shape = tuple(max(s1, s2) for s1, s2 in zip(shape1, shape2))
        return result_shape

    def __eq__(self, other):
        if not isinstance(other, TensorType):
            return False
        return self.dtype == other.dtype and self.shape == other.shape

    def __repr__(self):
        return f"Tensor[{self.dtype}, {self.shape}]"
