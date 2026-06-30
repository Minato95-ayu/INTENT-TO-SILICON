# Changelog

All notable changes to the AAYU project will be documented in this file.

## [Unreleased]

### Added
- **Phase 5.4: Type Inference**
  - Added local variable type inference in `TypeCheckerPass`.
  - Added function return type inference for functions without explicit return type annotations.
- **Phase 5.3: Type Checker**
  - Added semantic type hierarchy (`AAYUType`, `PrimitiveType`, `AnyType`, `FunctionType`, `VoidType`).
  - Added reserved types `UnknownType` and `ErrorType`.
  - Added type enforcement for assignments, declarations, function returns, and binary expressions.
  - Added `AAYUTypeError` diagnostics (range AAYU2xxx).
- **Phase 5.2: Symbol Types**
  - Added `declared_type` and `resolved_type` properties to `Symbol`.
  - Bound Parser's `TypeNode` instances to symbols in `ScopeBuilderPass`.
- **Phase 5.1: Type AST**
  - Added `TypeNode` hierarchy (`PrimitiveTypeNode`, `NamedTypeNode`, `FunctionTypeNode`).
  - Updated `Parser` to support type annotations.

### Fixed
- Fixed bug where `SourceSpan` was improperly accessed for line numbers in compiler errors.
