"""
Script para compilar Tecnodespegue Optimizer a un ejecutable portable.
Ejecutar: python build_exe.py
"""
import subprocess
import sys
import os

def build():
    print("=" * 60)
    print("  Tecnodespegue Optimizer - Compilador a EXE")
    print("=" * 60)
    print()

    # Directorio del proyecto
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    print("[1/3] Verificando dependencias...")

    # Verificar PyInstaller
    try:
        import PyInstaller
        print(f"      PyInstaller {PyInstaller.__version__} encontrado")
    except ImportError:
        print("      Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"])

    print("[2/3] Compilando ejecutable...")
    print("      Esto puede tomar varios minutos...")
    print()

    # Comando de PyInstaller con flet
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=TecnodespegueOptimizer",
        "--onefile",           # Un solo archivo exe
        "--windowed",          # Sin consola
        "--clean",             # Limpiar cache
        "--noconfirm",         # No preguntar
        "--add-data", "src;src",  # Incluir carpeta src
        # Solicitar admin al ejecutar
        "--uac-admin",
        "main.py"
    ]

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print()
        print("[3/3] Compilación exitosa!")
        print()
        print("=" * 60)
        exe_path = os.path.join(project_dir, "dist", "TecnodespegueOptimizer.exe")
        print(f"  Ejecutable creado en:")
        print(f"  {exe_path}")
        print()
        print("  Puedes copiar este archivo a cualquier PC")
        print("  No requiere Python instalado")
        print("=" * 60)
    else:
        print()
        print("[ERROR] La compilación falló")
        print("Intenta ejecutar manualmente:")
        print("  flet pack main.py --name TecnodespegueOptimizer --uac-admin")

if __name__ == "__main__":
    build()
