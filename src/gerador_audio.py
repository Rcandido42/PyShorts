import asyncio
import edge_tts
import os

VOZ = "pt-BR-AntonioNeural"

async def gerar_audio(texto, caminho_saida):
    print(f"Gerando áudio para: '{texto[:40]}...'")
    
    comunicacao = edge_tts.Communicate(texto, VOZ)
    
    await comunicacao.save(caminho_saida)
    print(f"Áudio salvo com sucesso em: {caminho_saida}")

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    
    texto_teste = "Fala mano! Este é o primeiro teste do nosso gerador automático de vídeos. Se você está ouvindo isso, o código funcionou perfeitamente!"
    
    arquivo_saida = "assets/audio_teste.mp3"
    
    asyncio.run(gerar_audio(texto_teste, arquivo_saida))