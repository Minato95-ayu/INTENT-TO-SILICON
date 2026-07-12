"""
AAYU Operating System - Runtime Kernel Core
-------------------------------------------
File: runtime/kernel/core.py

WHY DOES THIS FILE EXIST?
This is the master brain of the AAYU Runtime OS. The AAYU Virtual Machine (VM) executes 
bytecode, but when that bytecode needs to do something "real" (like write to a database, 
draw a UI button, or send an HTTP request), the VM calls the Kernel. The Kernel then 
dispatches that request to the appropriate Plugin (Storage, UI, Web).

WHAT DOES THIS CODE DO?
1. Boot/Shutdown Cascade: It orchestrates the lifecycle of all registered plugins. 
   It ensures they are initialized, booted, and shut down in the correct topological order.
2. Plugin Isolation (The `dispatch` method): This is critical. If the VM asks the 
   Storage plugin to execute a query, and the Storage plugin throws a fatal crash, 
   the Kernel catches it. It logs the crash and returns a clean `DispatchResult` 
   containing the error. The AAYU OS *does not crash*. This is how robust operating 
   systems prevent a single bad app from taking down the whole machine.
"""

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
        WHY SEPARATE initialize() FROM start()?
        Dependency Injection. Phase 1 (initialize) injects the Kernel into all plugins.
        Phase 2 (start) boots them up. If we tried to do this in one pass, a plugin 
        might try to use the Event Bus before all other plugins were registered.
        """
        logger.info("Kernel: Booting OS...")
        boot_order = self.registry.get_boot_order()
        
        # Phase 1: Initialize (Dependency Injection)
        for plugin in boot_order:
            meta = plugin.metadata()
            try:
                plugin.initialize(self)
                logger.debug(f"Initialized {meta.name}")
            except Exception as e:
                logger.error(f"Kernel: Failed to initialize {meta.name}: {e}", exc_info=True)
                
        # Phase 2: Start
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
        e.g., kernel.dispatch(target="storage", action="insert", payload=data)
        
        WHY IS THIS SURROUNDED IN A TRY/CATCH?
        Plugin Isolation. We never trust the plugin's code. If it crashes, we catch 
        the exception, log it, and return a clean failure result.
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
            # We catch ALL exceptions to protect the Kernel
            logger.error(f"Kernel: Dispatch crash in '{target}' handling '{action}': {e}", exc_info=True)
            return DispatchResult(success=False, error=str(e), time=time.time() - start_time)

    def shutdown(self) -> None:
        """
        Gracefully shuts down all plugins in *reverse* boot order.
        WHY REVERSE?
        If 'UI' depends on 'State', we must shut down 'UI' before shutting down 'State'. 
        If we shut down 'State' first, the still-running 'UI' might crash trying to read from it.
        """
        logger.info("Kernel: Initiating OS Shutdown...")
        shutdown_order = list(reversed(self.registry.get_boot_order()))
        
        # Phase 1: Stop accepting new requests (drain)
        for plugin in shutdown_order:
            try:
                plugin.stop()
            except Exception as e:
                logger.error(f"Kernel: Error stopping {plugin.metadata().name}: {e}", exc_info=True)
                
        # Phase 2: Full shutdown/resource release
        for plugin in shutdown_order:
            try:
                plugin.shutdown()
                logger.info(f"Shut down {plugin.metadata().name}")
            except Exception as e:
                logger.error(f"Kernel: Error during shutdown of {plugin.metadata().name}: {e}", exc_info=True)
                
        self._booted = False
        logger.info("Kernel: OS Shutdown Complete.")
