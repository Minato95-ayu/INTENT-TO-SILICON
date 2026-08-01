import time
import logging
import urllib.request
import urllib.error
from typing import Any, Dict
from aayu.runtime.kernel.interface import RuntimeInterface, RuntimeMetadata, DispatchResult

logger = logging.getLogger("aayu.kernel.network")

class NetworkRuntime(RuntimeInterface):
    """
    AAYU OS - Network Runtime Plugin.
    Manages outbound requests via standard library (zero-dependency).
    """
    def __init__(self):
        self.kernel = None

    def metadata(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            name="network",
            version="1.0",
            dependencies=[],
            author="AAYU Core",
            priority=10
        )

    def initialize(self, kernel) -> None:
        self.kernel = kernel

    def boot(self) -> None:
        logger.info("Network Runtime booted")

    def start(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def handle(self, action: str, payload: Dict[str, Any]) -> DispatchResult:
        start_ms = time.time()
        try:
            if action == "request":
                req_obj = payload["request"]
                method = req_obj.get("method", "GET").upper()
                url = req_obj["url"]
                headers = req_obj.get("headers", {})
                body = req_obj.get("body")
                timeout = req_obj.get("timeout", 10)
                
                # Encode body if provided
                data = None
                if body is not None:
                    if isinstance(body, str):
                        data = body.encode('utf-8')
                    else:
                        data = body
                
                req = urllib.request.Request(url, data=data, headers=headers, method=method)
                
                response_obj = {
                    "status": 0,
                    "headers": {},
                    "body": None,
                    "duration": 0,
                    "error": None
                }
                
                req_start = time.time()
                try:
                    with urllib.request.urlopen(req, timeout=timeout) as res:
                        response_obj["status"] = res.status
                        response_obj["headers"] = dict(res.headers)
                        response_obj["body"] = res.read().decode('utf-8')
                except urllib.error.HTTPError as e:
                    response_obj["status"] = e.code
                    response_obj["headers"] = dict(e.headers)
                    response_obj["body"] = e.read().decode('utf-8')
                    response_obj["error"] = str(e)
                except urllib.error.URLError as e:
                    response_obj["error"] = f"Network Error: {e.reason}"
                except TimeoutError:
                    response_obj["error"] = "Timeout Error"
                except Exception as e:
                    response_obj["error"] = str(e)
                finally:
                    response_obj["duration"] = time.time() - req_start
                
                return DispatchResult(success=True, data={"response": response_obj}, time=time.time() - start_ms)

            else:
                raise ValueError(f"Unknown Network action: {action}")

        except Exception as e:
            return DispatchResult(success=False, error=str(e), time=time.time() - start_ms)

    def stop(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health(self) -> dict:
        return {"status": "healthy"}

    def capabilities(self) -> dict:
        return {"actions": ["request"]}
    
    def diagnostics(self) -> dict:
        return {}
