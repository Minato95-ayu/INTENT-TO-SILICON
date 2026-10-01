pub mod tensor {
    #[derive(Debug, Clone)]
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

        pub fn dot(&self, other: &Tensor) -> Option<f64> {
            if self.data.len() != other.data.len() { return None; }
            let sum = self.data.iter().zip(other.data.iter()).map(|(a, b)| a * b).sum();
            Some(sum)
        }

        pub fn transpose(&self) -> Option<Tensor> {
            if self.shape.len() != 2 { return None; }
            let m = self.shape[0];
            let n = self.shape[1];
            let mut out = vec![0.0; m * n];
            for i in 0..m {
                for j in 0..n {
                    out[j * m + i] = self.data[i * n + j];
                }
            }
            Some(Tensor::new(vec![n, m], out))
        }
    }

    pub mod nn {
        use super::Tensor;
        
        pub fn relu(tensor: &Tensor) -> Tensor {
            let data = tensor.data.iter().map(|&x| if x > 0.0 { x } else { 0.0 }).collect();
            Tensor::new(tensor.shape.clone(), data)
        }

        pub fn sigmoid(tensor: &Tensor) -> Tensor {
            let data = tensor.data.iter().map(|&x| 1.0 / (1.0 + (-x).exp())).collect();
            Tensor::new(tensor.shape.clone(), data)
        }

        pub struct LlmWeights {
            pub token_embedding_table: Tensor,
            pub wq: Vec<Tensor>,
            pub wk: Vec<Tensor>,
            pub wv: Vec<Tensor>,
            pub wo: Vec<Tensor>,
            pub rms_att_weight: Vec<Tensor>,
            pub w1: Vec<Tensor>,
            pub w2: Vec<Tensor>,
            pub w3: Vec<Tensor>,
            pub rms_ffn_weight: Vec<Tensor>,
            pub rms_final_weight: Tensor,
            pub wcls: Tensor,
        }
    }
}
