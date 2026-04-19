# Estructura del Proyecto

```
social-video-downloader/
├── src/                        # Codigo fuente de los 4 descargadores
│   ├── yt-downloader.py        # YouTube
│   ├── ig-downloader.py        # Instagram
│   ├── tk-downloader.py        # TikTok
│   └── fb-downloader.py        # Facebook
├── assets/                     # Imagenes y recursos visuales
│   ├── banner.html             # Banner para GitHub (abrir en navegador)
│   └── banner.css              # Estilos del banner
├── install.bat                 # Instalador principal
├── install.reg                 # Registro del menu contextual
├── uninstall.reg               # Desinstalador
├── requirements.txt            # Dependencias de Python
├── README.md                   # Documentacion
├── CHANGELOG.md                # Historial de cambios
├── LICENSE                     # Licencia MIT
└── .gitignore                  # Archivos ignorados por Git
```

## Como Subir a GitHub

1. Crea un nuevo repositorio en GitHub
2. Inicializa Git en esta carpeta:
   ```bash
   cd social-video-downloader
   git init
   git add .
   git commit -m "Initial release: v1.0.0"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/social-video-downloader.git
   git push -u origin main
   ```

3. Crea un Release:
   - Ve a "Releases" en tu repo de GitHub
   - Click "Create a new release"
   - Tag: `v1.0.0`
   - Title: `Social Video Downloader v1.0`
   - Descripcion: Copia el resumen del README

## Para hacer el banner:

1. Abre `assets/banner.html` en Chrome/Edge
2. Presiona F12 > Ctrl+Shift+P > "Capture full size screenshot"
3. Guarda la captura como `assets/demo.png`
4. Sube `demo.png` al repositorio
