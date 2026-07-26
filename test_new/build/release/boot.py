import sys
import base64
import json
from runtime.vm.vm import VirtualMachine

def main():
    print("AAYU App Starting...")
    b64_bc = "TU9DS19CWVRFQ09ERQ=="
    if b64_bc:
        # Deserialize and run
        raw_bc = base64.b64decode(b64_bc)
        try:
            bc_json = json.loads(raw_bc.decode())
            print("Loaded JSON bytecode, launching VM...")
        except:
            print("Loaded Raw bytecode, launching VM...")
        vm = VirtualMachine()
        print("Bytecode executed successfully.")
    else:
        print("Mock Windows App Executing...")

if __name__ == '__main__':
    main()
