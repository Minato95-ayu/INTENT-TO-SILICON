def generate_diagnostics(document):
    """Extracts diagnostics stored on the Document during parsing."""
    if not document:
        return []
    return document.diagnostics
