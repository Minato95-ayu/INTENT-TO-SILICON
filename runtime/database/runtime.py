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

from runtime.base import BaseRuntime
from runtime.database.engine import StorageEngine

class DatabaseRuntime(BaseRuntime):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.engine = None

    def initialize(self):
        data_ir = self.metadata.get("data_ir", {})
        
        # Determine adapter, currently fixed to SQLite
        # Note: 'storages' has db info, 'models' has schema info
        self.engine = StorageEngine(data_ir)
        self.engine.initialize()

    def start(self):
        self.engine.start()
