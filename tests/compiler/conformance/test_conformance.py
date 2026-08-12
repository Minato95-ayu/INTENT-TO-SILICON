import os
import pytest
from pathlib import Path

# We will implement this as we build out the public Compiler API.
# For now, this is the skeleton that discovers the tests.

CONFORMANCE_DIR = Path(__file__).parent
PHASES = [
    "lexer", "parser", "semantic", "hir", "mir", 
    "ssa", "optimizer", "allocation", "lir", "bytecode", "vm"
]

def discover_test_cases():
    cases = []
    for phase in PHASES:
        phase_dir = CONFORMANCE_DIR / phase
        if not phase_dir.exists():
            continue
        
        for file in phase_dir.glob("*.aayu"):
            cases.append((phase, file.name))
    return cases

@pytest.mark.parametrize("phase, file_name", discover_test_cases())
def test_conformance(phase, file_name):
    """
    Executes a conformance test for a given compiler phase.
    """
    source_file = CONFORMANCE_DIR / phase / file_name
    
    # TODO: This will use the new aayu.compiler.api.Compiler to compile up to `phase`.
    # Then it will dump the output and compare it to the `expected.*` file.
    
    # E.g. if phase == "parser", we compile to AST, dump it, and compare to source_file.with_suffix(".expected.ast")
    pass
