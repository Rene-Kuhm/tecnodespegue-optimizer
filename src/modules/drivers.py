"""Módulo para escanear, detectar y actualizar drivers del sistema."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Callable, Dict
import re
import os
import tempfile
import urllib.request
import zipfile
import subprocess
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
    hardware_id: str = ""


@dataclass
class ResultadoEscaneo:
    """Resultado del escaneo de drivers."""
    total: int
    actualizados: int
    desactualizados: int
    faltantes: int
    con_problemas: int
    drivers: List[DriverInfo]
    todos_ok: bool = False


# URLs de drivers de fabricantes conocidos
DRIVER_SOURCES = {
    "intel": {
        "dsa": "https://dsadata.intel.com/installer",  # Intel Driver & Support Assistant
        "chipset": "https://downloadmirror.intel.com/",
    },
    "realtek": {
        "audio": "https://www.realtek.com/en/downloads",
    },
    "nvidia": {
        "geforce": "https://www.nvidia.com/Download/index.aspx",
    },
    "amd": {
        "adrenalin": "https://www.amd.com/en/support",
    }
}


def _categorizar_driver(nombre: str, clase: str) -> CategoriaDriver:
    """Determina la categoría del driver basándose en su nombre y clase."""
    nombre_lower = (nombre or "").lower()
    clase_lower = (clase or "").lower()

    if any(x in nombre_lower or x in clase_lower for x in ['display', 'graphics', 'gpu', 'nvidia', 'amd', 'intel hd', 'intel uhd', 'intel iris', 'video', 'vga', 'geforce', 'radeon']):
        return CategoriaDriver.DISPLAY
    elif any(x in nombre_lower or x in clase_lower for x in ['network', 'ethernet', 'wifi', 'wireless', 'lan', 'net', 'wi-fi', '802.11']):
        return CategoriaDriver.NETWORK
    elif any(x in nombre_lower or x in clase_lower for x in ['audio', 'sound', 'realtek', 'speaker', 'headphone', 'microphone']):
        return CategoriaDriver.AUDIO
    elif any(x in nombre_lower or x in clase_lower for x in ['usb', 'hub']):
        return CategoriaDriver.USB
    elif any(x in nombre_lower or x in clase_lower for x in ['storage', 'disk', 'nvme', 'ssd', 'hdd', 'sata', 'raid', 'ahci']):
        return CategoriaDriver.STORAGE
    elif any(x in nombre_lower or x in clase_lower for x in ['bluetooth', 'bt']):
        return CategoriaDriver.BLUETOOTH
    elif any(x in nombre_lower or x in clase_lower for x in ['keyboard', 'mouse', 'hid', 'input', 'touchpad', 'trackpad']):
        return CategoriaDriver.INPUT
    elif any(x in nombre_lower or x in clase_lower for x in ['print', 'scanner']):
        return CategoriaDriver.PRINTER
    elif any(x in nombre_lower or x in clase_lower for x in ['system', 'processor', 'acpi', 'pci', 'smbus', 'management engine']):
        return CategoriaDriver.SYSTEM
    else:
        return CategoriaDriver.OTHER


def _identificar_fabricante(nombre: str, hardware_id: str) -> str:
    """Identifica el fabricante basándose en el nombre y hardware ID."""
    texto = f"{nombre} {hardware_id}".lower()

    if 'intel' in texto or 'ven_8086' in texto.replace('&', '_'):
        return "Intel"
    elif 'nvidia' in texto or 'ven_10de' in texto.replace('&', '_'):
        return "NVIDIA"
    elif 'amd' in texto or 'ati' in texto or 'ven_1002' in texto.replace('&', '_'):
        return "AMD"
    elif 'realtek' in texto or 'ven_10ec' in texto.replace('&', '_'):
        return "Realtek"
    elif 'qualcomm' in texto or 'atheros' in texto:
        return "Qualcomm"
    elif 'broadcom' in texto:
        return "Broadcom"
    elif 'microsoft' in texto:
        return "Microsoft"

    return "Desconocido"


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
    Select-Object DeviceName, Manufacturer, DriverVersion, DriverDate, DeviceClass, DeviceID, InfName, IsSigned, HardWareID |
    ConvertTo-Json -Compress
    """

    exito, salida = ejecutar_powershell(comando_drivers)

    if callback:
        callback("Analizando drivers instalados...", 30)

    if exito and salida and salida.strip() not in ['', '[]', 'null']:
        try:
            import json
            datos = json.loads(salida)

            if isinstance(datos, dict):
                datos = [datos]

            total_drivers = len(datos)
            for i, d in enumerate(datos):
                if callback and i % 20 == 0:
                    progreso = 30 + int((i / max(total_drivers, 1)) * 40)
                    callback(f"Procesando driver {i+1} de {total_drivers}...", progreso)

                nombre = d.get('DeviceName') or 'Desconocido'
                if not nombre or nombre == 'Desconocido':
                    continue  # Saltar dispositivos sin nombre

                fabricante = d.get('Manufacturer') or 'Desconocido'
                version = d.get('DriverVersion') or 'N/A'
                fecha_raw = d.get('DriverDate', '')
                clase = d.get('DeviceClass') or ''
                device_id = d.get('DeviceID') or ''
                inf_name = d.get('InfName') or ''
                hardware_id = d.get('HardWareID') or ''

                # Manejar HardwareID que puede ser lista o string
                if isinstance(hardware_id, list):
                    hardware_id = hardware_id[0] if hardware_id else ''

                # Parsear fecha
                fecha = "N/A"
                if fecha_raw:
                    try:
                        # La fecha puede venir en formato WMI: yyyymmdd000000.000000+000
                        fecha_str = str(fecha_raw)
                        if len(fecha_str) >= 8:
                            match = re.match(r'(\d{4})(\d{2})(\d{2})', fecha_str)
                            if match:
                                fecha = f"{match.group(3)}/{match.group(2)}/{match.group(1)}"
                    except Exception:
                        pass

                # Determinar estado
                estado = EstadoDriver.OK
                if not version or version == 'N/A':
                    estado = EstadoDriver.FALTANTE
                elif not d.get('IsSigned', True):
                    estado = EstadoDriver.PROBLEMA

                # Identificar fabricante si no está disponible
                if fabricante == 'Desconocido' or not fabricante:
                    fabricante = _identificar_fabricante(nombre, hardware_id)

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
                    hardware_id=hardware_id,
                    necesita_actualizacion=estado != EstadoDriver.OK
                )
                drivers.append(driver)

        except json.JSONDecodeError:
            pass
        except Exception:
            pass

    if callback:
        callback("Verificando dispositivos con problemas...", 75)

    # Buscar dispositivos con problemas
    comando_problemas = """
    Get-PnpDevice | Where-Object { $_.Problem -ne 0 -or $_.Status -eq 'Error' -or $_.Status -eq 'Unknown' } |
    Select-Object InstanceId, FriendlyName, Class, Problem, Status, HardwareID |
    ConvertTo-Json -Compress
    """

    exito_prob, salida_prob = ejecutar_powershell(comando_problemas)

    if exito_prob and salida_prob and salida_prob.strip() not in ['', '[]', 'null']:
        try:
            import json
            problemas = json.loads(salida_prob)

            if isinstance(problemas, dict):
                problemas = [problemas]

            for p in problemas:
                device_id = p.get('InstanceId') or ''
                nombre = p.get('FriendlyName') or 'Dispositivo desconocido'
                error_code = p.get('Problem') or 0
                hardware_ids = p.get('HardwareID') or []
                hardware_id = hardware_ids[0] if hardware_ids else ''

                # Verificar si ya existe
                existe = False
                for d in drivers:
                    if d.device_id == device_id:
                        if error_code == 28:
                            d.estado = EstadoDriver.FALTANTE
                        else:
                            d.estado = EstadoDriver.PROBLEMA
                        d.necesita_actualizacion = True
                        existe = True
                        break

                if not existe:
                    fabricante = _identificar_fabricante(nombre, hardware_id)
                    estado = EstadoDriver.FALTANTE if error_code == 28 else EstadoDriver.PROBLEMA

                    driver = DriverInfo(
                        nombre=nombre,
                        dispositivo=nombre,
                        fabricante=fabricante,
                        version="No instalado",
                        fecha="N/A",
                        estado=estado,
                        categoria=CategoriaDriver.OTHER,
                        device_id=device_id,
                        hardware_id=hardware_id,
                        necesita_actualizacion=True
                    )
                    drivers.append(driver)

        except:
            pass

    if callback:
        callback("Finalizando escaneo...", 95)

    # Calcular estadísticas
    actualizados = sum(1 for d in drivers if d.estado == EstadoDriver.OK)
    desactualizados = sum(1 for d in drivers if d.estado == EstadoDriver.DESACTUALIZADO)
    faltantes = sum(1 for d in drivers if d.estado == EstadoDriver.FALTANTE)
    con_problemas = sum(1 for d in drivers if d.estado == EstadoDriver.PROBLEMA)
    todos_ok = faltantes == 0 and con_problemas == 0

    if callback:
        callback("Escaneo completado", 100)

    return ResultadoEscaneo(
        total=len(drivers),
        actualizados=actualizados,
        desactualizados=desactualizados,
        faltantes=faltantes,
        con_problemas=con_problemas,
        drivers=drivers,
        todos_ok=todos_ok
    )


