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
        Validates if this tensor can be broadcasted to the target shape.
        Follows standard NumPy/PyTorch broadcasting rules.
        """
        # Right-align shapes
        ndim = max(len(self.shape), len(target_shape))
        shape1 = (1,) * (ndim - len(self.shape)) + self.shape
        shape2 = (1,) * (ndim - len(target_shape)) + target_shape
        
        for s1, s2 in zip(shape1, shape2):
            if s1 != s2 and s1 != 1 and s2 != 1:
                return False
        return True

    def get_broadcasted_shape(self, other: 'TensorType') -> Tuple[int, ...]:
        """Returns the resulting shape after broadcasting two tensors."""
        if not self.can_broadcast_to(other.shape) and not other.can_broadcast_to(self.shape):
            raise TypeError(f"Cannot broadcast tensors of shapes {self.shape} and {other.shape}")
            
        ndim = max(len(self.shape), len(other.shape))
        shape1 = (1,) * (ndim - len(self.shape)) + self.shape
        shape2 = (1,) * (ndim - len(other.shape)) + other.shape
        
        result_shape = tuple(max(s1, s2) for s1, s2 in zip(shape1, shape2))
        return result_shape

    def __eq__(self, other):
        if not isinstance(other, TensorType):
            return False
        return self.dtype == other.dtype and self.shape == other.shape

    def __repr__(self):
        return f"Tensor[{self.dtype}, {self.shape}]"
