use std::time::Instant;

// NaN-boxed value - everything fits in 8 bytes, no enum overhead
#[derive(Clone, Copy)]
struct NanVal(u64);

const TAG_INT: u64 = 0x7FF8_0000_0000_0000;

impl NanVal {
    #[inline(always)]
    fn int(v: i64) -> Self { NanVal(TAG_INT | (v as u64 & 0x0000_FFFF_FFFF_FFFF)) }
    #[inline(always)]
    fn as_int(self) -> i64 { (self.0 & 0x0000_FFFF_FFFF_FFFF) as i64 }
}

fn main() {
    // Method 1: AAYU TurboVM style (bytecode dispatch loop)
    let n = 1_000_000usize;
    
    // Simulate bytecode: PUSH 1, [PUSH 1, ADD] * (n-1), HALT
    let mut bytecode: Vec<u8> = Vec::with_capacity(n * 4 + 5);
    bytecode.extend_from_slice(&[1, 0, 0]); // PUSH_CONST 0
    for _ in 0..n-1 {
        bytecode.extend_from_slice(&[1, 0, 0]); // PUSH_CONST 0
        bytecode.push(0x10); // ADD
    }
    bytecode.push(0); // HALT
    
    let constants = [NanVal::int(1)];
    
    // Hot loop — NaN-boxed, unsafe, zero-alloc
    let mut stack = [NanVal(0); 4096];
    let mut sp: usize = 0;
    let mut ip: usize = 0;
    let bc = bytecode.as_ptr();
    let len = bytecode.len();
    
    let start = Instant::now();
    unsafe {
        loop {
            if ip >= len { break; }
            let op = *bc.add(ip);
            ip += 1;
            match op {
                0 => break,
                1 => {
                    let idx = ((*bc.add(ip) as u16) << 8 | *bc.add(ip+1) as u16) as usize;
                    ip += 2;
                    *stack.get_unchecked_mut(sp) = *constants.get_unchecked(idx);
                    sp += 1;
                }
                0x10 => {
                    sp -= 1;
                    let b = *stack.get_unchecked(sp);
                    sp -= 1;
                    let a = *stack.get_unchecked(sp);
                    *stack.get_unchecked_mut(sp) = NanVal::int(a.as_int() + b.as_int());
                    sp += 1;
                }
                _ => {}
            }
        }
    }
    let d = start.elapsed();
    let result = stack[sp-1].as_int();
    println!("NaN-boxed VM  1M adds: {} in {:?}", result, d);
    
    // Method 2: Pure Rust loop (ceiling)
    let start = Instant::now();
    let mut total: i64 = 0;
    for _ in 0..n { total += 1; }
    // prevent optimization
    println!("Rust native   1M adds: {} in {:?}", total, start.elapsed());
    
    // Method 3: Volatile (can't be optimized away)
    let start = Instant::now();
    let mut total: i64 = 0;
    for _ in 0..n {
        unsafe { std::ptr::write_volatile(&mut total, total + 1); }
    }
    let d3 = start.elapsed();
    println!("Rust volatile 1M adds: {} in {:?}", total, d3);
}
