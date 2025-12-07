"""Módulo para escanear, detectar y actualizar drivers del sistema."""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Callable
import re
from src.utils.admin import ejecutar_powershell, ejecutar_cmd


class EstadoDriver(Enum):
    """Estado del driver."""
    OK = "Actualizado"
    DESACTUALIZADO = "Desactualizado"
    FALTANTE = "Faltante"
    PROBLEMA = "Con problemas"
    DESCONOCIDO = "Desconocido"


class CategoriaDriver(Enum):
    """Categorías de drivers."""
    DISPLAY = "Pantalla/GPU"
    NETWORK = "Red"
    AUDIO = "Audio"
    USB = "USB"
    STORAGE = "Almacenamiento"
    SYSTEM = "Sistema"
    INPUT = "Entrada"
    BLUETOOTH = "Bluetooth"
    PRINTER = "Impresora"
    OTHER = "Otros"


@dataclass
class DriverInfo:
    """Información de un driver."""
    nombre: str
    dispositivo: str
    fabricante: str
    version: str
    fecha: str
    estado: EstadoDriver
    categoria: CategoriaDriver
    device_id: str
    inf_name: str = ""
    necesita_actualizacion: bool = False


@dataclass
class ResultadoEscaneo:
    """Resultado del escaneo de drivers."""
    total: int
    actualizados: int
    desactualizados: int
    faltantes: int
    con_problemas: int
    drivers: List[DriverInfo]


def _categorizar_driver(nombre: str, clase: str) -> CategoriaDriver:
    """Determina la categoría del driver basándose en su nombre y clase."""
    nombre_lower = nombre.lower()
    clase_lower = clase.lower()

    if any(x in nombre_lower or x in clase_lower for x in ['display', 'graphics', 'gpu', 'nvidia', 'amd', 'intel', 'video', 'vga']):
        return CategoriaDriver.DISPLAY
    elif any(x in nombre_lower or x in clase_lower for x in ['network', 'ethernet', 'wifi', 'wireless', 'lan', 'net']):
        return CategoriaDriver.NETWORK
    elif any(x in nombre_lower or x in clase_lower for x in ['audio', 'sound', 'realtek', 'speaker']):
        return CategoriaDriver.AUDIO
    elif any(x in nombre_lower or x in clase_lower for x in ['usb', 'hub']):
        return CategoriaDriver.USB
    elif any(x in nombre_lower or x in clase_lower for x in ['storage', 'disk', 'nvme', 'ssd', 'hdd', 'sata', 'raid']):
        return CategoriaDriver.STORAGE
    elif any(x in nombre_lower or x in clase_lower for x in ['bluetooth', 'bt']):
        return CategoriaDriver.BLUETOOTH
    elif any(x in nombre_lower or x in clase_lower for x in ['keyboard', 'mouse', 'hid', 'input', 'touchpad']):
        return CategoriaDriver.INPUT
    elif any(x in nombre_lower or x in clase_lower for x in ['print', 'scanner']):
        return CategoriaDriver.PRINTER
    elif any(x in nombre_lower or x in clase_lower for x in ['system', 'processor', 'acpi', 'pci']):
        return CategoriaDriver.SYSTEM
    else:
        return CategoriaDriver.OTHER


