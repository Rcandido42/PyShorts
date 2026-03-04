import whisper
import os

def extrair_legendas(caminho_audio):
    print("Carregando a IA do Whisper (isso pode demorar um pouquinho na 1ª vez)...")
    modelo = whisper.load_model("base")
    
    print(f"Ouvindo o áudio '{caminho_audio}' e cravando os tempos...")
    
    resultado = modelo.transcribe(caminho_audio, language="pt", word_timestamps=True, fp16=False)
    
    legendas = []
    
    for segmento in resultado["segments"]:
        for palavra in segmento["words"]:
            legendas.append({
                "texto": palavra["word"].strip(),
                "inicio": palavra["start"],
                "fim": palavra["end"]
            })
            
    print(f"Sucesso! Extraídas {len(legendas)} palavras com sincronização exata.")
    return legendas

if __name__ == "__main__":
    arquivo_audio = "assets/audio_teste.mp3"
    
    if os.path.exists(arquivo_audio):
        palavras = extrair_legendas(arquivo_audio)
        
        print("\n Teste de Sincronização (Primeiras 5 palavras):")
        for p in palavras[:5]:
            print(f"[{p['inicio']:.2f}s -> {p['fim']:.2f}s] {p['texto']}")
    else:
        print("Áudio não encontrado. Rode o gerador_audio.py primeiro!")