def _descargar_intel_dsa(callback: Optional[Callable[[str, int], None]] = None) -> tuple[bool, str]:
    """Descarga e instala Intel Driver & Support Assistant."""
    if callback:
        callback("Descargando Intel Driver & Support Assistant...", 10)

    try:
        # URL del instalador de Intel DSA
        url = "https://dsadata.intel.com/installer"
        temp_dir = tempfile.gettempdir()
        installer_path = os.path.join(temp_dir, "Intel-Driver-and-Support-Assistant-Installer.exe")

        # Descargar
        urllib.request.urlretrieve(url, installer_path)

        if callback:
            callback("Instalando Intel DSA...", 50)

        # Ejecutar instalador silencioso
        result = subprocess.run(
            [installer_path, "/quiet", "/norestart"],
            capture_output=True,
            timeout=300
        )

        if callback:
            callback("Intel DSA instalado", 100)

        return True, "Intel Driver & Support Assistant instalado. Ábrelo para actualizar drivers Intel."
    except Exception as e:
        return False, f"Error: {str(e)}"


def _instalar_driver_via_devcon(hardware_id: str, inf_path: str) -> tuple[bool, str]:
    """Instala un driver usando el hardware ID."""
    comando = f'''
    $infPath = "{inf_path}"
    $hwid = "{hardware_id}"

    # Usar pnputil para instalar el driver
    $result = & pnputil /add-driver $infPath /install 2>&1

    if ($LASTEXITCODE -eq 0) {{
        Write-Output "SUCCESS"
    }} else {{
        Write-Output "FAILED: $result"
    }}
    '''

    exito, salida = ejecutar_powershell(comando)

    if "SUCCESS" in salida:
        return True, "Driver instalado correctamente"
    return False, salida