def escanear_drivers(callback: Optional[Callable[[str, int], None]] = None) -> ResultadoEscaneo:
    """
    Escanea todos los drivers del sistema.

    Args:
        callback: Función para reportar progreso (mensaje, porcentaje)

    Returns:
        ResultadoEscaneo con la lista de drivers encontrados
    """
    drivers: List[DriverInfo] = []

    if callback:
        callback("Obteniendo lista de dispositivos...", 10)

    # Obtener todos los dispositivos con sus drivers
    comando_drivers = """
    Get-WmiObject Win32_PnPSignedDriver | Where-Object { $_.DeviceName -ne $null } |
    Select-Object DeviceName, Manufacturer, DriverVersion, DriverDate, DeviceClass, DeviceID, InfName, IsSigned |
    ConvertTo-Json -Compress
    """

    exito, salida = ejecutar_powershell(comando_drivers)

    if callback:
        callback("Analizando drivers instalados...", 30)

    if exito and salida:
        try:
            import json
            datos = json.loads(salida)

            # Asegurar que sea una lista
            if isinstance(datos, dict):
                datos = [datos]

            for i, d in enumerate(datos):
                if callback and i % 20 == 0:
                    progreso = 30 + int((i / len(datos)) * 40)
                    callback(f"Procesando driver {i+1} de {len(datos)}...", progreso)

                nombre = d.get('DeviceName', 'Desconocido') or 'Desconocido'
                fabricante = d.get('Manufacturer', 'Desconocido') or 'Desconocido'
                version = d.get('DriverVersion', 'N/A') or 'N/A'
                fecha_raw = d.get('DriverDate', '')
                clase = d.get('DeviceClass', '') or ''
                device_id = d.get('DeviceID', '') or ''
                inf_name = d.get('InfName', '') or ''

                # Parsear fecha
                fecha = "N/A"
                if fecha_raw:
                    try:
                        # Formato: 20231115000000.000000-000
                        match = re.match(r'(\d{4})(\d{2})(\d{2})', str(fecha_raw))
                        if match:
                            fecha = f"{match.group(3)}/{match.group(2)}/{match.group(1)}"
                    except:
                        pass

                # Determinar estado
                estado = EstadoDriver.OK
                if not version or version == 'N/A':
                    estado = EstadoDriver.FALTANTE
                elif not d.get('IsSigned', True):
                    estado = EstadoDriver.PROBLEMA

                categoria = _categorizar_driver(nombre, clase)

                driver = DriverInfo(
                    nombre=nombre,
                    dispositivo=nombre,
                    fabricante=fabricante,
                    version=version,
                    fecha=fecha,
                    estado=estado,
                    categoria=categoria,
                    device_id=device_id,
                    inf_name=inf_name,
                    necesita_actualizacion=estado != EstadoDriver.OK
                )
                drivers.append(driver)

        except json.JSONDecodeError:
            pass

    if callback:
        callback("Verificando dispositivos con problemas...", 75)

    # Buscar dispositivos con problemas (código de error != 0)
    comando_problemas = """
    Get-WmiObject Win32_PnPEntity | Where-Object { $_.ConfigManagerErrorCode -ne 0 } |
    Select-Object Name, DeviceID, ConfigManagerErrorCode |
    ConvertTo-Json -Compress
    """

    exito_prob, salida_prob = ejecutar_powershell(comando_problemas)

    if exito_prob and salida_prob:
        try:
            import json
            problemas = json.loads(salida_prob)

            if isinstance(problemas, dict):
                problemas = [problemas]

            for p in problemas:
                device_id = p.get('DeviceID', '')
                nombre = p.get('Name', 'Dispositivo desconocido')
                error_code = p.get('ConfigManagerErrorCode', 0)

                # Verificar si ya existe
                existe = False
                for d in drivers:
                    if d.device_id == device_id:
                        d.estado = EstadoDriver.PROBLEMA
                        d.necesita_actualizacion = True
                        existe = True
                        break

                if not existe and error_code == 28:  # Driver no instalado
                    driver = DriverInfo(
                        nombre=nombre,
                        dispositivo=nombre,
                        fabricante="Desconocido",
                        version="No instalado",
                        fecha="N/A",
                        estado=EstadoDriver.FALTANTE,
                        categoria=CategoriaDriver.OTHER,
                        device_id=device_id,
                        necesita_actualizacion=True
                    )
                    drivers.append(driver)

        except json.JSONDecodeError:
            pass

    if callback:
        callback("Finalizando escaneo...", 95)

    # Calcular estadísticas
    actualizados = sum(1 for d in drivers if d.estado == EstadoDriver.OK)
    desactualizados = sum(1 for d in drivers if d.estado == EstadoDriver.DESACTUALIZADO)
    faltantes = sum(1 for d in drivers if d.estado == EstadoDriver.FALTANTE)
    con_problemas = sum(1 for d in drivers if d.estado == EstadoDriver.PROBLEMA)

    if callback:
        callback("Escaneo completado", 100)

    return ResultadoEscaneo(
        total=len(drivers),
        actualizados=actualizados,
        desactualizados=desactualizados,
        faltantes=faltantes,
        con_problemas=con_problemas,
        drivers=drivers
    )


def buscar_actualizaciones_windows(callback: Optional[Callable[[str, int], None]] = None) -> tuple[bool, str]:
    """
    Busca actualizaciones de drivers a través de Windows Update.

    Returns:
        (exito, mensaje)
    """
    if callback:
        callback("Buscando actualizaciones en Windows Update...", 20)

    comando = """
    $UpdateSession = New-Object -ComObject Microsoft.Update.Session
    $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
    $Updates = $UpdateSearcher.Search("IsInstalled=0 and Type='Driver'")

    if ($Updates.Updates.Count -eq 0) {
        Write-Output "NO_UPDATES"
    } else {
        $Updates.Updates | ForEach-Object {
            Write-Output "$($_.Title)"
        }
    }
    """

    exito, salida = ejecutar_powershell(comando)

    if callback:
        callback("Búsqueda completada", 100)

    if exito:
        if "NO_UPDATES" in salida:
            return True, "No hay actualizaciones de drivers disponibles"
        else:
            updates = [line for line in salida.split('\n') if line.strip()]
            return True, f"Se encontraron {len(updates)} actualizaciones disponibles"

    return False, "Error al buscar actualizaciones"


