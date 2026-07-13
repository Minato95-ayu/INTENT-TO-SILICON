from tools.lsp.server import LanguageServer

def handle(args):
    server = LanguageServer()
    server.start()
