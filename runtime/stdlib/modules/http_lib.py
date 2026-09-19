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

"""
HTTP Module for AAYU Standard Library
Provides HTTP.get() and HTTP.post() using the standard async calling convention.
"""
import json
import urllib.request
import urllib.error

def http_get(args, vm):
    if not args: return None
    url = args[0]
    if hasattr(url, 'stringify'): url = url.stringify()
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AAYU-VM/1.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
    except Exception as e:
        raise Exception(f"HTTP request failed: {e}")

def http_post(args, vm):
    if len(args) < 2: return None
    url = args[0]
    if hasattr(url, 'stringify'): url = url.stringify()
    
    body = args[1]
    if hasattr(body, 'stringify'): body = body.stringify()
    
    if isinstance(body, dict) or isinstance(body, list):
        body_data = json.dumps(body).encode('utf-8')
    else:
        body_data = str(body).encode('utf-8')
        
    try:
        req = urllib.request.Request(url, data=body_data, headers={'User-Agent': 'AAYU-VM/1.0', 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
    except Exception as e:
        raise Exception(f"HTTP request failed: {e}")

def register_http_lib(registry):
    registry.register('HTTP.get', http_get)
    registry.register('HTTP.post', http_post)
    registry.register('http::get', http_get)
    registry.register('http::post', http_post)

