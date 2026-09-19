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
AAYU Runtime — Database Backup & Recovery
Provides automated SQLite backup, restore, and WAL configuration.

Uses Python's sqlite3.backup() API for safe online backups without
locking the database during the process.
"""

import os
import sqlite3
import shutil
import time
from datetime import datetime


class BackupEngine:
    """
    Production-grade backup engine for the AAYU SQLite database.

    Features:
    - Online backup using sqlite3.backup() (no read/write blocking)
    - Timestamped backup files with configurable retention
    - Restore from any backup file
    - WAL mode configuration for concurrent access
    - Vacuum support for database compaction
    """

    def __init__(self, db_path="aayu_data/Main.db", backup_dir="aayu_data/backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def backup(self, label=None):
        """
        Create a full backup of the database.

        Uses sqlite3.backup() for a safe, incremental online backup that
        does not block concurrent reads/writes.

        Args:
            label: Optional human-readable label for the backup file.

        Returns:
            str: Path to the created backup file.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        suffix = f"_{label}" if label else ""
        backup_filename = f"backup_{timestamp}{suffix}.db"
        backup_path = os.path.join(self.backup_dir, backup_filename)

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found: {self.db_path}")

        # Use sqlite3.backup() for safe online backup
        source = sqlite3.connect(self.db_path)
        dest = sqlite3.connect(backup_path)

        try:
            source.backup(dest, pages=100, progress=self._backup_progress)
            print(f"[Backup] Created: {backup_path}")
        finally:
            dest.close()
            source.close()

        return backup_path

    def _backup_progress(self, status, remaining, total):
        """Callback for sqlite3.backup() progress reporting."""
        if total > 0:
            percent = ((total - remaining) / total) * 100
            if remaining == 0:
                print(f"[Backup] Complete: {total} pages copied")

    def restore(self, backup_path):
        """
        Restore the database from a backup file.

        Creates a safety backup of the current database before restoring,
        then copies the backup over the live database.

        Args:
            backup_path: Path to the backup file to restore from.

        Returns:
            str: Path to the safety backup of the pre-restore database.
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        # Safety: backup current DB before overwriting
        safety_path = None
        if os.path.exists(self.db_path):
            safety_path = self.backup(label="pre_restore_safety")
            print(f"[Restore] Safety backup created: {safety_path}")

        # Use sqlite3.backup() for safe restoration
        source = sqlite3.connect(backup_path)
        dest = sqlite3.connect(self.db_path)

        try:
            source.backup(dest)
            print(f"[Restore] Database restored from: {backup_path}")
        finally:
            dest.close()
            source.close()

        return safety_path

    def list_backups(self):
        """
        List all available backup files sorted by creation time.

        Returns:
            list[dict]: Each dict has "path", "filename", "size_bytes", "created_at".
        """
        backups = []
        if not os.path.exists(self.backup_dir):
            return backups

        for filename in sorted(os.listdir(self.backup_dir)):
            if filename.startswith("backup_") and filename.endswith(".db"):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                backups.append({
                    "path": filepath,
                    "filename": filename,
                    "size_bytes": stat.st_size,
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                })

        return backups

    def cleanup(self, keep_latest=5):
        """
        Remove old backups, keeping only the N most recent.

        Args:
            keep_latest: Number of most recent backups to keep.
        """
        backups = self.list_backups()
        if len(backups) <= keep_latest:
            return 0

        # Sort by creation time (oldest first) and remove excess
        to_remove = backups[:-keep_latest]
        removed = 0
        for backup in to_remove:
            try:
                os.remove(backup["path"])
                print(f"[Backup] Cleaned up: {backup['filename']}")
                removed += 1
            except OSError as e:
                print(f"[Backup] Failed to remove {backup['filename']}: {e}")

        return removed

    def vacuum(self):
        """
        Run VACUUM on the database to reclaim unused space and
        defragment the database file.

        Note: VACUUM requires exclusive access and may briefly lock the DB.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("VACUUM;")
            print("[Backup] VACUUM completed — database compacted")
        finally:
            conn.close()

    def configure_wal(self):
        """
        Enable WAL (Write-Ahead Logging) mode for better concurrent
        read/write performance.

        WAL mode allows readers and writers to operate concurrently
        without blocking each other — essential for production use.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            result = conn.execute("PRAGMA journal_mode=WAL;").fetchone()
            print(f"[Backup] Journal mode set to: {result[0]}")
        finally:
            conn.close()

    def integrity_check(self):
        """
        Run SQLite's built-in integrity check on the database.

        Returns:
            bool: True if database passes integrity check.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            result = conn.execute("PRAGMA integrity_check;").fetchone()
            is_ok = result[0] == "ok"
            if is_ok:
                print("[Backup] Integrity check: PASSED")
            else:
                print(f"[Backup] Integrity check: FAILED — {result[0]}")
            return is_ok
        finally:
            conn.close()
