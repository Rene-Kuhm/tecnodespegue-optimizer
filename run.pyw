"""
Tecnodespegue Optimizer - Launcher sin consola
Ejecuta este archivo para iniciar la aplicación sin ventana de consola.
"""
import subprocess
import sys
import os

# Obtener la ruta del directorio actual
dir_path = os.path.dirname(os.path.abspath(__file__))

# Ejecutar main.py sin mostrar consola
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

subprocess.Popen(
    [sys.executable, os.path.join(dir_path, "main.py")],
    startupinfo=startupinfo,
    creationflags=subprocess.CREATE_NO_WINDOW
)
