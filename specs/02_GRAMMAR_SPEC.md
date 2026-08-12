Specification: 02_GRAMMAR_SPEC.md
Version: 0.1.0
Status:
[x] Draft
[ ] Review
[ ] Frozen
[ ] Deprecated

Owner: Compiler Team
Depends On: 01_LANGUAGE_SPEC
Compiler Version: >=0.5.0
Last Updated: 2026-08-04

---

# 02 Grammar Spec (Frozen)

## Purpose
This document defines the formal grammar, lexical structure, and syntactic rules of the AAYU programming language. All compiler frontends (Lexer and Parser) MUST adhere strictly to these rules.

## Scope
Defines the valid character set, keywords, operators, block scoping (`{ }`), statement termination (`.`), and basic control flow grammar. 

## Definitions
- **Statement:** An imperative command or declaration, ending in a period (`.`).
- **Block:** A scoped collection of statements, bounded by curly braces (`{ }`).
- **Identifier:** A sequence of characters representing a variable, function, or type name.

## Core Mechanics

### 1. Character Set & Encoding
AAYU source code MUST be encoded in UTF-8. 

### 2. Lexical Tokens
- **Identifiers:** Must start with a letter (a-z, A-Z) or underscore (`_`), followed by alphanumeric characters or underscores.
- **Keywords:** Reserved words that cannot be used as identifiers (e.g., `let`, `state`, `task`, `model`, `route`, `page`).
- **Numeric Literals:** 
  - Integer: `[0-9]+`
  - Float: `[0-9]+\.[0-9]+`
- **String Literals:** Enclosed in double quotes (`"..."`). Supports standard escape sequences (`\n`, `\t`, `\"`).
- **Punctuation:**
  - Terminator: `.`
  - Scope: `{`, `}`
  - Grouping: `(`, `)`
  - Parameter mapping: `:`

### 3. Syntax Rules (EBNF Representation)

```ebnf
Program ::= { Statement }
Statement ::= ( Declaration | Assignment | ExpressionStatement | ControlFlow ) "."
Block ::= "{" { Statement } "}"

Declaration ::= "let" Identifier [ "=" Expression ]
              | "state" Identifier [ "=" Expression ]
              | "const" Identifier "=" Expression
              | "task" Identifier "(" [ Parameters ] ")" Block

Assignment ::= Identifier "=" Expression

Expression ::= LogicalOr
LogicalOr ::= LogicalAnd { "or" LogicalAnd }
LogicalAnd ::= Equality { "and" Equality }
Equality ::= Relational { ("==" | "!=") Relational }
Relational ::= Additive { (">" | "<" | ">=" | "<=") Additive }
Additive ::= Multiplicative { ("+" | "-") Multiplicative }
Multiplicative ::= Unary { ("*" | "/" | "%") Unary }

Unary ::= ["-" | "not"] Primary
Primary ::= Identifier | NumericLiteral | StringLiteral | "(" Expression ")" | FunctionCall
```

## Compiler Rules
1. **Rule G.1:** The Lexer MUST reject any source file not encoded in UTF-8.
2. **Rule G.2:** The Parser MUST throw a `SyntaxError` if a statement is not terminated by a period (`.`), unless it is a block declaration where the block itself acts as the terminator boundary.
3. **Rule G.3:** The Parser MUST enforce strict block scoping via `{}`. Indentation is ignored for scoping, though recommended for readability.

## Status Update
- Changed from Draft to **Frozen**. Compiler team is authorized to implement.
