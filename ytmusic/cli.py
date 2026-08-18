"""CLI do ytmusic-dl: baixa músicas do YouTube e busca letras, tudo pelo Termux."""
import argparse
import logging
from pathlib import Path

from . import config as cfgmod
from . import downloader, lyrics


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")


def cmd_download(args) -> None:
    cfg = cfgmod.load_config()
    if args.url:
        downloader.download_single(args.url, cfg)
    else:
        downloader.download_all(cfg)


def cmd_lyrics(args) -> None:
    cfg = cfgmod.load_config()
    music_dir = Path(cfg["music_dir"]).expanduser()
    lyrics.fetch_all(music_dir, workers=args.workers)


def cmd_sync(args) -> None:
    cmd_download(args)
    cmd_lyrics(args)


def cmd_add_playlist(args) -> None:
    cfgmod.add_playlist(args.url, args.name)
    print(f"Playlist adicionada: {args.url}")


def cmd_remove_playlist(args) -> None:
    cfgmod.remove_playlist(args.url)
    print(f"Playlist removida: {args.url}")


def cmd_list_playlists(args) -> None:
    cfg = cfgmod.load_config()
    if not cfg["playlists"]:
        print("Nenhuma playlist configurada.")
        return
    for p in cfg["playlists"]:
        print(f"- {p['name']}: {p['url']}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="ytmusic", description="Baixador de músicas + letras para uso offline no Termux")
    parser.add_argument("-v", "--verbose", action="store_true", help="log detalhado")
    sub = parser.add_subparsers(dest="command", required=True)

    p_dl = sub.add_parser("download", help="baixa playlists configuradas (ou uma URL avulsa)")
    p_dl.add_argument("url", nargs="?", help="URL de playlist/vídeo avulso (opcional)")
    p_dl.set_defaults(func=cmd_download)

    p_ly = sub.add_parser("lyrics", help="busca letras (.lrc) para os mp3 existentes")
    p_ly.add_argument("--workers", type=int, default=3, help="buscas em paralelo (padrão: 3)")
    p_ly.set_defaults(func=cmd_lyrics)

    p_sync = sub.add_parser("sync", help="download + lyrics em sequência")
    p_sync.add_argument("url", nargs="?", default=None)
    p_sync.add_argument("--workers", type=int, default=3)
    p_sync.set_defaults(func=cmd_sync)

    p_add = sub.add_parser("add-playlist", help="salva uma playlist na config")
    p_add.add_argument("url")
    p_add.add_argument("--name", default=None)
    p_add.set_defaults(func=cmd_add_playlist)

    p_rm = sub.add_parser("remove-playlist", help="remove uma playlist da config")
    p_rm.add_argument("url")
    p_rm.set_defaults(func=cmd_remove_playlist)

    p_list = sub.add_parser("list-playlists", help="lista playlists configuradas")
    p_list.set_defaults(func=cmd_list_playlists)

    args = parser.parse_args()
    setup_logging(args.verbose)
    args.func(args)


if __name__ == "__main__":
    main()
