import sys

with open('prototype/aayu_language/runtime/stdlib.py', 'a', encoding='utf-8') as f:
    f.write('''
    def http_request(self, options: dict) -> dict:
        import urllib.request
        import urllib.error
        import json
        
        url = options.get("url")
        method = options.get("method", "GET").upper()
        headers = options.get("headers", {})
        body = options.get("body")
        
        if not url:
            raise Exception("http_request requires a 'url'")
            
        req_data = None
        if body is not None:
            if isinstance(body, dict) or isinstance(body, list):
                req_data = json.dumps(body).encode("utf-8")
                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
            else:
                req_data = str(body).encode("utf-8")
                
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        
        status_code = 500
        res_body = ""
        
        try:
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()
                res_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            status_code = e.code
            res_body = e.read().decode("utf-8")
        except Exception as e:
            raise Exception(f"HTTP Request failed: {e}")
            
        # Try parse JSON
        parsed_body = res_body
        try:
            parsed_body = json.loads(res_body)
        except:
            pass
            
        return {
            "status": status_code,
            "body": parsed_body
        }
''')
