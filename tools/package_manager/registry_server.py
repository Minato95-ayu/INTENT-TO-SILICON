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

import os
import json
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

app = FastAPI(title="AAYU Self-Hosted Package Registry")
REGISTRY_DIR = os.path.expanduser("~/.aayu_registry_data")
os.makedirs(REGISTRY_DIR, exist_ok=True)

def get_pkg_dir(name: str):
    d = os.path.join(REGISTRY_DIR, name)
    os.makedirs(d, exist_ok=True)
    return d

@app.get("/search")
async def search(q: str = ""):
    results = []
    for pkg_name in os.listdir(REGISTRY_DIR):
        if q.lower() in pkg_name.lower() or not q:
            meta_path = os.path.join(get_pkg_dir(pkg_name), "meta.json")
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as f:
                    results.append(json.load(f))
    return JSONResponse(content=results)

@app.get("/manifest/{pkg_name}")
async def get_manifest(pkg_name: str):
    meta_path = os.path.join(get_pkg_dir(pkg_name), "meta.json")
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=404, detail="Package not found")
    with open(meta_path, 'r') as f:
        return JSONResponse(content=json.load(f))

@app.get("/download/{pkg_name}/{version}")
async def download(pkg_name: str, version: str):
    pkg_file = os.path.join(get_pkg_dir(pkg_name), f"{version}.zip")
    if not os.path.exists(pkg_file):
        raise HTTPException(status_code=404, detail="Version not found")
    return FileResponse(path=pkg_file, filename=f"{pkg_name}-{version}.zip", media_type="application/zip")

@app.post("/publish")
async def publish(manifest: str = Form(...), file: UploadFile = File(...)):
    manifest_data = json.loads(manifest)
    name = manifest_data["name"]
    version = manifest_data["version"]
    
    pkg_dir = get_pkg_dir(name)
    meta_path = os.path.join(pkg_dir, "meta.json")
    
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            meta = json.load(f)
            
    meta["name"] = name
    meta["description"] = manifest_data.get("description", "")
    meta["owner"] = manifest_data.get("author", "unknown")
    if "versions" not in meta:
        meta["versions"] = {}
        
    meta["versions"][version] = {
        "checksum": manifest_data.get("checksum", ""),
        "dependencies": manifest_data.get("dependencies", {})
    }
    
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
        
    dest_zip = os.path.join(pkg_dir, f"{version}.zip")
    with open(dest_zip, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return JSONResponse(content={"status": "success", "package": name, "version": version})

def start_server(port: int = 5000):
    print(f"\n=========================================")
    print(f"AAYU Self-Hosted Registry started!")
    print(f"Data directory: {REGISTRY_DIR}")
    print(f"API Endpoint: http://localhost:{port}")
    print(f"=========================================\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
