class CancellationManager:
    """Manages active requests and supports dropping them to prevent stutter."""
    def __init__(self):
        self._cancelled = set()
        
    def cancel(self, request_id):
        if request_id is not None:
            self._cancelled.add(request_id)
            
    def is_cancelled(self, request_id):
        return request_id in self._cancelled
        
    def check(self, request_id):
        if self.is_cancelled(request_id):
            raise InterruptedError(f"Request {request_id} was cancelled")
