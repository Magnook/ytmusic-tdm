"""Download de áudio via yt-dlp, organizado por artista/álbum quando possível."""
import logging
import shutil
import subprocess
from pathlib import Path

logger = logging.getLogger("ytmusic.downloader")


def _check_deps() -> list[str]:
    missing = []
    for tool in ("yt-dlp", "ffmpeg"):
        if shutil.which(tool) is None:
            missing.append(tool)
    return missing


def build_command(url: str, cfg: dict, music_dir: Path) -> list[str]:
    archive_file = music_dir / "archive.txt"
    output_template = str(music_dir / "%(artist,uploader)s/%(title)s.%(ext)s")

    return [
        "yt-dlp",
        "-i",
        "--js-runtimes", "node",
        "--download-archive", str(archive_file),
        "--extractor-args", f"youtube:player_client={cfg['player_client']}",
        "-f", "bestaudio",
        "-x", "--audio-format", cfg["audio_format"],
        "--audio-quality", cfg["audio_quality"],
        "--embed-thumbnail", "--add-metadata",
        "--sleep-interval", str(cfg["sleep_interval"]),
        "--max-sleep-interval", str(cfg["max_sleep_interval"]),
        "-o", output_template,
        url,
    ]


def download_playlist(url: str, cfg: dict) -> bool:
    music_dir = Path(cfg["music_dir"]).expanduser()
    music_dir.mkdir(parents=True, exist_ok=True)

    missing = _check_deps()
    if missing:
        logger.error("Faltando dependências: %s. Rode install.sh primeiro.", ", ".join(missing))
        return False

    cmd = build_command(url, cfg, music_dir)
    logger.info("Baixando: %s", url)
    try:
        result = subprocess.run(cmd, check=False)
    except FileNotFoundError:
        logger.error("yt-dlp não encontrado no PATH.")
        return False

    if result.returncode != 0:
        logger.warning("yt-dlp terminou com código %s para %s (algumas faixas podem ter falhado)", result.returncode, url)
        return False
    return True


def download_all(cfg: dict) -> None:
    if not cfg["playlists"]:
        logger.warning("Nenhuma playlist configurada. Use: ytmusic add-playlist <url>")
        return
    ok, fail = 0, 0
    for entry in cfg["playlists"]:
        success = download_playlist(entry["url"], cfg)
        ok += success
        fail += not success
    logger.info("Concluído: %d playlist(s) ok, %d com erro.", ok, fail)


def download_single(url: str, cfg: dict) -> None:
    download_playlist(url, cfg)
