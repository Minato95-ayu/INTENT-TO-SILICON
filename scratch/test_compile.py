
import tools.commands.run as run_cmd
import sys

args = ["stthomas_app/app.aayu", "--renderer=web"]
try:
    run_cmd.handle(args)
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()

