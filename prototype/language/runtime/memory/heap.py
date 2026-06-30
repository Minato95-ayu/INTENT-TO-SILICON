from typing import Dict, Any, Optional

class HeapObject:
    def __init__(self, obj_id: int, obj_type: str, payload: Any):
        self.id = obj_id
        self.type = obj_type
        self.payload = payload
        self.ref_count = 0
        self.flags = 0

class Heap:
    def __init__(self):
        self.objects: Dict[int, HeapObject] = {}
        self.next_address = 1
        
    def allocate(self, obj_type: str, payload: Any) -> HeapObject:
        addr = self.next_address
        obj = HeapObject(addr, obj_type, payload)
        self.objects[addr] = obj
        self.next_address += 1
        return obj
        
    def free(self, address: int):
        if address in self.objects:
            del self.objects[address]
            
    def get(self, address: int) -> Optional[HeapObject]:
        return self.objects.get(address)
