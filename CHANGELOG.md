# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-04-15

### Added
- 🎉 Initial release
- YT Downloader: YouTube video downloads with audio merge and Whisper transcription
- IG Downloader: Instagram Reels & Stories downloads with transcription
- TK Downloader: TikTok video downloads with transcription
- FB Downloader: Facebook video downloads with transcription
- Windows context menu integration via registry files
- One-click `install.bat` installer
- Automatic folder organization per video
- Duplicate detection (skips already downloaded videos)
- Uninstaller included (`uninstall.reg`)

### Features
- Right-click on any folder to access downloaders
- GPU acceleration for Whisper transcription (CUDA support)
- Queue system for batch downloads
- Console toggle in GUI
- Clean folder structure:
  - `F:\YT_VIDEOS\`
  - `F:\IG_VIDEOS\`
  - `F:\TK_VIDEOS\`
  - `F:\FB_VIDEOS\`
