"""Busca e salva letras sincronizadas (.lrc) para os mp3 baixados."""
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import syncedlyrics
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

logger = logging.getLogger("ytmusic.lyrics")

# Termos comuns que atrapalham a busca por letra
JUNK_PATTERNS = [
    r"\(official\s*(video|audio|music\s*video|lyric\s*video)?\)",
    r"\[official\s*(video|audio|music\s*video|lyric\s*video)?\]",
    r"\(lyrics?\)", r"\[lyrics?\]",
    r"\(hd\)", r"\[hd\]", r"\(4k\)", r"\[4k\]",
    r"\bofficial\s*video\b", r"\bofficial\s*audio\b",
    r"\blyric\s*video\b",
    r"\bhq\b",
]
JUNK_RE = re.compile("|".join(JUNK_PATTERNS), re.IGNORECASE)


def clean_query(text: str) -> str:
    text = JUNK_RE.sub("", text)
    text = re.sub(r"\s{2,}", " ", text).strip(" -_")
    return text


def build_search_query(mp3_path: Path) -> str:
    query = mp3_path.stem
    try:
        audio = EasyID3(mp3_path)
        title = audio.get("title", [""])[0]
        artist = audio.get("artist", [""])[0]
        if title:
            query = f"{artist} - {title}" if artist else title
    except Exception:
        pass
    return clean_query(query)


def fetch_lyrics(mp3_path: Path, providers: list[str], retries: int = 2) -> tuple[Path, bool, str]:
    lrc_path = mp3_path.with_suffix(".lrc")
    if lrc_path.exists():
        return mp3_path, True, "já existia"

    query = build_search_query(mp3_path)
    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            lrc = syncedlyrics.search(query, providers=providers)
            if lrc:
                lrc_path.write_text(lrc, encoding="utf-8")
                return mp3_path, True, query
            return mp3_path, False, f"não encontrada ({query})"
        except Exception as e:
            last_error = str(e)
    return mp3_path, False, f"erro após {retries} tentativas: {last_error}"


def fetch_all(music_dir: Path, providers: list[str] | None = None, workers: int = 3) -> None:
    providers = providers or ["Lrclib", "NetEase", "Musixmatch"]
    mp3_files = sorted(music_dir.rglob("*.mp3"))
    logger.info("Encontradas %d músicas.", len(mp3_files))

    if not mp3_files:
        return

    ok, fail = 0, 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(fetch_lyrics, f, providers): f for f in mp3_files}
        for future in as_completed(futures):
            mp3_path, success, info = future.result()
            if success:
                ok += 1
                logger.info("[OK] %s (%s)", mp3_path.name, info)
            else:
                fail += 1
                logger.warning("[FALHOU] %s -> %s", mp3_path.name, info)

    logger.info("Concluído: %d letras salvas/existentes, %d falharam.", ok, fail)
