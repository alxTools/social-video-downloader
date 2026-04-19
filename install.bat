@echo off
chcp 65001 >nul
title Social Video Downloader - Instalador
color 0A

echo ╔════════════════════════════════════════════════════════════╗
echo ║        Social Video Downloader - Instalador                ║
echo ║        Descarga videos de YouTube, Instagram,              ║
echo ║        TikTok y Facebook con un solo clic                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  Este instalador necesita permisos de administrador.
    echo    Solicitando elevacion...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo 📦 Verificando dependencias...
echo.

:: Check Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python no esta instalado.
    echo    Por favor, instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)
echo ✅ Python detectado

:: Check pip
pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ pip no esta instalado.
    pause
    exit /b 1
)
echo ✅ pip detectado

echo.
echo 📥 Instalando dependencias de Python...
echo.

:: Install required packages
pip install yt-dlp whisper openai-whisper torch pydub

echo.
echo 📁 Creando directorios de salida...
echo.

:: Create output directories
if not exist "F:\YT_VIDEOS" mkdir "F:\YT_VIDEOS"
if not exist "F:\IG_VIDEOS" mkdir "F:\IG_VIDEOS"
if not exist "F:\TK_VIDEOS" mkdir "F:\TK_VIDEOS"
if not exist "F:\FB_VIDEOS" mkdir "F:\FB_VIDEOS"

echo ✅ Directorios creados:
echo    - F:\YT_VIDEOS (YouTube)
echo    - F:\IG_VIDEOS (Instagram)
echo    - F:\TK_VIDEOS (TikTok)
echo    - F:\FB_VIDEOS (Facebook)

echo.
echo 📝 Instalando entradas del menu contextual...
echo.

:: Copy files to user Documents
set "INSTALL_DIR=%USERPROFILE%\Documents\SocialVideoDownloader"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\src" mkdir "%INSTALL_DIR%\src"

copy /Y "src\*.py" "%INSTALL_DIR%\src\"

echo ✅ Archivos copiados a: %INSTALL_DIR%

echo.
echo 🔄 Registrando en el menu contextual de Windows...
echo.

:: Import registry
regedit /s "install.reg"

echo ✅ Instalacion completada!
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                     INSTRUCCIONES                          ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║ 1. Haz clic derecho en cualquier carpeta                   ║
echo ║ 2. Selecciona:                                             ║
echo ║    • YT Downloader - Para videos de YouTube                ║
echo ║    • IG Downloader - Para Reels/Stories de Instagram       ║
echo ║    • TK Downloader - Para videos de TikTok                 ║
echo ║    • FB Downloader - Para videos de Facebook               ║
echo ║ 3. Pega el enlace y haz clic en "Agregar a la Cola"        ║
echo ║ 4. Los videos se guardaran automaticamente en F:\          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pause
