"""Módulo de limpieza del sistema."""
import os
import shutil
from dataclasses import dataclass
from src.utils.admin import ejecutar_powershell, ejecutar_cmd


@dataclass
class ResultadoLimpieza:
    """Resultado de una operación de limpieza."""
    nombre: str
    espacio_liberado_mb: float
    archivos_eliminados: int
    exito: bool
    mensaje: str = ""


def limpiar_temp_usuario() -> ResultadoLimpieza:
    """Limpia archivos temporales del usuario."""
    ruta = os.environ.get('TEMP', '')
    return _limpiar_directorio(ruta, "Temp Usuario")


def limpiar_temp_windows() -> ResultadoLimpieza:
    """Limpia archivos temporales de Windows."""
    ruta = "C:\\Windows\\Temp"
    return _limpiar_directorio(ruta, "Temp Windows")


def limpiar_prefetch() -> ResultadoLimpieza:
    """Limpia archivos Prefetch."""
    ruta = "C:\\Windows\\Prefetch"
    return _limpiar_directorio(ruta, "Prefetch")


def limpiar_cache_windows_update() -> ResultadoLimpieza:
    """Limpia caché de Windows Update."""
    ruta = "C:\\Windows\\SoftwareDistribution\\Download"

    # Calcular tamaño antes de limpiar
    tamano_antes = _obtener_tamano_directorio(ruta) if os.path.exists(ruta) else 0

    cmd = '''
    # Detener el servicio de Windows Update
    $wu = Get-Service -Name "wuauserv" -ErrorAction SilentlyContinue
    if ($wu -and $wu.Status -eq 'Running') {
        Stop-Service -Name "wuauserv" -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    }

    # Limpiar caché
    if (Test-Path "C:\\Windows\\SoftwareDistribution\\Download") {
        Remove-Item -Path "C:\\Windows\\SoftwareDistribution\\Download\\*" -Recurse -Force -ErrorAction SilentlyContinue
    }

    # Reiniciar servicio
    Start-Service -Name "wuauserv" -ErrorAction SilentlyContinue
    Write-Output "DONE"
    '''

    exito, salida = ejecutar_powershell(cmd)

    # Calcular espacio liberado
    tamano_despues = _obtener_tamano_directorio(ruta) if os.path.exists(ruta) else 0
    espacio_liberado = max(0, tamano_antes - tamano_despues)

    return ResultadoLimpieza(
        nombre="Caché Windows Update",
        espacio_liberado_mb=round(espacio_liberado, 2),
        archivos_eliminados=0,
        exito="DONE" in salida or exito,
        mensaje="Caché limpiada correctamente" if exito else "Error parcial al limpiar"
    )


def limpiar_thumbnails() -> ResultadoLimpieza:
    """Limpia caché de miniaturas."""
    ruta = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Explorer')

    archivos = 0
    tamano = 0

    if os.path.exists(ruta):
        for archivo in os.listdir(ruta):
            if archivo.startswith('thumbcache_') and archivo.endswith('.db'):
                archivo_path = os.path.join(ruta, archivo)
                try:
                    tamano += os.path.getsize(archivo_path) / (1024 * 1024)
                    os.remove(archivo_path)
                    archivos += 1
                except:
                    pass

    return ResultadoLimpieza(
        nombre="Caché de Miniaturas",
        espacio_liberado_mb=round(tamano, 2),
        archivos_eliminados=archivos,
        exito=True
    )


def limpiar_cache_navegadores() -> ResultadoLimpieza:
    """Limpia caché de navegadores comunes."""
    rutas = [
        # Chrome
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
        # Edge
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
        # Firefox
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Mozilla', 'Firefox', 'Profiles'),
    ]

    total_tamano = 0
    total_archivos = 0

    for ruta in rutas:
        if os.path.exists(ruta):
            resultado = _limpiar_directorio(ruta, "temp")
            total_tamano += resultado.espacio_liberado_mb
            total_archivos += resultado.archivos_eliminados

    return ResultadoLimpieza(
        nombre="Caché de Navegadores",
        espacio_liberado_mb=round(total_tamano, 2),
        archivos_eliminados=total_archivos,
        exito=True
    )


