"""Utilidades para verificar y solicitar permisos de administrador."""
import ctypes
import sys
import os


def es_administrador() -> bool:
    """Verifica si el script se está ejecutando como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def solicitar_admin():
    """Reinicia el script con permisos de administrador."""
    if not es_administrador():
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join([f'"{arg}"' for arg in sys.argv]),
            None,
            1
        )
        sys.exit(0)


def ejecutar_powershell(comando: str, como_admin: bool = True) -> tuple[bool, str]:
    """Ejecuta un comando de PowerShell y retorna el resultado."""
    import subprocess

    try:
        args = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command", comando
        ]

        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        salida = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""

        if result.returncode == 0:
            return True, salida
        else:
            return False, error or salida

    except Exception as e:
        return False, str(e)


def ejecutar_cmd(comando: str) -> tuple[bool, str]:
    """Ejecuta un comando de CMD y retorna el resultado."""
    import subprocess

    try:
        result = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        salida = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""

        return result.returncode == 0, salida or error

    except Exception as e:
        return False, str(e)
