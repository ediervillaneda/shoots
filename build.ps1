# build.ps1 -- Lanzador del build de Starfall
# Uso: .\build.ps1
# Requiere: Python 3.12+, pip install pygame-ce pyinstaller

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

python build_release.py
