"""Información del sistema Windows."""
import platform
import psutil
from dataclasses import dataclass


@dataclass
class InfoSistema:
    """Información del sistema."""
    nombre_pc: str
    version_windows: str
    build: str
    arquitectura: str
    cpu: str
    nucleos: int
    ram_total_gb: float
    ram_disponible_gb: float
    ram_uso_porcentaje: float
    disco_total_gb: float
    disco_libre_gb: float


def obtener_info_sistema() -> InfoSistema:
    """Obtiene información completa del sistema."""
    import subprocess

    # Obtener build de Windows
    try:
        result = subprocess.run(
            ["powershell", "-Command", "(Get-CimInstance Win32_OperatingSystem).BuildNumber"],
            capture_output=True, text=True
        )
        build = result.stdout.strip()
    except:
        build = "Desconocido"

    # Obtener nombre del CPU
    try:
        result = subprocess.run(
            ["powershell", "-Command", "(Get-CimInstance Win32_Processor).Name"],
            capture_output=True, text=True
        )
        cpu = result.stdout.strip()
    except:
        cpu = platform.processor()

    # RAM
    mem = psutil.virtual_memory()
    ram_total = mem.total / (1024 ** 3)
    ram_disponible = mem.available / (1024 ** 3)

    # Disco principal
    disco = psutil.disk_usage('C:')
    disco_total = disco.total / (1024 ** 3)
    disco_libre = disco.free / (1024 ** 3)

    return InfoSistema(
        nombre_pc=platform.node(),
        version_windows=platform.version(),
        build=build,
        arquitectura=platform.machine(),
        cpu=cpu,
        nucleos=psutil.cpu_count(logical=True),
        ram_total_gb=round(ram_total, 2),
        ram_disponible_gb=round(ram_disponible, 2),
        ram_uso_porcentaje=mem.percent,
        disco_total_gb=round(disco_total, 2),
        disco_libre_gb=round(disco_libre, 2)
    )


def obtener_uso_cpu() -> float:
    """Obtiene el uso actual de CPU."""
    return psutil.cpu_percent(interval=1)


def obtener_procesos_top(limite: int = 10) -> list[dict]:
    """Obtiene los procesos con mayor consumo de recursos."""
    procesos = []

    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
        try:
            info = proc.info
            procesos.append({
                'pid': info['pid'],
                'nombre': info['name'],
                'memoria_mb': round(info['memory_info'].rss / (1024 * 1024), 2),
                'cpu': info['cpu_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Ordenar por memoria
    procesos.sort(key=lambda x: x['memoria_mb'], reverse=True)
    return procesos[:limite]
