"""Módulo de gestión de servicios de Windows."""
from dataclasses import dataclass
from enum import Enum
from src.utils.admin import ejecutar_powershell


class EstadoServicio(Enum):
    EJECUTANDO = "Running"
    DETENIDO = "Stopped"
    DESCONOCIDO = "Unknown"


class TipoInicio(Enum):
    AUTOMATICO = "Automatic"
    MANUAL = "Manual"
    DESHABILITADO = "Disabled"
    AUTOMATICO_RETRASADO = "AutomaticDelayedStart"


@dataclass
class Servicio:
    """Representa un servicio de Windows."""
    nombre: str
    nombre_display: str
    descripcion: str
    estado: EstadoServicio
    tipo_inicio: TipoInicio
    recomendacion: str = ""
    seguro_deshabilitar: bool = False


# Servicios que se pueden deshabilitar de forma segura
SERVICIOS_DESHABILITABLES = {
    # Telemetría y diagnóstico
    "DiagTrack": ("Experiencias del usuario conectado y telemetría", "Envía datos a Microsoft"),
    "dmwappushservice": ("Servicio de enrutamiento de mensajes push WAP", "Telemetría"),
    "WerSvc": ("Servicio de informe de errores de Windows", "Envía informes de errores"),

    # Xbox (si no juegas)
    "XblAuthManager": ("Administrador de autenticación de Xbox Live", "Autenticación Xbox"),
    "XblGameSave": ("Servicio de juegos guardados en Xbox Live", "Guardado en la nube Xbox"),
    "XboxGipSvc": ("Servicio de administración de accesorios de Xbox", "Accesorios Xbox"),
    "XboxNetApiSvc": ("Servicio de red de Xbox Live", "Red de Xbox"),

    # Indexación (si no usas búsqueda mucho)
    "WSearch": ("Windows Search", "Indexación de búsqueda - puede causar uso alto de disco"),

    # Superfetch
    "SysMain": ("SysMain (Superfetch)", "Precarga de apps - puede causar uso de disco"),

    # Ubicación
    "lfsvc": ("Servicio de geolocalización", "Ubicación GPS"),

    # Mapas
    "MapsBroker": ("Administrador de mapas descargados", "Mapas offline"),

    # Fax
    "Fax": ("Fax", "Servicio de fax - innecesario si no usas fax"),

    # Escritorio remoto
    "TermService": ("Servicios de Escritorio remoto", "RDP - si no lo usas"),
    "SessionEnv": ("Configuración de Escritorio remoto", "RDP"),
    "UmRdpService": ("Redirector de puerto en modo usuario de RDP", "RDP"),

    # Teléfono
    "PhoneSvc": ("Servicio telefónico", "Si no vinculas teléfono"),
    "TapiSrv": ("Telefonía", "API de telefonía antigua"),

    # Biometría (si no usas huella/cara)
    "WbioSrvc": ("Servicio biométrico de Windows", "Huella/reconocimiento facial"),

    # Wallet
    "WalletService": ("Servicio de billetera", "Microsoft Wallet"),

    # Hyper-V (si no usas máquinas virtuales)
    "HvHost": ("Servicio de host de HV", "Hyper-V"),
    "vmickvpexchange": ("Servicio de intercambio de datos de Hyper-V", "Hyper-V"),
    "vmicguestinterface": ("Interfaz de servicio de invitado de Hyper-V", "Hyper-V"),
    "vmicshutdown": ("Servicio de cierre de invitado de Hyper-V", "Hyper-V"),
    "vmicheartbeat": ("Servicio de latido de Hyper-V", "Hyper-V"),
    "vmicvmsession": ("Servicio de sesión de máquina virtual de Hyper-V", "Hyper-V"),
    "vmicrdv": ("Servicio de virtualización de escritorio remoto de Hyper-V", "Hyper-V"),
    "vmictimesync": ("Servicio de sincronización de hora de Hyper-V", "Hyper-V"),
    "vmicvss": ("Servicio de solicitud en la sombra del volumen de Hyper-V", "Hyper-V"),

    # Otros
    "RetailDemo": ("Servicio de demostración del distribuidor", "Modo demo tiendas"),
    "WMPNetworkSvc": ("Servicio de uso compartido de red del Reproductor de Windows Media", "Compartir WMP"),
    "wisvc": ("Servicio Windows Insider", "Programa Insider"),
    "DusmSvc": ("Uso de datos", "Monitoreo de datos móviles"),
    "BITS": ("Servicio de transferencia inteligente en segundo plano", "Descarga actualizaciones - cuidado"),
}


