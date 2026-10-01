use std::rc::Rc;
use std::cell::RefCell;

#[derive(Debug, Clone)]
pub struct Tensor {
    pub shape: Vec<usize>,
    pub strides: Vec<usize>,
    pub offset: usize,
    pub data: Rc<RefCell<Vec<f64>>>,
}

impl Tensor {
    pub fn new(shape: Vec<usize>, data: Vec<f64>) -> Self {
        let strides = Self::compute_strides(&shape);
        Self {
            shape,
            strides,
            offset: 0,
            data: Rc::new(RefCell::new(data)),
        }
    }

    fn compute_strides(shape: &[usize]) -> Vec<usize> {
        let mut strides = vec![0; shape.len()];
        let mut current = 1;
        for i in (0..shape.len()).rev() {
            strides[i] = current;
            current *= shape[i];
        }
        strides
    }

    pub fn get_element(&self, indices: &[usize]) -> f64 {
        assert_eq!(indices.len(), self.shape.len(), "Indices length must match shape length");
        let mut idx = self.offset;
        for (i, &index) in indices.iter().enumerate() {
            assert!(index < self.shape[i], "Index out of bounds");
            idx += index * self.strides[i];
        }
        self.data.borrow()[idx]
    }

    pub fn set_element(&self, indices: &[usize], value: f64) {
        assert_eq!(indices.len(), self.shape.len(), "Indices length must match shape length");
        let mut idx = self.offset;
        for (i, &index) in indices.iter().enumerate() {
            assert!(index < self.shape[i], "Index out of bounds");
            idx += index * self.strides[i];
        }
        self.data.borrow_mut()[idx] = value;
    }

    /// Zero-copy slice view
    pub fn slice_view(&self, starts: &[usize], ends: &[usize]) -> Self {
        assert_eq!(starts.len(), self.shape.len());
        assert_eq!(ends.len(), self.shape.len());
        
        let mut new_shape = Vec::new();
        let mut new_offset = self.offset;
        
        for i in 0..self.shape.len() {
            assert!(starts[i] <= ends[i] && ends[i] <= self.shape[i], "Invalid slice bounds");
            new_shape.push(ends[i] - starts[i]);
            new_offset += starts[i] * self.strides[i];
        }

        Self {
            shape: new_shape,
            strides: self.strides.clone(),
            offset: new_offset,
            data: Rc::clone(&self.data),
        }
    }

    /// Zero-copy transpose (swaps last two dimensions)
    pub fn transpose(&self) -> Self {
        assert!(self.shape.len() >= 2, "Cannot transpose tensor with less than 2 dimensions");
        let mut new_shape = self.shape.clone();
        let mut new_strides = self.strides.clone();
        
        let len = new_shape.len();
        new_shape.swap(len - 1, len - 2);
        new_strides.swap(len - 1, len - 2);

        Self {
            shape: new_shape,
            strides: new_strides,
            offset: self.offset,
            data: Rc::clone(&self.data),
        }
    }

    pub fn print(&self) {
        // Simple recursive print for 2D. 
        if self.shape.len() == 2 {
            print!("[");
            for i in 0..self.shape[0] {
                if i > 0 { print!(" "); }
                print!("[");
                for j in 0..self.shape[1] {
                    print!("{:.4}", self.get_element(&[i, j]));
                    if j < self.shape[1] - 1 { print!(", "); }
                }
                print!("]");
                if i < self.shape[0] - 1 { println!(","); }
            }
            println!("]");
        } else {
            println!("Tensor(shape={:?}, offset={})", self.shape, self.offset);
        }
    }
}
