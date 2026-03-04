# PyShorts Studio - Gerador de Vídeos Virais 100% Automático

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-darkblue)
![AI](https://img.shields.io/badge/AI-Whisper_&_EdgeTTS-green)

O PyShorts Studio é uma aplicação completa em Python que automatiza a criação de vídeos curtos (Shorts, Reels, TikToks). Com apenas um clique, o software baixa um vídeo de fundo, gera a narração com Inteligência Artificial, sincroniza as palavras e renderiza o vídeo final em formato vertical com legendas animadas.

---

## Funcionalidades

- Download Automático: Baixa vídeos de fundo do YouTube em alta qualidade.
- Voz com IA: Transforma qualquer texto numa narração realista usando `edge-tts`.
- Legendas Inteligentes: Usa a IA da OpenAI (`Whisper`) para ouvir o áudio e sincronizar cada palavra com precisão de milissegundos.
- Formato TikTok/Shorts: Corta e redimensiona o vídeo automaticamente para a proporção 9:16 (1080x1920).
- Interface Moderna: GUI em Dark Mode construída com `CustomTkinter`, rodando processos em segundo plano para não "congelar" a janela.

---

## Como Instalar

### 1. Pré-requisitos
Antes de rodares o projeto, precisas de instalar o ImageMagick (essencial para o Python desenhar as legendas):
1. Baixa a versão para Windows 64-bit no [site oficial](https://imagemagick.org/script/download.php).
2. Durante a instalação, marca a caixa "Install legacy utilities (e.g. convert)".
3. Confirma se o caminho `C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe` (ou a tua versão específica) está correto no ficheiro `src/editor_video.py`.

### 2. Configurar o Ambiente
Clona este repositório e cria um ambiente virtual (recomendado na raiz do Disco C: para evitar bugs de sincronização com o OneDrive):

```powershell
# Cria a pasta e entra nela
mkdir C:\PyShorts
cd C:\PyShorts

# Cria e ativa o ambiente virtual
python -m venv venv
.\venv\Scripts\activate
