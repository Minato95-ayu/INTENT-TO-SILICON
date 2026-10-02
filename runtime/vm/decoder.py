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

from runtime.vm.instructions import Opcode

class Decoder:
    __slots__ = ['bytecode', 'constant_pool', 'length']
    'Decodes bytecode stream into instructions.'

    def __init__(self, bytecode, constant_pool):
        self.bytecode = bytecode
        self.constant_pool = constant_pool
        self.length = len(bytecode)

    def fetch8(self, ip: int) -> int:
        if ip >= self.length:
            return Opcode.HALT
        return self.bytecode[ip]

    def fetch16(self, ip: int) -> int:
        if ip + 1 >= self.length:
            return 0
        return self.bytecode[ip] << 8 | self.bytecode[ip + 1]