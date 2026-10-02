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

import json

class ErrorEngine:
    def handle_404(self, ctx):
        # AAYU Native 404
        ctx.response.status(404).json({"error": "Endpoint not found in AAYU Application IR"})

    def handle_500(self, ctx, exception):
        # AAYU Native 500. We don't expose Python tracebacks to the user.
        print(f"[AAYU Runtime Error] {exception}")
        ctx.response.status(500).json({"error": "Internal Server Error in AAYU Runtime"})
