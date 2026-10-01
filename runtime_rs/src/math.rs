pub mod tensor {
    pub struct Tensor {
        pub shape: Vec<usize>,
        pub data: Vec<f64>,
    }

    impl Tensor {
        pub fn new(shape: Vec<usize>, data: Vec<f64>) -> Self {
            Self { shape, data }
        }
        
        pub fn add(&self, other: &Tensor) -> Option<Tensor> {
            if self.shape != other.shape { return None; }
            let data = self.data.iter().zip(other.data.iter()).map(|(a, b)| a + b).collect();
            Some(Tensor::new(self.shape.clone(), data))
        }

        pub fn matmul(&self, other: &Tensor) -> Option<Tensor> {
            // Simplified MatMul
            if self.shape.len() != 2 || other.shape.len() != 2 { return None; }
            if self.shape[1] != other.shape[0] { return None; }
            
            let m = self.shape[0];
            let k = self.shape[1];
            let n = other.shape[1];
            
            let mut out = vec![0.0; m * n];
            for i in 0..m {
                for j in 0..n {
                    let mut sum = 0.0;
                    for l in 0..k {
                        sum += self.data[i * k + l] * other.data[l * n + j];
                    }
                    out[i * n + j] = sum;
                }
            }
            Some(Tensor::new(vec![m, n], out))
        }
    }
}
