"""Utilidades para verificar y solicitar permisos de administrador."""
import ctypes
import sys
import os
import subprocess

# Constantes para ocultar ventanas
CREATE_NO_WINDOW = 0x08000000
STARTF_USESHOWWINDOW = 0x00000001
SW_HIDE = 0


def es_administrador() -> bool:
    """Verifica si el script se está ejecutando como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def solicitar_admin():
    """Reinicia el script con permisos de administrador."""
    if not es_administrador():
        # Usar pythonw para no mostrar consola
        python_exe = sys.executable
        if python_exe.endswith('python.exe'):
            pythonw = python_exe.replace('python.exe', 'pythonw.exe')
            if os.path.exists(pythonw):
                python_exe = pythonw

        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            python_exe,
            " ".join([f'"{arg}"' for arg in sys.argv]),
            None,
            0  # SW_HIDE - ocultar ventana
        )
        sys.exit(0)


def _crear_startupinfo():
    """Crea un objeto STARTUPINFO para ocultar ventanas."""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = SW_HIDE
    return startupinfo


def ejecutar_powershell(comando: str, como_admin: bool = True) -> tuple[bool, str]:
    """Ejecuta un comando de PowerShell sin mostrar ventana y retorna el resultado."""
    try:
        # Configurar output como UTF-8
        comando_utf8 = f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {comando}"

        args = [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-WindowStyle", "Hidden",
            "-ExecutionPolicy", "Bypass",
            "-Command", comando_utf8
        ]

        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            creationflags=CREATE_NO_WINDOW,
            startupinfo=_crear_startupinfo(),
            timeout=300  # 5 minutos máximo
        )

        salida = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""

        # Considerar éxito si returncode es 0 o si hay salida válida
        if result.returncode == 0:
            return True, salida
        elif salida and not error:
            # Algunos comandos retornan código no-cero pero funcionan
            return True, salida
        else:
            return False, error or salida or "Error desconocido"

    except subprocess.TimeoutExpired:
        return False, "El comando excedió el tiempo límite"
    except Exception as e:
        return False, str(e)


def ejecutar_cmd(comando: str) -> tuple[bool, str]:
    """Ejecuta un comando de CMD sin mostrar ventana y retorna el resultado."""
    try:
        result = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            creationflags=CREATE_NO_WINDOW,
            startupinfo=_crear_startupinfo(),
            timeout=120  # 2 minutos máximo
        )

        salida = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""

        return result.returncode == 0, salida or error

    except subprocess.TimeoutExpired:
        return False, "El comando excedió el tiempo límite"
    except Exception as e:
        return False, str(e)


def ejecutar_reg(comando: str) -> tuple[bool, str]:
    """Ejecuta un comando de registro sin mostrar ventana."""
    try:
        result = subprocess.run(
            f"reg {comando}",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            creationflags=CREATE_NO_WINDOW,
            startupinfo=_crear_startupinfo()
        )

        salida = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""

        return result.returncode == 0, salida or error

    except Exception as e:
        return False, str(e)
