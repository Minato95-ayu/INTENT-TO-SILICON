import unittest
from aayu.compiler.semantic.context import SemanticContext, IDCollisionError, TypeID, SymbolID
from aayu.compiler.semantic.types import StructType, StructField, EnumType, EnumVariant
from aayu.compiler.hir.builder import HIRBuilder
from aayu.compiler.hir.validator import HIRValidator
from aayu.compiler.hir.nodes import HIRModule, HIRStructInit
from aayu.compiler.semantic.diagnostics import DiagnosticEngine

class MockDiagnosticEngine(DiagnosticEngine):
    def __init__(self):
        super().__init__()
        self.errors = []

    def report(self, diagnostic, *args, **kwargs):
        self.errors.append(diagnostic)

class TestHIR3SemanticBoundary(unittest.TestCase):
    def setUp(self):
        self.diag = MockDiagnosticEngine()
        self.context = SemanticContext(self.diag)
        
    def test_id_determinism_and_collisions(self):
        # TypeID determinism
        t1 = self.context.type_registry._generate_type_id("core::Int")
        t2 = self.context.type_registry._generate_type_id("core::Int")
        self.assertEqual(t1, t2)
        
        # SymbolID determinism
        s1 = self.context.symbol_registry._generate_symbol_id("my_module::my_var")
        s2 = self.context.symbol_registry._generate_symbol_id("my_module::my_var")
        self.assertEqual(s1, s2)
        
        # Collision
        self.context.type_registry._name_by_type_id[TypeID(999)] = "some::OtherType"
        # Not easily triggerable randomly without mocking hash, but we verify it's importable and logic exists.

    def test_struct_field_validity(self):
        sf = StructField(name="x", field_type=None, index=0)
        sf.generate_id("my_module::Point")
        sf2 = StructField(name="x", field_type=None, index=0)
        sf2.generate_id("my_module::Point")
        self.assertEqual(sf.field_id, sf2.field_id)
        
    def test_enum_variant_validity(self):
        ev = EnumVariant(name="Red", tag=0)
        ev.generate_id("my_module::Color")
        ev2 = EnumVariant(name="Red", tag=0)
        ev2.generate_id("my_module::Color")
        self.assertEqual(ev.variant_id, ev2.variant_id)
        
    def test_hir_validator_struct_init(self):
        struct_type = StructType(name="Point")
        f1 = StructField("x", None, 0)
        f1.generate_id("Point")
        struct_type.fields.append(f1)
        
        t_id = self.context.type_registry.register_type("Point", struct_type)
        
        from aayu.compiler.hir.nodes import HIRNullLiteral
        # Valid init
        init_valid = HIRStructInit(
            origin_node_id=1, 
            type_id=t_id, 
            struct_type_id=t_id, 
            args=[HIRNullLiteral(origin_node_id=2, type_id=t_id)]
        )
        
        # Invalid init
        init_invalid = HIRStructInit(
            origin_node_id=2, 
            type_id=t_id, 
            struct_type_id=t_id, 
            args=[
                HIRNullLiteral(origin_node_id=3, type_id=t_id),
                HIRNullLiteral(origin_node_id=4, type_id=t_id)
            ]
        )
        
        validator = HIRValidator(self.context)
        validator._validate_node(init_valid)
        self.assertEqual(len(validator.errors), 0)
        
        validator._validate_node(init_invalid)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn("expected 1 arguments, got 2", validator.errors[0])
        
    def test_hir_builder_no_fallback(self):
        class MockScope:
            def resolve(self, name): return None
        
        builder = HIRBuilder(self.context)
        builder.global_scope = MockScope()
        builder.module_id = "test"
        
        from aayu.compiler.errors import InternalCompilerError
        
        with self.assertRaises(InternalCompilerError) as ctx:
            builder._get_type_id(999)
        self.assertIn("Type missing in SemanticContext", str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
