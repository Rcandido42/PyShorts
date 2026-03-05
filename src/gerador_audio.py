import edge_tts

async def gerar_audio(texto, caminho_saida, voz_escolhida="Masculino (PT-BR)"):
    vozes = {
        "Masculino (PT-BR)": "pt-BR-AntonioNeural",
        "Feminina (PT-BR)": "pt-BR-FranciscaNeural",
        "Masculino (PT-PT)": "pt-PT-DuarteNeural",
        "Feminina (PT-PT)": "pt-PT-RaquelNeural"
    }
    
    voz_oficial = vozes.get(voz_escolhida, "pt-BR-AntonioNeural")
    
    communicate = edge_tts.Communicate(texto, voz_oficial)
    await communicate.save(caminho_saida)