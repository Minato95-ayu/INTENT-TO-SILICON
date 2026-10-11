fn main() {
    // 10M addition benchmark
    let start = std::time::Instant::now();
    let mut total: i64 = 0;
    for _ in 0..10_000_000 {
        total += 1;
    }
    let d = start.elapsed();
    println!("Rust Native 10M additions: {} in {:?}", total, d);

    // 1M addition benchmark
    let start = std::time::Instant::now();
    let mut total: i64 = 0;
    for _ in 0..1_000_000 {
        total += 1;
    }
    let d = start.elapsed();
    println!("Rust Native 1M additions: {} in {:?}", total, d);
}
