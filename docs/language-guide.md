# Language Guide

AAYU is a deterministic, strictly-typed language optimized for AI compilation.

## Basic Syntax
All statements must end with a period (.) unless they open a block (e.g., do, has).

`ayu
// Variables
let x: Number = 10.
mut y: Number = 20.

// Functions
fn calculate_total(price: Number, tax: Number) -> Number do
    return price + tax.
end.

// Entities (Data Structures)
entity User has
    id: Number
    name: Text
end.
`\n