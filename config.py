import json
import logging
import os
import platform

logger = logging.getLogger(__name__)

_SYSTEM = platform.system()


class ConfigManager:
    def __init__(self, app_name="KeyboardEmulator"):
        self.app_name = app_name
        self.path = self._resolve_path()
        self.defaults = {"delay": "3", "speed": "0.05"}

    def _resolve_path(self):
        if _SYSTEM == "Windows":
            base = os.path.join(os.getenv("APPDATA", ""), self.app_name)
        elif _SYSTEM == "Darwin":
            base = os.path.join(os.path.expanduser("~"), "Library", "Application Support", self.app_name)
        else:
            base = os.path.join(os.path.expanduser("~"), ".config", self.app_name)
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, "config.json")

    def load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r") as f:
                    data = json.load(f)
                logger.info("Config loaded: %s", self.path)
                return {**self.defaults, **data}
        except Exception as e:
            logger.warning("Failed to load config: %s", e)
        return dict(self.defaults)

    def save(self, delay, speed):
        try:
            data = {"delay": str(delay), "speed": str(speed)}
            with open(self.path, "w") as f:
                json.dump(data, f)
            logger.info("Config saved: %s", self.path)
        except Exception as e:
            logger.error("Failed to save config: %s", e)
