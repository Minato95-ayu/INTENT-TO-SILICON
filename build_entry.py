import sys
from tools.cli import main

# Explicitly import all dynamic commands so PyInstaller traces them
import tools.commands.benchmark
import tools.commands.build
import tools.commands.disassemble
import tools.commands.doctor
import tools.commands.explain
import tools.commands.format
import tools.commands.init
import tools.commands.install
import tools.commands.list
import tools.commands.login
import tools.commands.logout
import tools.commands.lsp
import tools.commands.new
import tools.commands.publish
import tools.commands.registry
import tools.commands.remove
import tools.commands.run
import tools.commands.search
import tools.commands.serve
import tools.commands.test
import tools.commands.tree
import tools.commands.update
import tools.commands.version

if __name__ == '__main__':
    sys.exit(main())
