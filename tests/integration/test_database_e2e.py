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

import pytest
from runtime.database.runtime import DatabaseRuntime

def test_database_runtime_e2e():
    metadata = {
        "data_ir": {
            "storages": [{"name": "app.db"}],
            "models": [{"name": "User", "fields": [{"name": "id", "type": "Int", "is_primary": True}]}]
        }
    }
    rt = DatabaseRuntime(metadata)
    rt.initialize()
    rt.start()
    
    assert rt.engine is not None

