# ytmusic-tdm

YouTube Music Terminal Download Manager

Baixador de música do YouTube com letras sincronizadas (.lrc), feito para
rodar 100% no **Termux**, sem depender de nenhum streaming pago. Pensado
para uso com players locais como o [Musicolet](https://play.google.com/store/apps/details?id=in.krosbits.musicolet).

> ⚠️ Uso pessoal: baixe apenas conteúdo que você tem o direito de acessar
> (ex: suas próprias playlists, músicas de artistas que autorizam download,
> conteúdo em domínio público). Respeite os termos de uso do YouTube e os
> direitos autorais dos artistas.

## Funcionalidades

- Baixa playlists inteiras em MP3 (áudio de melhor qualidade), com capa e
  metadados embutidos
- Organiza automaticamente em pastas por artista
- Evita redownload com `archive.txt`
- Busca letras sincronizadas (`.lrc`) em paralelo, com limpeza automática
  de título (remove "(Official Video)", "[Lyrics]" etc. antes de buscar)
- Guarda suas playlists numa config, então basta rodar `ytmusic sync`
  periodicamente

## Instalação (Termux)

```bash
git clone https://github.com/Magnook/ytmusic-tdm.git
cd ytmusic-tdm
bash install.sh
```

## Uso

```bash
# Adicionar playlist(s) à config
ytmusic add-playlist "https://www.youtube.com/playlist?list=PLxxxx" --name "Favoritas"

# Ver playlists configuradas
ytmusic list-playlists

# Baixar tudo que está configurado
ytmusic download

# Baixar uma URL avulsa (sem salvar na config)
ytmusic download "https://www.youtube.com/watch?v=xxxx"

# Buscar letras para os mp3 já baixados
ytmusic lyrics

# Fazer os dois em sequência (rotina de atualização)
ytmusic sync
```

Os arquivos ficam em `~/storage/music/<Artista>/<Música>.mp3` (mesmo
diretório visível pelo Musicolet, se ele estiver configurado para
escanear o armazenamento compartilhado).

## Configuração

A config fica em `~/.config/ytmusic-tdm/config.json`:

```json
{
  "music_dir": "/data/data/com.termux/files/home/storage/music",
  "audio_format": "mp3",
  "audio_quality": "0",
  "player_client": "tv_embedded",
  "sleep_interval": 2,
  "max_sleep_interval": 5,
  "playlists": [
    {"name": "Favoritas", "url": "https://www.youtube.com/playlist?list=PLxxxx"}
  ]
}
```

Pode editar esse arquivo manualmente também.

## Automatizar (opcional)

Com [Termux:Boot](https://wiki.termux.com/wiki/Termux:Boot) ou um cron via
`termux-job-scheduler`, dá pra rodar `ytmusic sync` uma vez por dia/semana
e manter a biblioteca sempre atualizada sem precisar lembrar de rodar
manualmente.

## Por que não um APK?

Empacotar yt-tdm + ffmpeg + um runtime JS num APK nativo é possível
(via Kivy/Buildozer, por exemplo), mas é um projeto bem mais complexo e
frágil de manter do que aproveitar o Termux, que já roda Python e
binários nativos de forma simples e com acesso direto ao armazenamento
compartilhado do Android.

## Licença

Uso pessoal, sem garantias. Fique à vontade para adaptar.
=======
# ytmusic
Baixador de música do YouTube com letras sincronizadas (.lrc), feito para rodar 100% no **Termux**, sem depender de nenhum streaming pago. Pensado para uso com players locais como o [Musicolet](https://play.google.com/store/apps/details?id=in.krosbits.musicolet).