def actualizar_todos_drivers(
    callback: Optional[Callable[[str, int], None]] = None,
    on_driver_installed: Optional[Callable[[str, bool], None]] = None
) -> tuple[int, int, str]:
    """
    Actualiza todos los drivers posibles usando múltiples métodos.

    Args:
        callback: Función para reportar progreso (mensaje, porcentaje)
        on_driver_installed: Función llamada cuando un driver se instala (device_id, éxito)

    Returns:
        (exitosos, fallidos, mensaje)
    """
    drivers_instalados = 0
    drivers_fallidos = 0
    dispositivos_intel = []
    dispositivos_otros = []
    drivers_actualizados_ids = []  # Lista de device_ids que se actualizaron

    if callback:
        callback("Escaneando dispositivos del sistema...", 5)

    # 1. Escanear dispositivos
    ejecutar_cmd("pnputil /scan-devices")

    if callback:
        callback("Identificando drivers faltantes...", 10)

    # 2. Obtener dispositivos con problemas
    comando_faltantes = """
    Get-PnpDevice | Where-Object { $_.Problem -eq 28 -or $_.Status -eq 'Error' } |
    Select-Object InstanceId, FriendlyName, Class, HardwareID |
    ConvertTo-Json -Compress
    """

    exito_faltantes, salida_faltantes = ejecutar_powershell(comando_faltantes)
    dispositivos_faltantes = []

    if exito_faltantes and salida_faltantes and salida_faltantes.strip() not in ['', '[]', 'null']:
        try:
            import json
            datos = json.loads(salida_faltantes)
            if isinstance(datos, dict):
                datos = [datos]
            dispositivos_faltantes = datos
        except:
            pass

    # Clasificar por fabricante
    for disp in dispositivos_faltantes:
        nombre = disp.get('FriendlyName') or 'Dispositivo'
        hw_ids = disp.get('HardwareID') or []
        hw_id = hw_ids[0] if hw_ids else ''

        fabricante = _identificar_fabricante(nombre, hw_id)
        disp['fabricante_detectado'] = fabricante

        if fabricante == "Intel":
            dispositivos_intel.append(disp)
        else:
            dispositivos_otros.append(disp)

    if callback:
        callback(f"Encontrados {len(dispositivos_faltantes)} dispositivos sin driver...", 15)

    # 3. Intentar Windows Update primero
    if callback:
        callback("Buscando drivers en Windows Update...", 20)

    comando_wu = """
    try {
        # Forzar búsqueda de drivers
        $UpdateSession = New-Object -ComObject Microsoft.Update.Session
        $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()

        # Buscar actualizaciones de drivers
        $SearchResult = $UpdateSearcher.Search("IsInstalled=0 and Type='Driver'")

        if ($SearchResult.Updates.Count -gt 0) {
            $UpdatesToDownload = New-Object -ComObject Microsoft.Update.UpdateColl
            foreach ($Update in $SearchResult.Updates) {
                $UpdatesToDownload.Add($Update) | Out-Null
            }

            $Downloader = $UpdateSession.CreateUpdateDownloader()
            $Downloader.Updates = $UpdatesToDownload
            $Downloader.Download() | Out-Null

            $Installer = New-Object -ComObject Microsoft.Update.Installer
            $Installer.Updates = $UpdatesToDownload
            $InstallResult = $Installer.Install()

            $installed = 0
            for ($i = 0; $i -lt $UpdatesToDownload.Count; $i++) {
                if ($InstallResult.GetUpdateResult($i).ResultCode -eq 2) {
                    $installed++
                }
            }
            Write-Output "WU_INSTALLED:$installed"
        } else {
            Write-Output "WU_NONE:0"
        }
    } catch {
        Write-Output "WU_ERROR:$($_.Exception.Message)"
    }
    """

    if callback:
        callback("Descargando drivers de Windows Update...", 35)

    exito_wu, salida_wu = ejecutar_powershell(comando_wu)

    if "WU_INSTALLED:" in salida_wu:
        try:
            count = int(salida_wu.split("WU_INSTALLED:")[1].strip())
            drivers_instalados += count
        except:
            pass

    # 4. Buscar en Windows INF local
    if callback:
        callback("Buscando drivers en el sistema...", 50)

    for i, disp in enumerate(dispositivos_faltantes):
        instance_id = disp.get('InstanceId', '')
        nombre = disp.get('FriendlyName') or 'Dispositivo'

        if callback:
            progreso = 50 + int((i / max(len(dispositivos_faltantes), 1)) * 25)
            callback(f"Instalando driver: {nombre[:35]}...", progreso)

        # Intentar instalar desde Windows INF
        comando_install = f'''
        try {{
            $device = Get-PnpDevice | Where-Object {{ $_.InstanceId -eq "{instance_id}" }}
            if ($device) {{
                # Buscar e instalar driver
                $result = & pnputil /add-driver C:\\Windows\\INF\\*.inf /subdirs /install 2>&1

                # Verificar si se instaló
                Start-Sleep -Seconds 2
                $deviceAfter = Get-PnpDevice | Where-Object {{ $_.InstanceId -eq "{instance_id}" }}
                if ($deviceAfter.Problem -eq 0) {{
                    Write-Output "INSTALLED"
                }} else {{
                    Write-Output "STILL_MISSING"
                }}
            }}
        }} catch {{
            Write-Output "ERROR"
        }}
        '''

        exito_inst, salida_inst = ejecutar_powershell(comando_install)

        if "INSTALLED" in salida_inst:
            drivers_instalados += 1
            drivers_actualizados_ids.append(instance_id)
            # Notificar que el driver se instaló
            if on_driver_installed:
                on_driver_installed(instance_id, True)
        else:
            drivers_fallidos += 1
            if on_driver_installed:
                on_driver_installed(instance_id, False)

    # 5. Verificar estado final
    if callback:
        callback("Verificando estado final...", 95)

    # Verificar cuántos dispositivos aún tienen problemas
    exito_final, salida_final = ejecutar_powershell("""
    $problemas = Get-PnpDevice | Where-Object { $_.Problem -eq 28 -or $_.Status -eq 'Error' }
    Write-Output "REMAINING:$($problemas.Count)"
    """)

    remaining = 0
    if "REMAINING:" in salida_final:
        try:
            remaining = int(salida_final.split("REMAINING:")[1].strip())
        except:
            pass

    if callback:
        callback("Proceso completado", 100)

    # Construir mensaje final
    if drivers_instalados > 0 and remaining == 0:
        return drivers_instalados, 0, f"¡Perfecto! Se instalaron {drivers_instalados} drivers. Todo está actualizado."
    elif drivers_instalados > 0:
        return drivers_instalados, remaining, f"Se instalaron {drivers_instalados} drivers. {remaining} dispositivos requieren drivers del fabricante."
    elif remaining > 0:
        # Dar información sobre dónde conseguir los drivers
        fabricantes = set()
        for d in dispositivos_faltantes:
            fab = d.get('fabricante_detectado', 'Desconocido')
            if fab != 'Desconocido':
                fabricantes.add(fab)

        if fabricantes:
            fab_str = ", ".join(fabricantes)
            return 0, remaining, f"Drivers no disponibles en Windows Update. Descárgalos de: {fab_str}"
        else:
            return 0, remaining, f"{remaining} dispositivos necesitan drivers. Descárgalos del fabricante de tu PC."
    else:
        return 0, 0, "¡Perfecto! Todos los drivers están instalados y actualizados."


