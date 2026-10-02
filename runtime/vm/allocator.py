# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

class ObjectPool:
    __slots__ = ['next_ptr', 'pool']
    'Manages the raw memory allocation for VM objects.'

    def __init__(self):
        self.pool = {}
        self.next_ptr = 1

    def allocate(self, obj_type, value):
        ptr = self.next_ptr
        self.next_ptr += 1
        self.pool[ptr] = {'type': obj_type, 'value': value, 'ref_count': 0}
        return ptr

    def free(self, ptr):
        if ptr in self.pool:
            del self.pool[ptr]

    def get(self, ptr):
        return self.pool.get(ptr)

class Allocator:
    __slots__ = ['pool']

    def __init__(self):
        self.pool = ObjectPool()

    def alloc_string(self, val: str) -> int:
        return self.pool.allocate('string', val)

    def alloc_int(self, val: int) -> int:
        return self.pool.allocate('int', val)

    def alloc_widget(self, w_type: str, props: dict) -> int:
        return self.pool.allocate('widget', {'type': w_type, 'props': props, 'children': []})