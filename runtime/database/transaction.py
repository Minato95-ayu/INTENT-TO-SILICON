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
AAYU Runtime — Transaction Manager
Provides safe transaction handling with nested savepoint support,
context managers, and automatic rollback on exception.
"""


class TransactionManager:
    """
    Production-grade transaction manager for the AAYU database subsystem.

    Features:
    - Standard BEGIN/COMMIT/ROLLBACK
    - Nested savepoint support (SAVEPOINT sp_N / RELEASE sp_N)
    - Context manager for automatic commit/rollback
    - Transaction depth tracking for nested transactions
    """

    def __init__(self, adapter):
        self.adapter = adapter
        self._depth = 0  # Nesting level — 0 means no active transaction

    @property
    def in_transaction(self):
        """Check if a transaction is currently active."""
        return self._depth > 0

    def begin(self):
        """
        Begin a new transaction or create a savepoint for nesting.

        First call starts a real transaction (BEGIN).
        Subsequent nested calls create savepoints (SAVEPOINT sp_N).
        """
        if self._depth == 0:
            self.adapter.execute_raw("BEGIN TRANSACTION;")
        else:
            self.adapter.execute_raw(f"SAVEPOINT sp_{self._depth};")
        self._depth += 1

    def commit(self):
        """
        Commit the current transaction level.

        For savepoints: releases the savepoint.
        For the outermost transaction: commits to disk.
        """
        if self._depth <= 0:
            raise RuntimeError("Cannot commit — no active transaction")

        self._depth -= 1
        if self._depth == 0:
            self.adapter.execute_raw("COMMIT;")
        else:
            self.adapter.execute_raw(f"RELEASE SAVEPOINT sp_{self._depth};")

    def rollback(self):
        """
        Rollback the current transaction level.

        For savepoints: rolls back to the savepoint.
        For the outermost transaction: rolls back everything.
        """
        if self._depth <= 0:
            raise RuntimeError("Cannot rollback — no active transaction")

        self._depth -= 1
        if self._depth == 0:
            self.adapter.execute_raw("ROLLBACK;")
        else:
            self.adapter.execute_raw(f"ROLLBACK TO SAVEPOINT sp_{self._depth};")

    def atomic(self):
        """
        Context manager for automatic transaction handling.

        Usage:
            with transaction.atomic():
                adapter.execute_raw("INSERT INTO ...")
                adapter.execute_raw("UPDATE ...")
            # Auto-commits on success, auto-rolls back on exception

        Supports nesting — inner atomics use savepoints:
            with transaction.atomic():
                adapter.execute_raw("INSERT INTO users ...")
                with transaction.atomic():
                    adapter.execute_raw("INSERT INTO profiles ...")
                    # If this fails, only the inner savepoint rolls back
        """
        return _AtomicContext(self)


class _AtomicContext:
    """Context manager helper for TransactionManager.atomic()."""

    def __init__(self, manager):
        self.manager = manager

    def __enter__(self):
        self.manager.begin()
        return self.manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Exception occurred — rollback
            self.manager.rollback()
            return False  # Re-raise the exception
        else:
            # Success — commit
            self.manager.commit()
            return False
