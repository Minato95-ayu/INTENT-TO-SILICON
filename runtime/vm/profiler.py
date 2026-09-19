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

class Profiler:
    __slots__ = ['allocations', 'end_time', 'instruction_count', 'peak_memory_bytes', 'start_time']
    'Collects execution telemetry for benchmarking.'

    def __init__(self):
        self.instruction_count = 0
        self.peak_memory_bytes = 0
        self.allocations = 0
        self.start_time = 0
        self.end_time = 0

    def tick(self, heap_active_bytes=0):
        self.instruction_count += 1
        if heap_active_bytes > self.peak_memory_bytes:
            self.peak_memory_bytes = heap_active_bytes

    def record_allocation(self):
        self.allocations += 1

    def summary(self):
        return {'instructions': self.instruction_count, 'peak_memory': self.peak_memory_bytes, 'allocations': self.allocations, 'time': self.end_time - self.start_time}