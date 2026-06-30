class FreezeGuard:
    def check(self, component: str) -> bool:
        """
        Check if a component is frozen.
        Returns True if ALLOWED to modify, False if FROZEN.
        """
        # MVP: Stub based on PROJECT_SNAPSHOT.md
        frozen_components = ["Lexer", "Parser", "AST", "Compiler", "ISA", "Modules"]
        if component in frozen_components:
            return False
        return True
