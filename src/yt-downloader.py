#!/bin/env python3
# YT Downloader - YouTube Videos with Audio Merge & Transcription

import tkinter as tk
from tkinter import scrolledtext
import yt_dlp
import threading
import queue
import os
import re
import whisper
import torch
import subprocess
from pydub import AudioSegment

# Static output directory
OUTPUT_DIR = r"F:\YT_VIDEOS"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cola para almacenar las descargas
video_queue = queue.Queue()


def log_message(message):
    console_text.config(state=tk.NORMAL)
    console_text.insert(tk.END, message + "\n")
    console_text.config(state=tk.DISABLED)
    console_text.see(tk.END)


def sanitize_folder_name(name):
    """Remove invalid characters from folder name"""
    # Remove or replace invalid Windows filename characters
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    # Remove leading/trailing spaces and dots
    name = name.strip(" .")
    # Limit length to avoid path too long errors
    if len(name) > 100:
        name = name[:100]
    return name


def transcribe_audio(audio_path, text_path):
    """Transcribe audio using Whisper AI"""
    log_message(f"📝 Transcribiendo con Whisper (GPU - CUDA)...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("small", device=device)
    result = model.transcribe(audio_path)

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    log_message(f"✅ Transcripción guardada en {text_path}")


def merge_video_audio(video_path, audio_path, output_path):
    """Merge MP4 video with MP3 audio using FFmpeg"""
    log_message(
        f"🎬 Combinando video {video_path} con audio {audio_path} en {output_path}..."
    )

    try:
        command = [
            "ffmpeg",
            "-y",
            "-i",
            video_path,  # Input video
            "-i",
            audio_path,  # Input MP3
            "-c:v",
            "copy",  # Keep original video quality
            "-c:a",
            "aac",
            "-b:a",
            "192k",  # Convert audio to AAC
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",  # Ensure correct mapping
            "-strict",
            "experimental",
            output_path,
        ]
        subprocess.run(command, check=True)
        log_message(f"✅ Video final con audio guardado: {output_path}")
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Error al unir video y audio: {str(e)}")


def download_video_worker():
    """Background worker for downloading videos"""
    while True:
        url = video_queue.get()
        if url is None:
            break
        try:
            log_message(f"📥 Descargando: {url}")

            # First, extract info to get the video title
            info_opts = {"quiet": True}
            with yt_dlp.YoutubeDL(info_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get("title", "video")

            # Create unique folder based on video title
            folder_name = sanitize_folder_name(video_title)
            video_folder = os.path.join(OUTPUT_DIR, folder_name)

            # Check if video already exists - skip if it does
            if os.path.exists(video_folder):
                log_message(f"⏭️  Video ya existe (omitido): {video_title}")
                video_queue.task_done()
                continue

            os.makedirs(video_folder, exist_ok=True)
            log_message(f"📁 Carpeta creada: {video_folder}")

            # Download highest-quality video (NO AUDIO)
            video_opts = {
                "format": "bestvideo",
                "outtmpl": os.path.join(video_folder, "%(title)s_video.%(ext)s"),
            }

            # Download best audio separately (MP3)
            audio_opts = {
                "format": "bestaudio",
                "outtmpl": os.path.join(video_folder, "%(title)s_audio.%(ext)s"),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }

            # Download video
            with yt_dlp.YoutubeDL(video_opts) as ydl:
                video_info = ydl.extract_info(url, download=True)
                video_filename = ydl.prepare_filename(video_info)

            # Download audio
            with yt_dlp.YoutubeDL(audio_opts) as ydl:
                audio_info = ydl.extract_info(url, download=True)
                mp3_filename = ydl.prepare_filename(audio_info).replace(".webm", ".mp3")

            # Merge video and MP3
            final_mp4 = (
                video_filename.replace("_video", "_final")
                .replace(".webm", ".mp4")
                .replace(".mkv", ".mp4")
            )
            merge_video_audio(video_filename, mp3_filename, final_mp4)

            # Perform transcription
            transcription_file = mp3_filename.replace(".mp3", ".txt")
            transcribe_audio(mp3_filename, transcription_file)

            log_message(f"✅ Descarga y transcripción completadas: {url}")

        except Exception as e:
            log_message(f"❌ Error al procesar {url}: {str(e)}")

        video_queue.task_done()


def download_video():
    """Add video to queue for downloading"""
    url = url_entry.get()
    if not url:
        log_message("❌ Error: Por favor, ingrese un enlace de video de YouTube.")
        return
    video_queue.put(url)
    url_entry.delete(0, tk.END)


def start_worker():
    """Start background download worker thread"""
    worker_thread = threading.Thread(target=download_video_worker, daemon=True)
    worker_thread.start()


def toggle_console():
    """Show/hide console window"""
    if console_frame.winfo_ismapped():
        console_frame.pack_forget()
    else:
        console_frame.pack(fill=tk.BOTH, expand=True)


# GUI Configuration
root = tk.Tk()
root.title("Descargador de YouTube con Transcripción y Consola")

# Label
label = tk.Label(root, text="Ingrese el enlace del video de YouTube:")
label.pack(pady=10)

# URL Entry
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

# Download Button
download_button = tk.Button(root, text="Agregar a la Cola", command=download_video)
download_button.pack(pady=10)

# Toggle Console Button
toggle_button = tk.Button(root, text="Mostrar/Ocultar Consola", command=toggle_console)
toggle_button.pack(pady=5)

# Console Frame
console_frame = tk.Frame(root)
console_text = scrolledtext.ScrolledText(
    console_frame, width=60, height=10, state=tk.DISABLED
)
console_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Start Background Worker
start_worker()

# Run Application
root.mainloop()
