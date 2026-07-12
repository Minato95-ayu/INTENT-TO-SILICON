# aayu-ml

The `aayu-ml` package brings core mathematical and statistical operations natively to the AAYU VM.

## Usage

```aayu
use ml.

task process_data.
    list numbers.
    append 10 to numbers.
    append 20 to numbers.
    append 30 to numbers.
    
    set "average" to ml.mean(numbers).
    show average.
end.
```

## Functions

- `ml.mean(list)`: Returns the statistical mean.
- `ml.median(list)`: Returns the median.
- `ml.std(list)`: Returns the standard deviation.
- `ml.matrix_add(A, B)`: Adds two 2D matrices.
- `ml.matrix_multiply(A, B)`: Multiplies two matrices.
- `ml.linear_regression(x, y)`: Performs linear regression, returning `[m, c]`.
