"""Gerenciamento de configuração do ytmusic-dl."""
import json
import os
from pathlib import Path

CONFIG_DIR = Path(os.path.expanduser("~/.config/ytmusic-dl"))
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "music_dir": os.path.expanduser("~/storage/music"),
    "audio_format": "mp3",
    "audio_quality": "0",
    "player_client": "tv_embedded",
    "sleep_interval": 2,
    "max_sleep_interval": 5,
    "playlists": [],
}


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return dict(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    merged = dict(DEFAULT_CONFIG)
    merged.update(data)
    return merged


def save_config(cfg: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def add_playlist(url: str, name: str | None = None) -> dict:
    cfg = load_config()
    entry = {"url": url, "name": name or url}
    if any(p["url"] == url for p in cfg["playlists"]):
        return cfg
    cfg["playlists"].append(entry)
    save_config(cfg)
    return cfg


def remove_playlist(url: str) -> dict:
    cfg = load_config()
    cfg["playlists"] = [p for p in cfg["playlists"] if p["url"] != url]
    save_config(cfg)
    return cfg
