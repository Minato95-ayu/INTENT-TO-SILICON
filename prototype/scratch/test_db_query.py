import sys
import os
import threading
import time
import urllib.request

# Add prototype and aayu_language to sys.path
prototype_dir = r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype"
sys.path.append(prototype_dir)
sys.path.append(os.path.join(prototype_dir, "aayu_language"))

from vm import VirtualMachine
from serializer import deserialize

def run_test():
    # Load the compiled bytecode
    ayc_path = os.path.join(prototype_dir, "scratch", "test_db_query.ayc")
    with open(ayc_path, 'r', encoding='utf-8') as f:
        serialized = f.read()
    bytecode = deserialize(serialized)

    vm = VirtualMachine()

    # Start VM in a separate thread because serve_forever blocks
    def start_vm():
        vm.run(bytecode)

    t = threading.Thread(target=start_vm, daemon=True)
    t.start()

    # Give the server 1 second to start up
    time.sleep(1.0)

    try:
        print("Sending request to http://localhost:8099/test ...")
        response = urllib.request.urlopen("http://localhost:8099/test", timeout=3)
        html = response.read().decode('utf-8')
        print("Response received:")
        print(html)
    except Exception as e:
        print(f"Request failed: {e}")
    finally:
        # Programmatically shut down the server
        if hasattr(vm, "http_server") and vm.http_server:
            print("Shutting down VM HTTP server...")
            vm.http_server.shutdown()
            vm.http_server.server_close()
        t.join(timeout=2.0)
        print("Done!")

if __name__ == "__main__":
    run_test()