def actualizar_driver_windows_update(device_id: str, callback: Optional[Callable[[str, int], None]] = None) -> tuple[bool, str]:
    """
    Intenta actualizar un driver específico usando Windows Update.

    Args:
        device_id: ID del dispositivo
        callback: Función de progreso

    Returns:
        (exito, mensaje)
    """
    if callback:
        callback("Buscando driver en Windows Update...", 20)

    # Usar pnputil para buscar y actualizar driver
    comando = f'pnputil /scan-devices'
    exito1, _ = ejecutar_cmd(comando)

    if callback:
        callback("Instalando driver...", 60)

    # Intentar actualizar el driver específico
    comando_update = f"""
    $device = Get-PnpDevice | Where-Object {{ $_.InstanceId -eq '{device_id}' }}
    if ($device) {{
        $result = pnputil /add-driver C:\\Windows\\INF\\*.inf /subdirs /install 2>&1
        Write-Output "UPDATE_ATTEMPTED"
    }} else {{
        Write-Output "DEVICE_NOT_FOUND"
    }}
    """

    exito, salida = ejecutar_powershell(comando_update)

    if callback:
        callback("Proceso completado", 100)

    if "UPDATE_ATTEMPTED" in salida:
        return True, "Se intentó actualizar el driver. Reinicia para aplicar cambios."
    elif "DEVICE_NOT_FOUND" in salida:
        return False, "Dispositivo no encontrado"

    return False, "No se pudo actualizar el driver"


def actualizar_todos_drivers(callback: Optional[Callable[[str, int], None]] = None) -> tuple[int, int, str]:
    """
    Actualiza todos los drivers posibles usando Windows Update.

    Returns:
        (exitosos, fallidos, mensaje)
    """
    if callback:
        callback("Escaneando dispositivos...", 10)

    # Escanear dispositivos para detectar nuevos
    ejecutar_cmd("pnputil /scan-devices")

    if callback:
        callback("Buscando actualizaciones de drivers...", 30)

    # Buscar e instalar actualizaciones de drivers
    comando = """
    $UpdateSession = New-Object -ComObject Microsoft.Update.Session
    $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
    $Updates = $UpdateSearcher.Search("IsInstalled=0 and Type='Driver'")

    if ($Updates.Updates.Count -eq 0) {
        Write-Output "NO_UPDATES:0"
    } else {
        $Downloader = $UpdateSession.CreateUpdateDownloader()
        $Downloader.Updates = $Updates.Updates
        $Downloader.Download()

        $Installer = $UpdateSession.CreateUpdateInstaller()
        $Installer.Updates = $Updates.Updates
        $Result = $Installer.Install()

        $success = ($Updates.Updates | Where-Object { $_.IsInstalled }).Count
        Write-Output "INSTALLED:$success"
    }
    """

    if callback:
        callback("Descargando e instalando drivers...", 60)

    exito, salida = ejecutar_powershell(comando)

    if callback:
        callback("Proceso completado", 100)

    if "NO_UPDATES" in salida:
        return 0, 0, "Todos los drivers están actualizados"
    elif "INSTALLED:" in salida:
        try:
            count = int(salida.split("INSTALLED:")[1].strip())
            return count, 0, f"Se actualizaron {count} drivers"
        except:
            pass

    return 0, 0, "Proceso completado"


def exportar_reporte_drivers(drivers: List[DriverInfo], ruta: str) -> tuple[bool, str]:
    """
    Exporta un reporte de drivers a un archivo.

    Args:
        drivers: Lista de drivers
        ruta: Ruta del archivo de salida

    Returns:
        (exito, mensaje)
    """
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("  REPORTE DE DRIVERS - TECNODESPEGUE OPTIMIZER\n")
            f.write("=" * 70 + "\n\n")

            # Estadísticas
            total = len(drivers)
            ok = sum(1 for d in drivers if d.estado == EstadoDriver.OK)
            problemas = sum(1 for d in drivers if d.estado in [EstadoDriver.FALTANTE, EstadoDriver.PROBLEMA])

            f.write(f"Total de drivers: {total}\n")
            f.write(f"Drivers OK: {ok}\n")
            f.write(f"Drivers con problemas: {problemas}\n\n")

            f.write("-" * 70 + "\n")
            f.write("DETALLE DE DRIVERS\n")
            f.write("-" * 70 + "\n\n")

            for cat in CategoriaDriver:
                drivers_cat = [d for d in drivers if d.categoria == cat]
                if drivers_cat:
                    f.write(f"\n[{cat.value}]\n")
                    f.write("-" * 40 + "\n")
                    for d in drivers_cat:
                        estado_icon = "✓" if d.estado == EstadoDriver.OK else "✗"
                        f.write(f"  {estado_icon} {d.nombre}\n")
                        f.write(f"    Fabricante: {d.fabricante}\n")
                        f.write(f"    Versión: {d.version}\n")
                        f.write(f"    Fecha: {d.fecha}\n")
                        f.write(f"    Estado: {d.estado.value}\n\n")

        return True, f"Reporte exportado a {ruta}"
    except Exception as e:
        return False, str(e)


def obtener_info_gpu() -> dict:
    """Obtiene información detallada de la GPU."""
    comando = """
    Get-WmiObject Win32_VideoController | Select-Object Name, DriverVersion, DriverDate, AdapterRAM, VideoProcessor |
    ConvertTo-Json -Compress
    """

    exito, salida = ejecutar_powershell(comando)

    if exito and salida:
        try:
            import json
            datos = json.loads(salida)
            if isinstance(datos, dict):
                datos = [datos]
            return datos[0] if datos else {}
        except:
            pass

    return {}