def limpiar_papelera() -> ResultadoLimpieza:
    """Vacía la papelera de reciclaje."""
    cmd = "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
    exito, _ = ejecutar_powershell(cmd)
    return ResultadoLimpieza(
        nombre="Papelera de Reciclaje",
        espacio_liberado_mb=0,  # No podemos calcular fácilmente
        archivos_eliminados=0,
        exito=exito,
        mensaje="Papelera vaciada" if exito else "Error al vaciar"
    )


def limpiar_logs_windows() -> ResultadoLimpieza:
    """Limpia logs antiguos de Windows."""
    rutas = [
        "C:\\Windows\\Logs\\CBS",
        "C:\\Windows\\Logs\\DISM",
    ]

    total_tamano = 0
    total_archivos = 0

    for ruta in rutas:
        if os.path.exists(ruta):
            resultado = _limpiar_directorio(ruta, "temp")
            total_tamano += resultado.espacio_liberado_mb
            total_archivos += resultado.archivos_eliminados

    return ResultadoLimpieza(
        nombre="Logs de Windows",
        espacio_liberado_mb=round(total_tamano, 2),
        archivos_eliminados=total_archivos,
        exito=True
    )


def ejecutar_limpieza_disco() -> ResultadoLimpieza:
    """Ejecuta el limpiador de disco de Windows."""
    # Configurar limpieza automática con todas las opciones
    cmd = '''
    # Configurar opciones de limpieza
    $volumeCache = "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VolumeCaches"
    $cacheTypes = @(
        "Temporary Files",
        "Temporary Setup Files",
        "Old ChkDsk Files",
        "Setup Log Files",
        "System error memory dump files",
        "System error minidump files",
        "Windows Error Reporting Files",
        "Thumbnail Cache",
        "Update Cleanup"
    )

    foreach ($cache in $cacheTypes) {
        $path = Join-Path $volumeCache $cache
        if (Test-Path $path) {
            Set-ItemProperty -Path $path -Name "StateFlags0100" -Value 2 -Type DWord -Force -ErrorAction SilentlyContinue
        }
    }

    # Ejecutar limpieza
    Start-Process -FilePath "cleanmgr.exe" -ArgumentList "/sagerun:100" -Wait -NoNewWindow
    '''
    exito, _ = ejecutar_powershell(cmd)
    return ResultadoLimpieza(
        nombre="Limpieza de Disco de Windows",
        espacio_liberado_mb=0,
        archivos_eliminados=0,
        exito=exito,
        mensaje="Limpieza ejecutada" if exito else "Error al ejecutar"
    )


def ejecutar_limpieza_completa() -> list[ResultadoLimpieza]:
    """Ejecuta todas las limpiezas y retorna los resultados."""
    resultados = [
        limpiar_temp_usuario(),
        limpiar_temp_windows(),
        limpiar_prefetch(),
        limpiar_cache_windows_update(),
        limpiar_thumbnails(),
        limpiar_logs_windows(),
        limpiar_papelera(),
    ]
    return resultados


def _limpiar_directorio(ruta: str, nombre: str) -> ResultadoLimpieza:
    """Limpia un directorio y retorna estadísticas."""
    if not os.path.exists(ruta):
        return ResultadoLimpieza(nombre, 0, 0, True, "Directorio no existe")

    tamano_total = 0
    archivos_eliminados = 0

    for root, dirs, files in os.walk(ruta):
        for archivo in files:
            archivo_path = os.path.join(root, archivo)
            try:
                tamano_total += os.path.getsize(archivo_path)
                os.remove(archivo_path)
                archivos_eliminados += 1
            except:
                pass

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                shutil.rmtree(dir_path, ignore_errors=True)
            except:
                pass

    return ResultadoLimpieza(
        nombre=nombre,
        espacio_liberado_mb=round(tamano_total / (1024 * 1024), 2),
        archivos_eliminados=archivos_eliminados,
        exito=True
    )


def _obtener_tamano_directorio(ruta: str) -> float:
    """Obtiene el tamaño de un directorio en MB."""
    total = 0
    if os.path.exists(ruta):
        for root, dirs, files in os.walk(ruta):
            for archivo in files:
                try:
                    total += os.path.getsize(os.path.join(root, archivo))
                except:
                    pass
    return round(total / (1024 * 1024), 2)
