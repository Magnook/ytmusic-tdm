#!/data/data/com.termux/files/usr/bin/bash
# Instala dependências do ytmusic-dl no Termux.
set -e

echo "==> Atualizando pacotes..."
pkg update -y

echo "==> Instalando dependências do sistema (python, ffmpeg, nodejs)..."
pkg install -y python ffmpeg nodejs

echo "==> Garantindo acesso ao armazenamento compartilhado..."
if [ ! -d "$HOME/storage" ]; then
    termux-setup-storage
fi

echo "==> Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Instalando o ytmusic-dl em modo editável..."
pip install -e .

echo ""
echo "Pronto! Use 'ytmusic --help' para ver os comandos disponíveis."
echo "Primeiro passo: ytmusic add-playlist \"https://www.youtube.com/playlist?list=SEU_ID\""
