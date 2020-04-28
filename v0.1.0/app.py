from sgtk.platform import Application

class AssetRenameFilterApp(Application):
    def init_app(self):
        app_payload = self.import_module("app")
        menu_callback = lambda: app_payload.dialog.show_dialog(self)
        self.engine.register_command("Asset Rename Filter App...", menu_callback)