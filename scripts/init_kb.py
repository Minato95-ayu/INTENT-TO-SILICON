"""
=============================================================================
FILE: init_kb.py
PURPOSE: Initializes the knowledge base
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles initializes the knowledge base.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import json
import os

kb_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine\knowledge'

files = {
    'entities.json': {'Student': ['Learner', 'Pupil'], 'Teacher': ['Instructor', 'Professor'], 'Course': ['Class', 'Subject']},
    'fields.json': {'age': ['years old'], 'name': ['full name', 'moniker']},
    'relationships.json': {'EnrollsIn': ['takes', 'attends'], 'Teaches': ['instructs', 'leads']},
    'actions.json': {'Create': ['make', 'build', 'add', 'register'], 'Delete': ['remove', 'destroy', 'drop']},
    'constraints.json': {'GreaterThan': ['more than', 'over'], 'LessThan': ['under', 'below']},
    'domains.json': {'Education': ['school', 'university', 'college']},
    'patterns.json': {'CRUD': ['management system', 'manager', 'registry']},
    'verbs.json': {'manage': ['organize', 'handle', 'control']},
    'synonyms.json': {'system': ['app', 'application', 'platform']},
    'stopwords.json': ['a', 'an', 'the', 'is', 'are', 'was', 'were', 'to', 'for', 'with', 'of', 'and', 'or', 'but'],
    'templates.json': {'Record': ['data model', 'entity model']}
}

for filename, content in files.items():
    with open(os.path.join(kb_dir, filename), 'w') as f:
        json.dump(content, f, indent=4)
