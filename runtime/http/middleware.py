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

class MiddlewareBase:
    def process(self, ctx):
        raise NotImplementedError

class MiddlewarePipeline:
    def __init__(self):
        self.middlewares = []

    def add(self, middleware: MiddlewareBase):
        self.middlewares.append(middleware)

    def __iter__(self):
        return iter(self.middlewares)
