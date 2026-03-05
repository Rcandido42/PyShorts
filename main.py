import asyncio
import os
from src.gerador_audio import gerar_audio
from src.gerador_legendas import extrair_legendas
from src.editor_video import montar_video
from src.baixar_video import baixar_fundo_youtube

async def main():
    os.makedirs("assets/output", exist_ok=True)

    texto_do_video = "Deu certo"
    link_youtube = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    
    arquivo_audio = "assets/audio_teste.mp3"
    arquivo_fundo = "assets/background.mp4"
    arquivo_saida = "assets/output/video_final.mp4"

    print("A INICIAR A FÁBRICA DE VÍDEOS AUTOMÁTICA...\n")
    
    sucesso_download = baixar_fundo_youtube(link_youtube, arquivo_fundo)
    if not sucesso_download:
        print("Parando o processo devido a erro no download.")
        return

    await gerar_audio(texto_do_video, arquivo_audio)

    legendas = extrair_legendas(arquivo_audio)

    montar_video(arquivo_fundo, arquivo_audio, legendas, arquivo_saida)

if __name__ == "__main__":
    asyncio.run(main())