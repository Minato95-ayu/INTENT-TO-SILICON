import time
import logging
from typing import Any, Dict
from .registry import RuntimeRegistry
from .bus import EventBus
from .interface import DispatchResult

logger = logging.getLogger("aayu.kernel")

class RuntimeKernel:
    """
    The AAYU Operating System Kernel.
    Orchestrates plugins, dependencies, booting, and event dispatching.
    """
    def __init__(self):
        self.registry = RuntimeRegistry()
        self.bus = EventBus()
        self._booted = False

    def boot(self) -> None:
        """
        Initializes and starts all registered runtimes in topological order.
        """
        logger.info("Kernel: Booting OS...")
        boot_order = self.registry.get_boot_order()
        
        # Step 1: Initialize (Dependency Injection)
        for plugin in boot_order:
            meta = plugin.metadata()
            try:
                plugin.initialize(self)
                logger.debug(f"Initialized {meta.name}")
            except Exception as e:
                logger.error(f"Kernel: Failed to initialize {meta.name}: {e}", exc_info=True)
                
        # Step 2: Start
        for plugin in boot_order:
            meta = plugin.metadata()
            try:
                plugin.start()
                logger.info(f"Started {meta.name} v{meta.version}")
            except Exception as e:
                logger.error(f"Kernel: Failed to start {meta.name}: {e}", exc_info=True)
                
        self._booted = True
        logger.info("Kernel: OS Boot Complete.")

    def dispatch(self, target: str, action: str, payload: Dict[str, Any]) -> DispatchResult:
        """
        Dispatch an action to a specific runtime target.
        """
        start_time = time.time()
        plugin = self.registry.get(target)
        if not plugin:
            err = f"Target runtime '{target}' not found."
            logger.error(f"Kernel Dispatch Error: {err}")
            return DispatchResult(success=False, error=err, time=time.time() - start_time)
        
        try:
            result = plugin.handle(action, payload)
            if result is None:
                raise ValueError("Runtime handle() must return a DispatchResult.")
            result.time = time.time() - start_time
            return result
        except Exception as e:
            logger.error(f"Kernel: Dispatch crash in '{target}' handling '{action}': {e}", exc_info=True)
            return DispatchResult(success=False, error=str(e), time=time.time() - start_time)

    def shutdown(self) -> None:
        """
        Gracefully shuts down all plugins in reverse boot order.
        """
        logger.info("Kernel: Initiating OS Shutdown...")
        shutdown_order = list(reversed(self.registry.get_boot_order()))
        
        # Step 1: Stop accepting new requests
        for plugin in shutdown_order:
            try:
                plugin.stop()
            except Exception as e:
                logger.error(f"Kernel: Error stopping {plugin.metadata().name}: {e}", exc_info=True)
                
        # Step 2: Full shutdown/resource release
        for plugin in shutdown_order:
            try:
                plugin.shutdown()
                logger.info(f"Shut down {plugin.metadata().name}")
            except Exception as e:
                logger.error(f"Kernel: Error during shutdown of {plugin.metadata().name}: {e}", exc_info=True)
                
        self._booted = False
        logger.info("Kernel: OS Shutdown Complete.")
