import customtkinter as ctk
import threading
import asyncio
import os

from src.gerador_audio import gerar_audio
from src.gerador_legendas import extrair_legendas
from src.editor_video import montar_video
from src.baixar_video import baixar_fundo_youtube

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppPyShorts(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PyShorts - Gerador de Vídeos Virais")
        self.geometry("600x550")
        self.resizable(False, False)

        self.lbl_titulo = ctk.CTkLabel(self, text="PyShorts Studio", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo.pack(pady=(20, 10))

        self.lbl_texto = ctk.CTkLabel(self, text="O que o robô deve falar no vídeo?")
        self.lbl_texto.pack(anchor="w", padx=30)
        
        self.caixa_texto = ctk.CTkTextbox(self, height=120, width=540)
        self.caixa_texto.pack(padx=30, pady=(0, 20))
        self.caixa_texto.insert("1.0", "Fala mano! Este é um teste gerado diretamente da nossa nova interface visual em Python. O vídeo agora vai ficar em formato vertical, com a voz limpa e as legendas gigantes no meio da tela!")

        self.lbl_youtube = ctk.CTkLabel(self, text="Link do YouTube (Vídeo de fundo):")
        self.lbl_youtube.pack(anchor="w", padx=30)
        
        self.input_youtube = ctk.CTkEntry(self, width=540, placeholder_text="Ex: https://www.youtube.com/watch?v=...")
        self.input_youtube.pack(padx=30, pady=(0, 30))
        self.input_youtube.insert(0, "https://www.youtube.com/watch?v=aqz-KE-bpKQ")

        self.btn_gerar = ctk.CTkButton(self, text="GERAR VÍDEO AGORA", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=self.iniciar_processo)
        self.btn_gerar.pack(padx=30, fill="x")

        self.lbl_status = ctk.CTkLabel(self, text="Pronto para começar.", text_color="gray")
        self.lbl_status.pack(pady=20)

    def iniciar_processo(self):
        self.btn_gerar.configure(state="disabled", text="A GERAR... (Aguarde o processo terminar!)")
        self.lbl_status.configure(text="A iniciar os motores...", text_color="yellow")

        texto_usuario = self.caixa_texto.get("1.0", "end").strip()
        url_youtube = self.input_youtube.get().strip()

        threading.Thread(target=self.rodar_backend, args=(texto_usuario, url_youtube)).start()

    def rodar_backend(self, texto, url):
        asyncio.run(self.fluxo_principal(texto, url))

    async def fluxo_principal(self, texto, url):
        os.makedirs("assets/output", exist_ok=True)
        
        arq_audio = "assets/audio_teste.mp3"
        arq_fundo = "assets/background.mp4"
        arq_saida = "assets/output/video_final.mp4"

        try:
            self.atualizar_status("A baixar vídeo de fundo (YouTube)...", "yellow")
            if not baixar_fundo_youtube(url, arq_fundo):
                raise Exception("Erro ao baixar o vídeo. Verifica o link.")

            self.atualizar_status("A gerar narração com IA...", "yellow")
            await gerar_audio(texto, arq_audio)

            self.atualizar_status("A extrair tempos das legendas (Whisper demora um bocado)...", "yellow")
            legendas = extrair_legendas(arq_audio)

            self.atualizar_status("A renderizar o vídeo final (Aguarde a barra chegar a 100%)...", "orange")
            montar_video(arq_fundo, arq_audio, legendas, arq_saida)

            caminho_absoluto = os.path.abspath("assets/output")
            self.atualizar_status(f"SUCESSO! Vídeo salvo em:\n{caminho_absoluto}", "green")
            
            os.startfile(caminho_absoluto)

        except Exception as e:
            self.atualizar_status(f"ERRO: {str(e)}", "red")
            
        finally:
            self.atualizar_status_botao("normal", "GERAR VÍDEO AGORA")

    def atualizar_status(self, mensagem, cor):
        self.after(0, lambda: self.lbl_status.configure(text=mensagem, text_color=cor))
        
    def atualizar_status_botao(self, estado, texto):
        self.after(0, lambda: self.btn_gerar.configure(state=estado, text=texto))

if __name__ == "__main__":
    app = AppPyShorts()
    app.mainloop()