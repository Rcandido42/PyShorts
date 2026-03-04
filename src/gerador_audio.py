import asyncio
import edge_tts

VOZ = "pt-BR-AntonioNeural"

async def gerar_audio(texto, caminho_saida):
    print(f"A gerar áudio para: '{texto[:40]}...'")
    
    comunicacao = edge_tts.Communicate(texto, VOZ)
    await comunicacao.save(caminho_saida)
    
    print(f"Áudio salvo com sucesso em: {caminho_saida}")