def verificar_estado_drivers() -> tuple[bool, str, int, int]:
    """
    Verifica rápidamente el estado de los drivers.

    Returns:
        (todos_ok, mensaje, total, con_problemas)
    """
    comando = """
    $total = (Get-PnpDevice | Where-Object { $_.Status -eq 'OK' }).Count
    $problemas = (Get-PnpDevice | Where-Object { $_.Problem -ne 0 -or $_.Status -eq 'Error' }).Count
    Write-Output "TOTAL:$total,PROBLEMAS:$problemas"
    """

    exito, salida = ejecutar_powershell(comando)

    total = 0
    problemas = 0

    if exito and salida:
        try:
            parts = salida.strip().split(',')
            for part in parts:
                if 'TOTAL:' in part:
                    total = int(part.split(':')[1])
                elif 'PROBLEMAS:' in part:
                    problemas = int(part.split(':')[1])
        except:
            pass

    todos_ok = problemas == 0

    if todos_ok:
        mensaje = "¡Todos los drivers están perfectos!"
    else:
        mensaje = f"{problemas} dispositivos necesitan atención"

    return todos_ok, mensaje, total, problemas


def buscar_actualizaciones_windows(callback: Optional[Callable[[str, int], None]] = None) -> tuple[bool, str]:
    """Busca actualizaciones de drivers a través de Windows Update."""
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
    """Intenta actualizar un driver específico usando Windows Update."""
    if callback:
        callback("Buscando driver en Windows Update...", 20)

    comando = f'pnputil /scan-devices'
    ejecutar_cmd(comando)

    if callback:
        callback("Instalando driver...", 60)

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


def exportar_reporte_drivers(drivers: List[DriverInfo], ruta: str) -> tuple[bool, str]:
    """Exporta un reporte de drivers a un archivo."""
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("  REPORTE DE DRIVERS - TECNODESPEGUE OPTIMIZER\n")
            f.write("=" * 70 + "\n\n")

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
                        estado_icon = "OK" if d.estado == EstadoDriver.OK else "!!"
                        f.write(f"  [{estado_icon}] {d.nombre}\n")
                        f.write(f"       Fabricante: {d.fabricante}\n")
                        f.write(f"       Version: {d.version}\n")
                        f.write(f"       Fecha: {d.fecha}\n")
                        f.write(f"       Estado: {d.estado.value}\n\n")

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
