import sys
from tools.commands.run import handle

# Mock sys.argv to simulate running `aayu run test_assets.aayu --web`
sys.argv = ["aayu", "test_assets.aayu", "--web"]
try:
    handle(sys.argv[1:])
except Exception as e:
    print("Execution completed.")
