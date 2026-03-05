import customtkinter as ctk
import threading
import asyncio
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

from src.gerador_audio import gerar_audio
from src.gerador_legendas import extrair_legendas
from src.editor_video import montar_video
from src.baixar_video import baixar_fundo_youtube

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppPyShorts(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PyShorts Studio")
        self.geometry("700x720")
        self.resizable(False, False)

        fonte_titulo = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        fonte_label = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        fonte_texto = ctk.CTkFont(family="Segoe UI", size=13)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tab_estudio = self.tabview.add("Estudio de Criacao")
        self.tab_biblioteca = self.tabview.add("Minha Biblioteca")

        self.lbl_titulo = ctk.CTkLabel(self.tab_estudio, text="Criar Novo Video", font=fonte_titulo, text_color="#3b8ed0")
        self.lbl_titulo.pack(pady=(5, 10))

        self.frame_inputs = ctk.CTkFrame(self.tab_estudio, corner_radius=15)
        self.frame_inputs.pack(padx=20, pady=5, fill="both", expand=True)

        self.frame_ia = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_ia.pack(padx=20, pady=(15, 5), fill="x")

        self.input_tema = ctk.CTkEntry(self.frame_ia, placeholder_text="Ex: Curiosidades sobre o Espaco...", font=fonte_texto)
        self.input_tema.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_gerar_ia = ctk.CTkButton(self.frame_ia, text="Gerar Guiao", width=120, fg_color="#8e44ad", hover_color="#732d91", command=self.gerar_guiao)
        self.btn_gerar_ia.pack(side="right")

        self.caixa_texto = ctk.CTkTextbox(self.frame_inputs, height=80, font=fonte_texto)
        self.caixa_texto.pack(padx=20, pady=(5, 10), fill="x")
        self.caixa_texto.insert("1.0", "Escreva a narracao ou use o botao Gerar Guiao acima...")

        self.frame_opcoes = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_opcoes.pack(padx=20, pady=5, fill="x")

        self.lbl_voz = ctk.CTkLabel(self.frame_opcoes, text="Voz:", font=fonte_label)
        self.lbl_voz.pack(side="left")
        self.combo_voz = ctk.CTkOptionMenu(self.frame_opcoes, values=["Masculino (PT-BR)", "Feminina (PT-BR)", "Masculino (PT-PT)", "Feminina (PT-PT)"])
        self.combo_voz.pack(side="left", padx=(10, 20))

        self.lbl_cor = ctk.CTkLabel(self.frame_opcoes, text="Legenda:", font=fonte_label)
        self.lbl_cor.pack(side="left")
        self.combo_cor = ctk.CTkOptionMenu(self.frame_opcoes, values=["Amarelo", "Branco", "Verde", "Vermelho"])
        self.combo_cor.pack(side="left", padx=(10, 0))

        self.lbl_youtube = ctk.CTkLabel(self.frame_inputs, text="Link do YouTube (Video de Fundo):", font=fonte_label)
        self.lbl_youtube.pack(anchor="w", padx=20, pady=(10, 5))

        self.input_youtube = ctk.CTkEntry(self.frame_inputs, height=40, font=fonte_texto)
        self.input_youtube.pack(padx=20, pady=(0, 20), fill="x")
        self.input_youtube.insert(0, "https://www.youtube.com/watch?v=aqz-KE-bpKQ")

        self.frame_acao = ctk.CTkFrame(self.tab_estudio, fg_color="transparent")
        self.frame_acao.pack(padx=20, pady=10, fill="x")

        self.btn_gerar = ctk.CTkButton(self.frame_acao, text="GERAR VIDEO AGORA", height=50, font=fonte_label, command=self.iniciar_processo)
        self.btn_gerar.pack(fill="x", pady=(0, 10))

        self.barra_progresso = ctk.CTkProgressBar(self.frame_acao, height=8, corner_radius=4)
        self.barra_progresso.pack(fill="x", pady=(0, 10))
        self.barra_progresso.set(0)
        self.barra_progresso.pack_forget()

        self.lbl_status = ctk.CTkLabel(self.frame_acao, text="Pronto para processar.", font=fonte_texto, text_color="gray")
        self.lbl_status.pack()

        self.lbl_bib_titulo = ctk.CTkLabel(self.tab_biblioteca, text="Videos Guardados", font=fonte_titulo, text_color="#3b8ed0")
        self.lbl_bib_titulo.pack(pady=(10, 5))

        self.btn_atualizar = ctk.CTkButton(self.tab_biblioteca, text="Atualizar Lista", width=150, command=self.carregar_biblioteca)
        self.btn_atualizar.pack(pady=(0, 10))

        self.scroll_biblioteca = ctk.CTkScrollableFrame(self.tab_biblioteca, corner_radius=15)
        self.scroll_biblioteca.pack(fill="both", expand=True, padx=20, pady=10)

        os.makedirs("assets/output", exist_ok=True)
        self.carregar_biblioteca()

    def gerar_guiao(self):
        tema = self.input_tema.get().strip()
        if not tema:
            self.caixa_texto.delete("1.0", "end")
            self.caixa_texto.insert("1.0", "Erro: Escreve um tema ali em cima primeiro!")
            return

        self.btn_gerar_ia.configure(state="disabled", text="A Pensar...")
        self.caixa_texto.delete("1.0", "end")
        self.caixa_texto.insert("1.0", f"A usar Inteligencia Artificial para escrever um guiao sobre '{tema}'... Aguarda uns segundos!")

        threading.Thread(target=self.chamar_ia, args=(tema,)).start()

    def chamar_ia(self, tema):
        try:
            load_dotenv()
            chave_secreta = os.getenv("GEMINI_API_KEY")
            
            if not chave_secreta:
                raise Exception("Chave API nao encontrada no ficheiro .env!")

            genai.configure(api_key=chave_secreta)
            
            modelo = genai.GenerativeModel('gemini-2.5-flash') 
            prompt = f"Crie um guiao curto e viral para um video do TikTok/Shorts sobre: {tema}. O texto deve ser cativante e ir direto ao assunto. Nao inclua hashtags, nao inclua descricoes de cena, nao use emojis, escreva apenas o texto limpo que sera narrado."

            resposta = modelo.generate_content(prompt)
            texto_final = resposta.text.strip()

            self.after(0, lambda: self.caixa_texto.delete("1.0", "end"))
            self.after(0, lambda: self.caixa_texto.insert("1.0", texto_final))

        except Exception as e:
            self.after(0, lambda: self.caixa_texto.delete("1.0", "end"))
            self.after(0, lambda: self.caixa_texto.insert("1.0", f"Erro na IA: {e}"))
            
        finally:
            self.after(0, lambda: self.btn_gerar_ia.configure(state="normal", text="Gerar Guiao"))

    def carregar_biblioteca(self):
        for widget in self.scroll_biblioteca.winfo_children():
            widget.destroy()
        
        pasta_output = "assets/output"
        arquivos = [f for f in os.listdir(pasta_output) if f.endswith('.mp4')]
        arquivos.sort(reverse=True)
        
        if not arquivos:
            lbl_vazio = ctk.CTkLabel(self.scroll_biblioteca, text="Ainda nao criaste nenhum video. Vai ao Estudio!", text_color="gray")
            lbl_vazio.pack(pady=40)
            return

        for arq in arquivos:
            caminho_completo = os.path.abspath(os.path.join(pasta_output, arq))
            
            try:
                tamanho_mb = os.path.getsize(caminho_completo) / (1024 * 1024)
                tamanho_str = f"{tamanho_mb:.1f} MB"
            except:
                tamanho_str = "Desconhecido"

            frame_item = ctk.CTkFrame(self.scroll_biblioteca, fg_color="#2b2b2b", corner_radius=10)
            frame_item.pack(fill="x", padx=10, pady=5)
            
            frame_textos = ctk.CTkFrame(frame_item, fg_color="transparent")
            frame_textos.pack(side="left", padx=15, pady=10)
            
            lbl_nome = ctk.CTkLabel(frame_textos, text=arq, font=ctk.CTkFont(weight="bold", size=14))
            lbl_nome.pack(anchor="w")
            
            lbl_tamanho = ctk.CTkLabel(frame_textos, text=tamanho_str, text_color="gray", font=ctk.CTkFont(size=11))
            lbl_tamanho.pack(anchor="w")
            
            btn_apagar = ctk.CTkButton(
                frame_item, 
                text="Eliminar", 
                width=80, 
                fg_color="#8b0000", 
                hover_color="#5c0000",
                command=lambda c=caminho_completo: self.eliminar_video(c)
            )
            btn_apagar.pack(side="right", padx=(5, 15), pady=15)

            btn_abrir = ctk.CTkButton(
                frame_item, 
                text="Abrir", 
                width=80, 
                fg_color="#1f538d", 
                command=lambda c=caminho_completo: os.startfile(c)
            )
            btn_abrir.pack(side="right", padx=5, pady=15)

    def eliminar_video(self, caminho_arquivo):
        try:
            os.remove(caminho_arquivo)
            self.carregar_biblioteca()
        except Exception as e:
            print(f"Erro ao apagar ficheiro: {e}")

    def iniciar_processo(self):
        self.btn_gerar.configure(state="disabled", text="A PROCESSAR... (Aguarde)")
        self.lbl_status.configure(text="A iniciar os motores...", text_color="#3b8ed0")
        
        self.barra_progresso.pack(fill="x", pady=(0, 10))
        self.barra_progresso.set(0.05)

        texto_usuario = self.caixa_texto.get("1.0", "end").strip()
        url_youtube = self.input_youtube.get().strip()
        
        voz_escolhida = self.combo_voz.get()
        cor_escolhida = self.combo_cor.get()

        threading.Thread(target=self.rodar_backend, args=(texto_usuario, url_youtube, voz_escolhida, cor_escolhida)).start()

    def rodar_backend(self, texto, url, voz, cor):
        asyncio.run(self.fluxo_principal(texto, url, voz, cor))

    async def fluxo_principal(self, texto, url, voz, cor):
        os.makedirs("assets/output", exist_ok=True)
        
        arq_audio = "assets/audio_teste.mp3"
        arq_fundo = "assets/background.mp4"
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        arq_saida = f"assets/output/video_{timestamp}.mp4"

        try:
            self.atualizar_interface("A descarregar video de fundo...", "#E1B000", 0.25)
            if not baixar_fundo_youtube(url, arq_fundo):
                raise Exception("Erro ao baixar o video. Verifica o link.")

            self.atualizar_interface(f"A gerar narracao ({voz})...", "#E1B000", 0.50)
            await gerar_audio(texto, arq_audio, voz)

            self.atualizar_interface("A extrair tempos das legendas...", "#E1B000", 0.75)
            legendas = extrair_legendas(arq_audio)

            self.atualizar_interface(f"A renderizar video (Legendas: {cor})...", "#E1B000", 0.90)
            montar_video(arq_fundo, arq_audio, legendas, arq_saida, cor)

            caminho_absoluto = os.path.abspath(arq_saida)
            self.atualizar_interface(f"SUCESSO! Video salvo.", "#2ECC71", 1.0)
            
            self.after(0, self.carregar_biblioteca)
            os.startfile(caminho_absoluto)

        except Exception as e:
            self.atualizar_interface(f"ERRO: {str(e)}", "#E74C3C", 0)
            
        finally:
            self.after(0, lambda: self.btn_gerar.configure(state="normal", text="GERAR NOVO VIDEO"))

    def atualizar_interface(self, mensagem, cor, progresso):
        self.after(0, lambda: self.lbl_status.configure(text=mensagem, text_color=cor))
        self.after(0, lambda: self.barra_progresso.set(progresso))

if __name__ == "__main__":
    app = AppPyShorts()
    app.mainloop()