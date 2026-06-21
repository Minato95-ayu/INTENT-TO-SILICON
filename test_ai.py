import os
import shutil

# Copy packages
shutil.copytree('official_packages/aayu-dataframe', 'apm-test/.aayu/packages/dataframe', dirs_exist_ok=True)
shutil.copytree('official_packages/aayu-rag', 'apm-test/.aayu/packages/rag', dirs_exist_ok=True)

# Create dummy students.csv
with open('apm-test/students.csv', 'w', encoding='utf-8') as f:
    f.write("name,age,grade\nAlice,20,A\nBob,21,B\nCharlie,19,A\n")

# Write main.aayu
with open('apm-test/main_ai.aayu', 'w', encoding='utf-8') as f:
    f.write('''use dataframe.
use rag.

task main.
    # Test Dataframe
    data is read_csv("students.csv").
    first_row is get 0 from data.
    name is get "name" from first_row.

    # Test RAG
    run add_document with "AAYU is a new language.".
    run add_document with "Python is an old language.".
    ans is search("What is AAYU?").
    
    return ans.
end.
''')
