"""
build_release.py -- Genera Starfall.exe
Uso: python build_release.py
"""

import subprocess
import sys
import shutil
import time
from pathlib import Path

# -----------------------------------------------
#  Colores ANSI (funcionan en Windows 10+)
# -----------------------------------------------
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
WHITE  = "\033[97m"


def enable_ansi():
    """Activar colores ANSI en consola Windows."""
    if sys.platform == "win32":
        import ctypes
        kernel = ctypes.windll.kernel32
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)


def header():
    print()
    print(f"{BOLD}{CYAN}+------------------------------------------+{RESET}")
    print(f"{BOLD}{CYAN}|        STARFALL  --  Build Release       |{RESET}")
    print(f"{BOLD}{CYAN}+------------------------------------------+{RESET}")
    print()


def step(n: int, total: int, label: str):
    bar = f"[{n}/{total}]"
    print(f"{BOLD}{CYAN}{bar}{RESET} {WHITE}{label}{RESET}")


def ok(msg: str = ""):
    print(f"    {GREEN}OK{RESET}  {msg}" if msg else f"    {GREEN}OK{RESET}")


def fail(msg: str):
    print(f"    {RED}FAIL{RESET}  {RED}{msg}{RESET}")


def warn(msg: str):
    print(f"    {YELLOW}WARN{RESET}  {YELLOW}{msg}{RESET}")


def info(msg: str):
    print(f"    {DIM}{msg}{RESET}")


def separator():
    print(f"    {DIM}{'-' * 44}{RESET}")


def run(cmd: list, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def abort(reason: str):
    print()
    print(f"{RED}{BOLD}  BUILD ABORTADO: {reason}{RESET}")
    print()
    sys.exit(1)


# -----------------------------------------------
#  Configuracion
# -----------------------------------------------
ROOT   = Path(__file__).parent
DIST   = ROOT / "dist"
BUILD  = ROOT / "build"
SPEC   = ROOT / "Starfall.spec"
OUTPUT = DIST / "Starfall.exe"
TOTAL  = 5


# -----------------------------------------------
#  Paso 1: Requisitos
# -----------------------------------------------
def check_prerequisites():
    step(1, TOTAL, "Verificando requisitos")

    v = sys.version_info
    if v < (3, 12):
        fail(f"Se requiere Python 3.12+  (actual: {v.major}.{v.minor})")
        abort("version de Python insuficiente")
    ok(f"Python {v.major}.{v.minor}.{v.micro}")

    r = run([sys.executable, "-m", "PyInstaller", "--version"])
    if r.returncode != 0:
        fail("PyInstaller no encontrado")
        info("Instalar con:  pip install pyinstaller")
        abort("PyInstaller faltante")
    ok(f"PyInstaller {r.stdout.strip()}")

    r = run([sys.executable, "-c", "import pygame; print(pygame.version.ver)"])
    if r.returncode != 0:
        fail("pygame-ce no encontrado")
        info("Instalar con:  pip install pygame-ce")
        abort("pygame-ce faltante")
    ok(f"pygame-ce {r.stdout.strip()}")

    if not SPEC.exists():
        fail("Starfall.spec no encontrado")
        abort("spec file faltante")
    ok("Starfall.spec presente")

    print()


# -----------------------------------------------
#  Paso 2: Tests
# -----------------------------------------------
def run_tests():
    step(2, TOTAL, "Ejecutando tests")

    r = run([sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short"], cwd=ROOT)
    lines = (r.stdout + r.stderr).splitlines()
    summary = next((l for l in reversed(lines) if l.strip()), "")
    info(summary)

    if r.returncode != 0:
        separator()
        for line in lines:
            if "FAILED" in line or "ERROR" in line:
                info(f"  {line}")
        fail("Tests fallando -- build cancelado")
        abort("tests en rojo")

    ok("Todos los tests en verde")
    print()


# -----------------------------------------------
#  Paso 3: Limpieza
# -----------------------------------------------
def clean_previous():
    step(3, TOTAL, "Limpiando builds anteriores")

    cleaned = []
    for d in [DIST, BUILD]:
        if d.exists():
            shutil.rmtree(d)
            cleaned.append(d.name)

    if cleaned:
        ok(f"Eliminado: {', '.join(cleaned)}/")
    else:
        ok("Nada que limpiar")
    print()


# -----------------------------------------------
#  Paso 4: Compilacion
# -----------------------------------------------
def build_exe():
    step(4, TOTAL, "Compilando con PyInstaller")
    info("Esto puede tardar 30-60 segundos...")
    separator()

    start = time.time()
    r = run(
        [sys.executable, "-m", "PyInstaller", "Starfall.spec", "--noconfirm"],
        cwd=ROOT,
    )
    elapsed = time.time() - start

    for line in (r.stdout + r.stderr).splitlines():
        low = line.lower()
        if any(k in low for k in ["error", "warning", "info: building", "info: exe"]):
            tag = RED if "error" in low else (YELLOW if "warning" in low else DIM)
            info(f"{tag}{line}{RESET}")

    separator()

    if r.returncode != 0:
        fail("PyInstaller termino con error")
        abort("fallo en compilacion")

    ok(f"Compilado en {elapsed:.1f}s")
    print()


# -----------------------------------------------
#  Paso 5: Verificacion
# -----------------------------------------------
def verify_output():
    step(5, TOTAL, "Verificando resultado")

    if not OUTPUT.exists():
        fail(f"No se encontro {OUTPUT}")
        abort("ejecutable no generado")

    size_mb = OUTPUT.stat().st_size / (1024 * 1024)
    ok(f"Archivo generado: {OUTPUT}")
    ok(f"Tamano: {size_mb:.1f} MB")

    print()
    print(f"{BOLD}{GREEN}  +==========================================+{RESET}")
    print(f"{BOLD}{GREEN}  |           BUILD EXITOSO                  |{RESET}")
    print(f"{BOLD}{GREEN}  +==========================================+{RESET}")
    print()
    print(f"  {WHITE}Ejecutable listo en:{RESET}")
    print(f"  {CYAN}{OUTPUT}{RESET}")
    print()


# -----------------------------------------------

if __name__ == "__main__":
    enable_ansi()
    header()
    check_prerequisites()
    run_tests()
    clean_previous()
    build_exe()
    verify_output()
