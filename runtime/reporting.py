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

import logging
import json
import threading

logger = logging.getLogger("aayu.reporting")

class ExceptionAggregator:
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.lock = threading.Lock()
        self.errors = []
        
    def report(self, exception_obj):
        with self.lock:
            # Aggregate based on exception properties (stacktrace/message)
            if hasattr(exception_obj, "to_dict"):
                err_data = exception_obj.to_dict()
            else:
                err_data = {"type": type(exception_obj).__name__, "message": str(exception_obj)}
                
            self.errors.append(err_data)
            logger.error("AAYU Exception Reported", extra={"aayu_error": err_data})
            
    def get_summary(self):
        with self.lock:
            return list(self.errors)
