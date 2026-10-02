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

class Debugger:
    __slots__ = ['breakpoints', 'vm']
    'Basic debugging utilities for the VM.'

    def __init__(self, vm):
        self.vm = vm
        self.breakpoints = set()

    def add_breakpoint(self, ip: int):
        self.breakpoints.add(ip)

    def check_breakpoint(self):
        if self.vm.registers.ip in self.breakpoints:
            print(f'[DEBUG] Breakpoint hit at IP: {self.vm.registers.ip}')