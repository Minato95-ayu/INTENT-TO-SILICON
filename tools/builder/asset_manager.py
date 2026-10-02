class AssetManager:
    """Bundles user assets (images, fonts, themes) for the build."""
    def __init__(self):
        self.bundled_assets = []
        
    def bundle(self):
        print("[Builder] Bundling assets (images/, fonts/, themes/)...")
        # In a real implementation, copy these directories into build/dist/assets
        self.bundled_assets = ["images", "fonts", "themes", "aayu.json"]
        
    def get_asset_paths(self):
        return self.bundled_assets
