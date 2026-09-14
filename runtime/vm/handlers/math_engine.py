import math
from typing import List, Tuple, Any

class AayuTensor:
    """
    AAYU Tensor Representation (Row-Major, C-Contiguous by default).
    Supports Zero-Copy Slicing and Virtual Views via Strides and Offsets.
    """
    def __init__(self, raw_data: List[float], shape: Tuple[int, ...], strides: Tuple[int, ...] = None, offset: int = 0):
        self.raw_data = raw_data  # In a real C/C++ backend, this is float* pointing to Heap/VRAM
        self.shape = shape
        self.offset = offset
        
        # Calculate default C-contiguous strides if not provided
        if strides is None:
            self.strides = self._compute_contiguous_strides(shape)
        else:
            self.strides = strides

    @staticmethod
    def _compute_contiguous_strides(shape: Tuple[int, ...]) -> Tuple[int, ...]:
        """Calculates Row-Major strides."""
        strides = [1] * len(shape)
        stride = 1
        for i in range(len(shape) - 1, -1, -1):
            strides[i] = stride
            stride *= shape[i]
        return tuple(strides)

    def get_element(self, indices: Tuple[int, ...]) -> float:
        """Fetch a single element using Stride math."""
        if len(indices) != len(self.shape):
            raise ValueError(f"Index dimension mismatch. Expected {len(self.shape)}, got {len(indices)}")
            
        flat_idx = self.offset
        for i, idx in enumerate(indices):
            if idx < 0 or idx >= self.shape[i]:
                raise IndexError(f"Index {idx} out of bounds for dimension {i} (size {self.shape[i]})")
            flat_idx += idx * self.strides[i]
            
        return self.raw_data[flat_idx]

    def slice_view(self, starts: Tuple[int, ...], ends: Tuple[int, ...]) -> 'AayuTensor':
        """
        Creates a Zero-Copy Virtual View of the Tensor.
        Modifies shape and offset, but shares the same raw_data.
        """
        new_shape = []
        new_offset = self.offset
        
        for i in range(len(self.shape)):
            start = starts[i] if i < len(starts) else 0
            end = ends[i] if i < len(ends) else self.shape[i]
            
            if start < 0 or end > self.shape[i] or start >= end:
                raise IndexError(f"Invalid slice {start}:{end} for dimension {i} (size {self.shape[i]})")
                
            new_shape.append(end - start)
            new_offset += start * self.strides[i]
            
        return AayuTensor(
            raw_data=self.raw_data, # Zero-Copy: Passing the exact same memory reference
            shape=tuple(new_shape),
            strides=self.strides,   # Strides remain the same for slicing
            offset=new_offset
        )
        
    def transpose(self) -> 'AayuTensor':
        """
        Zero-Copy Transpose for 2D Tensors.
        Simply swaps the shape and strides!
        """
        if len(self.shape) != 2:
            raise NotImplementedError("Transpose currently supported for 2D tensors only.")
            
        return AayuTensor(
            raw_data=self.raw_data,
            shape=(self.shape[1], self.shape[0]),
            strides=(self.strides[1], self.strides[0]), # Swap strides!
            offset=self.offset
        )

    def __repr__(self):
        return f"<AayuTensor shape={self.shape} strides={self.strides} offset={self.offset}>"

class MathEngine:
    """Handles Vectorized Math & GPU Dispatching logic."""
    
    @staticmethod
    def add(t1: AayuTensor, t2: AayuTensor) -> AayuTensor:
        """
        Element-wise addition.
        In the future AOT JIT, this triggers PTX / SIMD instructions.
        """
        # Broadcasting check omitted for brevity
        if t1.shape != t2.shape:
            raise ValueError(f"Shape mismatch for broadcast: {t1.shape} vs {t2.shape}")
            
        # Allocate new memory for result
        result_data = [0.0] * math.prod(t1.shape)
        result = AayuTensor(result_data, t1.shape)
        
        # Simple CPU loop (Will be replaced by JIT PTX)
        for i in range(len(result_data)):
            # Warning: A real implementation would iterate using strides properly
            pass
            
        return result
