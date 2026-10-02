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

from typing import Any, Dict

class AssetManager:
    """
    Central repository for loading and caching fonts, images, SVG, and other assets.
    """
    def __init__(self):
        self._image_cache: Dict[str, Any] = {}
        self._font_cache: Dict[str, Any] = {}
        
    def load_image(self, path: str) -> Any:
        if path in self._image_cache:
            return self._image_cache[path]
        
        # Skeleton: V2 will load actual bytes via Pillow/Tkinter depending on backend
        image_data = f"[Image: {path}]"
        self._image_cache[path] = image_data
        return image_data
        
    def load_font(self, family: str, source_path: str):
        if family in self._font_cache:
            return
            
        # Skeleton: V2 will load raw .ttf / .otf
        self._font_cache[family] = source_path
