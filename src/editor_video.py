import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import os
from moviepy.config import change_settings
import moviepy.video.fx.all as vfx

caminho_magick = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
change_settings({"IMAGEMAGICK_BINARY": caminho_magick})

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

def montar_video(caminho_fundo, caminho_audio, legendas, caminho_saida, cor_legenda="Amarelo"):
    video_fundo = VideoFileClip(caminho_fundo)
    audio_fala = AudioFileClip(caminho_audio)
    
    video_fundo = video_fundo.without_audio().subclip(0, audio_fala.duration)
    video_fundo = video_fundo.set_audio(audio_fala)
    
    video_fundo = video_fundo.resize(height=1920)
    video_fundo = vfx.crop(video_fundo, width=1080, height=1920, x_center=video_fundo.w/2, y_center=video_fundo.h/2)
    
    clipes_tela = [video_fundo]
    
    cores = {
        "Amarelo": "yellow",
        "Branco": "white",
        "Verde": "#00FF00", 
        "Vermelho": "red"
    }
    cor_oficial = cores.get(cor_legenda, "yellow")
    
    for leg in legendas:
        txt_clip = TextClip(
            leg["texto"], 
            fontsize=110, 
            color=cor_oficial, 
            font='Arial-Bold', 
            stroke_color='black', 
            stroke_width=4,
            method='label'
        )
        txt_clip = txt_clip.set_start(leg["inicio"]).set_end(leg["fim"]).set_position(('center', 'center'))
        clipes_tela.append(txt_clip)
    
    video_final = CompositeVideoClip(clipes_tela)
    
    video_final.write_videofile(
        caminho_saida, 
        fps=30, 
        codec="libx264", 
        audio_codec="aac", 
        audio=True, 
        threads=4,
        ffmpeg_params=["-pix_fmt", "yuv420p"] 
    )
    
    video_fundo.close()
    audio_fala.close()
    video_final.close()