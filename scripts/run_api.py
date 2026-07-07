import os
import sys
import uvicorn
sys.path.insert(0, r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype')

from api.main import app

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
