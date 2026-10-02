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

class QueryNode: pass
class InsertNode(QueryNode):
    def __init__(self, model_name, fields):
        self.model_name = model_name
        self.fields = fields
class FindNode(QueryNode):
    def __init__(self, model_name):
        self.model_name = model_name
class UpdateNode(QueryNode):
    def __init__(self, model_name, fields):
        self.model_name = model_name
        self.fields = fields
class DeleteNode(QueryNode):
    def __init__(self, model_name):
        self.model_name = model_name
