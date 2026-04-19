#!/bin/env python3
# TK Downloader - TikTok Videos

import tkinter as tk
from tkinter import scrolledtext
import yt_dlp
import threading
import queue
import os
import re
import whisper
import torch

# Static output directory for TikTok
OUTPUT_DIR = r"F:\TK_VIDEOS"
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


def transcribe_audio(video_path, text_path):
    """Extract and transcribe audio from video using Whisper AI"""
    log_message(f"📝 Transcribiendo audio del video...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("small", device=device)
    result = model.transcribe(video_path)

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    log_message(f"✅ Transcripción guardada en {text_path}")


def download_video_worker():
    """Background worker for downloading TikTok videos"""
    while True:
        url = video_queue.get()
        if url is None:
            break
        try:
            log_message(f"📥 Descargando de TikTok: {url}")

            # First, extract info to get the video title/description
            info_opts = {"quiet": True}
            with yt_dlp.YoutubeDL(info_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get("title", "tiktok_video")
                # Use description if title is empty or generic
                if not video_title or video_title == "TikTok video":
                    video_title = info.get("description", "tiktok_video")[:50]

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

            # Download TikTok video (best quality with audio)
            ydl_opts = {
                "format": "best",
                "outtmpl": os.path.join(video_folder, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
            }

            # Download video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=True)
                video_filename = ydl.prepare_filename(video_info)
                # Ensure it has .mp4 extension
                if not video_filename.endswith(".mp4"):
                    video_filename = video_filename.rsplit(".", 1)[0] + ".mp4"

            log_message(f"✅ Video descargado: {video_filename}")

            # Perform transcription if video has audio
            try:
                transcription_file = os.path.join(video_folder, "transcripcion.txt")
                transcribe_audio(video_filename, transcription_file)
            except Exception as e:
                log_message(f"⚠️  No se pudo transcribir: {str(e)}")

            log_message(f"✅ Descarga completada: {url}")

        except Exception as e:
            log_message(f"❌ Error al procesar {url}: {str(e)}")

        video_queue.task_done()


def download_video():
    """Add video to queue for downloading"""
    url = url_entry.get()
    if not url:
        log_message("❌ Error: Por favor, ingrese un enlace de TikTok.")
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
root.title("Descargador de TikTok")

# Label
label = tk.Label(root, text="Ingrese el enlace de TikTok:")
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
