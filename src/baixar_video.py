import yt_dlp
import os

def baixar_fundo_youtube(url, caminho_saida):
    print(f"A baixar vídeo de fundo da URL: {url} ...")
    
    if os.path.exists(caminho_saida):
        print("O vídeo já existe na pasta, a saltar o download...")
        return True
    
    opcoes = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': caminho_saida,
        'noplaylist': True,
        'playlist_items': '1',
        'quiet': False
    }
    
    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        print(f"Vídeo baixado com sucesso! Salvo em: {caminho_saida}")
        return True
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")
        return False