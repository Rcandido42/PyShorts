import whisper

def extrair_legendas(caminho_audio):
    print("A carregar a IA do Whisper (isto pode demorar um pouco)...")
    modelo = whisper.load_model("base")
    
    print(f"A ouvir o áudio '{caminho_audio}' e a extrair os tempos...")
    resultado = modelo.transcribe(caminho_audio, language="pt", word_timestamps=True, fp16=False)
    
    legendas = []
    for segmento in resultado["segments"]:
        for palavra in segmento["words"]:
            legendas.append({
                "texto": palavra["word"].strip().upper(),
                "inicio": palavra["start"],
                "fim": palavra["end"]
            })
            
    print(f"Sucesso! Extraídas {len(legendas)} palavras.")
    return legendas