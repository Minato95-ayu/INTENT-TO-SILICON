"""
AAYU Runtime — Health & Metrics Endpoint
Provides /health and /metrics endpoints for production monitoring.
"""

import time
import json
import platform
import sys


class HealthEndpoint:
    """
    Production health and metrics endpoint for AAYU applications.

    Provides:
    - /health — Simple health check (200 OK if service is running)
    - /metrics — Prometheus-compatible metrics output

    Usage in the AAYU HTTP pipeline:
        health = HealthEndpoint(vm, api_router)
        # Register in router or handle in request handler
    """

    def __init__(self, vm=None, api_router=None):
        self.vm = vm
        self.api_router = api_router
        self._start_time = time.time()

    def health_check(self):
        """
        Simple health check response.

        Returns:
            dict: Health status with basic system info.
        """
        return {
            "status": "healthy",
            "service": "aayu-runtime",
            "uptime_seconds": round(time.time() - self._start_time, 2),
            "python_version": platform.python_version(),
            "platform": platform.system(),
        }

    def metrics(self):
        """
        Detailed metrics for monitoring.

        Returns dict with:
        - Process metrics (uptime, memory, python version)
        - HTTP metrics (request counts, error rates) from APIRouter
        - Database metrics (if available)
        - VM metrics (if available)
        """
        metrics = {
            "process": {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "python_version": platform.python_version(),
                "platform": f"{platform.system()} {platform.release()}",
            },
        }

        # HTTP metrics from APIRouter
        if self.api_router and hasattr(self.api_router, 'metrics_snapshot'):
            metrics["http"] = self.api_router.metrics_snapshot()

        # VM metrics
        if self.vm:
            vm_metrics = {}
            if hasattr(self.vm, 'interpreter') and self.vm.interpreter:
                interp = self.vm.interpreter
                if hasattr(interp, 'instruction_count'):
                    vm_metrics["instructions_executed"] = interp.instruction_count
            if hasattr(self.vm, 'database') and self.vm.database:
                vm_metrics["database_connected"] = True
            metrics["vm"] = vm_metrics

        return metrics

    def prometheus_format(self):
        """
        Output metrics in Prometheus text exposition format.

        Returns:
            str: Prometheus-compatible metrics text.
        """
        m = self.metrics()
        lines = []

        # Process metrics
        lines.append(f'# HELP aayu_uptime_seconds Time since process start')
        lines.append(f'# TYPE aayu_uptime_seconds gauge')
        lines.append(f'aayu_uptime_seconds {m["process"]["uptime_seconds"]}')

        # HTTP metrics
        if "http" in m:
            http = m["http"]
            lines.append(f'# HELP aayu_http_requests_total Total HTTP requests')
            lines.append(f'# TYPE aayu_http_requests_total counter')
            lines.append(f'aayu_http_requests_total {http.get("requests_total", 0)}')

            lines.append(f'# HELP aayu_http_responses HTTP responses by status class')
            lines.append(f'# TYPE aayu_http_responses counter')
            lines.append(f'aayu_http_responses{{status="2xx"}} {http.get("responses_2xx", 0)}')
            lines.append(f'aayu_http_responses{{status="4xx"}} {http.get("responses_4xx", 0)}')
            lines.append(f'aayu_http_responses{{status="5xx"}} {http.get("responses_5xx", 0)}')

            lines.append(f'# HELP aayu_rate_limit_clients Number of tracked rate limit clients')
            lines.append(f'# TYPE aayu_rate_limit_clients gauge')
            lines.append(f'aayu_rate_limit_clients {http.get("rate_limit_clients", 0)}')

        return "\n".join(lines) + "\n"
