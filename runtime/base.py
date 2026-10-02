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

from typing import Dict, Any

class BaseRuntime:
    """
    The base class for all AAYU Native Runtimes.
    All runtimes (HTTP, UI, Database, FileSystem) must implement this interface.
    """
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata

    def initialize(self):
        """
        Called to prepare the runtime (e.g., connect to DB, parse routes).
        """
        pass

    def start(self):
        """
        Called to start the runtime (e.g., spin up a server).
        """
        pass