def obtener_servicios() -> list[Servicio]:
    """Obtiene todos los servicios del sistema."""
    cmd = '''
    Get-Service | Select-Object Name, DisplayName, Status, StartType | ConvertTo-Json -Compress
    '''
    exito, salida = ejecutar_powershell(cmd)

    if not exito or not salida or salida.strip() in ['', '[]', 'null']:
        return []

    import json
    try:
        datos = json.loads(salida)
        if isinstance(datos, dict):
            datos = [datos]

        servicios = []
        for svc in datos:
            nombre = svc.get('Name', '')
            if not nombre:
                continue

            # Estado puede ser número (4=Running, 1=Stopped) o string
            status = svc.get('Status')
            if isinstance(status, int):
                estado = EstadoServicio.EJECUTANDO if status == 4 else EstadoServicio.DETENIDO
            elif isinstance(status, str):
                estado = EstadoServicio.EJECUTANDO if status.lower() == 'running' else EstadoServicio.DETENIDO
            else:
                estado = EstadoServicio.DESCONOCIDO

            # StartType puede ser número (2=Auto, 3=Manual, 4=Disabled) o string
            tipo = svc.get('StartType', 0)
            if isinstance(tipo, int):
                if tipo == 2:
                    tipo_inicio = TipoInicio.AUTOMATICO
                elif tipo == 3:
                    tipo_inicio = TipoInicio.MANUAL
                elif tipo == 4:
                    tipo_inicio = TipoInicio.DESHABILITADO
                else:
                    tipo_inicio = TipoInicio.AUTOMATICO
            elif isinstance(tipo, str):
                tipo_lower = tipo.lower()
                if 'disabled' in tipo_lower:
                    tipo_inicio = TipoInicio.DESHABILITADO
                elif 'manual' in tipo_lower:
                    tipo_inicio = TipoInicio.MANUAL
                elif 'auto' in tipo_lower:
                    tipo_inicio = TipoInicio.AUTOMATICO
                else:
                    tipo_inicio = TipoInicio.MANUAL
            else:
                tipo_inicio = TipoInicio.MANUAL

            desc = ""
            recomendacion = ""
            seguro = False

            if nombre in SERVICIOS_DESHABILITABLES:
                desc, recomendacion = SERVICIOS_DESHABILITABLES[nombre]
                seguro = True

            servicios.append(Servicio(
                nombre=nombre,
                nombre_display=svc.get('DisplayName', nombre) or nombre,
                descripcion=desc,
                estado=estado,
                tipo_inicio=tipo_inicio,
                recomendacion=recomendacion,
                seguro_deshabilitar=seguro
            ))

        return servicios
    except Exception:
        return []


def obtener_servicios_deshabilitables() -> list[Servicio]:
    """Obtiene solo los servicios que se pueden deshabilitar de forma segura."""
    todos = obtener_servicios()
    return [s for s in todos if s.seguro_deshabilitar]


def detener_servicio(nombre: str) -> tuple[bool, str]:
    """Detiene un servicio."""
    cmd = f'Stop-Service -Name "{nombre}" -Force -ErrorAction SilentlyContinue'
    return ejecutar_powershell(cmd)


def iniciar_servicio(nombre: str) -> tuple[bool, str]:
    """Inicia un servicio."""
    cmd = f'Start-Service -Name "{nombre}" -ErrorAction SilentlyContinue'
    return ejecutar_powershell(cmd)


def deshabilitar_servicio(nombre: str) -> tuple[bool, str]:
    """Deshabilita un servicio."""
    cmd = f'''
    Stop-Service -Name "{nombre}" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "{nombre}" -StartupType Disabled -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def habilitar_servicio(nombre: str, tipo: TipoInicio = TipoInicio.MANUAL) -> tuple[bool, str]:
    """Habilita un servicio."""
    cmd = f'''
    Set-Service -Name "{nombre}" -StartupType {tipo.value} -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_servicios_telemetria() -> tuple[int, int]:
    """Deshabilita todos los servicios de telemetría."""
    servicios = ["DiagTrack", "dmwappushservice", "WerSvc"]
    exitosos = 0
    fallidos = 0

    for svc in servicios:
        exito, _ = deshabilitar_servicio(svc)
        if exito:
            exitosos += 1
        else:
            fallidos += 1

    return exitosos, fallidos


def deshabilitar_servicios_xbox() -> tuple[int, int]:
    """Deshabilita todos los servicios de Xbox."""
    servicios = ["XblAuthManager", "XblGameSave", "XboxGipSvc", "XboxNetApiSvc"]
    exitosos = 0
    fallidos = 0

    for svc in servicios:
        exito, _ = deshabilitar_servicio(svc)
        if exito:
            exitosos += 1
        else:
            fallidos += 1

    return exitosos, fallidos


def deshabilitar_servicios_hyperv() -> tuple[int, int]:
    """Deshabilita todos los servicios de Hyper-V."""
    servicios = [
        "HvHost", "vmickvpexchange", "vmicguestinterface", "vmicshutdown",
        "vmicheartbeat", "vmicvmsession", "vmicrdv", "vmictimesync", "vmicvss"
    ]
    exitosos = 0
    fallidos = 0

    for svc in servicios:
        exito, _ = deshabilitar_servicio(svc)
        if exito:
            exitosos += 1
        else:
            fallidos += 1

    return exitosos, fallidos


def aplicar_perfil_minimo() -> tuple[int, int]:
    """Aplica el perfil mínimo de servicios (solo telemetría)."""
    return deshabilitar_servicios_telemetria()


def aplicar_perfil_recomendado() -> tuple[int, int]:
    """Aplica el perfil recomendado de servicios."""
    servicios = [
        "DiagTrack", "dmwappushservice", "WerSvc",  # Telemetría
        "XblAuthManager", "XblGameSave", "XboxGipSvc", "XboxNetApiSvc",  # Xbox
        "MapsBroker", "lfsvc",  # Mapas/Ubicación
        "RetailDemo", "wisvc",  # Demo/Insider
    ]

    exitosos = 0
    fallidos = 0

    for svc in servicios:
        exito, _ = deshabilitar_servicio(svc)
        if exito:
            exitosos += 1
        else:
            fallidos += 1

    return exitosos, fallidos


def aplicar_perfil_maximo() -> tuple[int, int]:
    """Aplica el perfil máximo de servicios (deshabilita todo lo seguro)."""
    exitosos = 0
    fallidos = 0

    for nombre in SERVICIOS_DESHABILITABLES.keys():
        exito, _ = deshabilitar_servicio(nombre)
        if exito:
            exitosos += 1
        else:
            fallidos += 1

    return exitosos, fallidos
