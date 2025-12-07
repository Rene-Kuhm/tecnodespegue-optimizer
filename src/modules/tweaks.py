"""Módulo de Tweaks del Sistema para Windows 11 25H2."""
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from src.utils.admin import ejecutar_powershell, ejecutar_cmd


class CategoriaTweak(Enum):
    RENDIMIENTO = "Rendimiento"
    PRIVACIDAD = "Privacidad"
    INTERFAZ = "Interfaz"
    ENERGIA = "Energía"
    RED = "Red"
    ALMACENAMIENTO = "Almacenamiento"


class NivelRiesgo(Enum):
    BAJO = "Bajo"
    MEDIO = "Medio"
    ALTO = "Alto"


@dataclass
class Tweak:
    """Representa un tweak del sistema."""
    id: str
    nombre: str
    descripcion: str
    categoria: CategoriaTweak
    riesgo: NivelRiesgo
    aplicar: Callable[[], tuple[bool, str]]
    revertir: Callable[[], tuple[bool, str]] | None = None
    requiere_reinicio: bool = False


# ============================================
# TWEAKS DE RENDIMIENTO
# ============================================

def deshabilitar_superfetch() -> tuple[bool, str]:
    """Deshabilita SysMain/Superfetch."""
    cmd = '''
    Stop-Service -Name "SysMain" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "SysMain" -StartupType Disabled -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def habilitar_superfetch() -> tuple[bool, str]:
    """Habilita SysMain/Superfetch."""
    cmd = '''
    Set-Service -Name "SysMain" -StartupType Automatic -ErrorAction SilentlyContinue
    Start-Service -Name "SysMain" -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_indexacion() -> tuple[bool, str]:
    """Deshabilita Windows Search Indexer."""
    cmd = '''
    Stop-Service -Name "WSearch" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "WSearch" -StartupType Disabled -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def habilitar_indexacion() -> tuple[bool, str]:
    """Habilita Windows Search Indexer."""
    cmd = '''
    Set-Service -Name "WSearch" -StartupType Automatic -ErrorAction SilentlyContinue
    Start-Service -Name "WSearch" -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def optimizar_efectos_visuales() -> tuple[bool, str]:
    """Optimiza efectos visuales para rendimiento."""
    cmd = '''
    # Configurar para mejor rendimiento
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Value 2 -Type DWord -Force
    # Deshabilitar transparencia
    Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" -Name "EnableTransparency" -Value 0 -Type DWord -Force
    # Deshabilitar animaciones
    Set-ItemProperty -Path "HKCU:\\Control Panel\\Desktop\\WindowMetrics" -Name "MinAnimate" -Value "0" -Type String -Force
    Set-ItemProperty -Path "HKCU:\\Control Panel\\Desktop" -Name "MenuShowDelay" -Value "0" -Type String -Force
    # Deshabilitar animaciones de ventanas
    Set-ItemProperty -Path "HKCU:\\Control Panel\\Desktop" -Name "UserPreferencesMask" -Value ([byte[]](0x90,0x12,0x03,0x80,0x10,0x00,0x00,0x00)) -Type Binary -Force
    '''
    return ejecutar_powershell(cmd)


def restaurar_efectos_visuales() -> tuple[bool, str]:
    """Restaura efectos visuales predeterminados."""
    cmd = '''
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Value 0 -Type DWord -Force
    Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" -Name "EnableTransparency" -Value 1 -Type DWord -Force
    Set-ItemProperty -Path "HKCU:\\Control Panel\\Desktop\\WindowMetrics" -Name "MinAnimate" -Value "1" -Type String -Force
    Set-ItemProperty -Path "HKCU:\\Control Panel\\Desktop" -Name "MenuShowDelay" -Value "400" -Type String -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_game_bar() -> tuple[bool, str]:
    """Deshabilita Xbox Game Bar y Game DVR."""
    cmd = '''
    # Game DVR
    New-Item -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR" -Force | Out-Null
    Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR" -Name "AppCaptureEnabled" -Value 0 -Type DWord -Force
    # Game Bar
    New-Item -Path "HKCU:\\System\\GameConfigStore" -Force | Out-Null
    Set-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_Enabled" -Value 0 -Type DWord -Force
    # Game Bar Tips
    Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\GameBar" -Name "ShowStartupPanel" -Value 0 -Type DWord -Force -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def plan_energia_alto_rendimiento() -> tuple[bool, str]:
    """Activa el plan de energía de alto rendimiento."""
    cmd = 'powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'
    return ejecutar_cmd(cmd)


def plan_energia_ultimate() -> tuple[bool, str]:
    """Activa o crea el plan de energía Ultimate Performance."""
    cmd = '''
    # Intentar activar Ultimate Performance
    $ultimate = powercfg /list | Select-String "Ultimate"
    if (-not $ultimate) {
        # Duplicar desde alto rendimiento
        powercfg /duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61
    }
    # Buscar y activar
    $guid = (powercfg /list | Select-String "Ultimate" | ForEach-Object { $_ -match "([a-f0-9-]{36})" | Out-Null; $matches[1] })
    if ($guid) {
        powercfg /setactive $guid
        Write-Output "Ultimate Performance activado"
    } else {
        powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
        Write-Output "Alto Rendimiento activado"
    }
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_hibernacion() -> tuple[bool, str]:
    """Deshabilita la hibernación."""
    cmd = 'powercfg /hibernate off'
    return ejecutar_cmd(cmd)


def habilitar_hibernacion() -> tuple[bool, str]:
    """Habilita la hibernación."""
    cmd = 'powercfg /hibernate on'
    return ejecutar_cmd(cmd)


# ============================================
# TWEAKS DE PRIVACIDAD
# ============================================

def deshabilitar_telemetria() -> tuple[bool, str]:
    """Deshabilita telemetría de Windows."""
    cmd = '''
    # Servicio de telemetría
    Stop-Service -Name "DiagTrack" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "DiagTrack" -StartupType Disabled -ErrorAction SilentlyContinue

    # dmwappushservice
    Stop-Service -Name "dmwappushservice" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "dmwappushservice" -StartupType Disabled -ErrorAction SilentlyContinue

    # Registro - Nivel de telemetría al mínimo
    New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Force | Out-Null
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Value 0 -Type DWord -Force

    # Deshabilitar feedback
    New-Item -Path "HKCU:\\SOFTWARE\\Microsoft\\Siuf\\Rules" -Force | Out-Null
    Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Siuf\\Rules" -Name "NumberOfSIUFInPeriod" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_cortana() -> tuple[bool, str]:
    """Deshabilita Cortana."""
    cmd = '''
    New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" -Force | Out-Null
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" -Name "AllowCortana" -Value 0 -Type DWord -Force
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" -Name "DisableWebSearch" -Value 1 -Type DWord -Force
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" -Name "ConnectedSearchUseWeb" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_historial_actividad() -> tuple[bool, str]:
    """Deshabilita el historial de actividad."""
    cmd = '''
    New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Force | Out-Null
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "EnableActivityFeed" -Value 0 -Type DWord -Force
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "PublishUserActivities" -Value 0 -Type DWord -Force
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "UploadUserActivities" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_advertising_id() -> tuple[bool, str]:
    """Deshabilita el ID de publicidad."""
    cmd = '''
    New-Item -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" -Force | Out-Null
    Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" -Name "Enabled" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_ubicacion() -> tuple[bool, str]:
    """Deshabilita servicios de ubicación."""
    cmd = '''
    Stop-Service -Name "lfsvc" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "lfsvc" -StartupType Disabled -ErrorAction SilentlyContinue
    New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\LocationAndSensors" -Force | Out-Null
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\LocationAndSensors" -Name "DisableLocation" -Value 1 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_apps_background() -> tuple[bool, str]:
    """Deshabilita apps en segundo plano."""
    cmd = '''
    New-Item -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" -Force | Out-Null
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" -Name "GlobalUserDisabled" -Value 1 -Type DWord -Force
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" -Name "BackgroundAppGlobalToggle" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


# ============================================
# TWEAKS DE SERVICIOS
# ============================================

def deshabilitar_servicios_xbox() -> tuple[bool, str]:
    """Deshabilita todos los servicios de Xbox."""
    cmd = '''
    $servicios = @("XblAuthManager", "XblGameSave", "XboxGipSvc", "XboxNetApiSvc")
    foreach ($svc in $servicios) {
        Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
        Set-Service -Name $svc -StartupType Disabled -ErrorAction SilentlyContinue
    }
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_servicios_impresion() -> tuple[bool, str]:
    """Deshabilita servicios de impresión (si no usas impresora)."""
    cmd = '''
    Stop-Service -Name "Spooler" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "Spooler" -StartupType Disabled -ErrorAction SilentlyContinue
    Stop-Service -Name "Fax" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "Fax" -StartupType Disabled -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_escritorio_remoto() -> tuple[bool, str]:
    """Deshabilita servicios de escritorio remoto."""
    cmd = '''
    $servicios = @("TermService", "SessionEnv", "UmRdpService")
    foreach ($svc in $servicios) {
        Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
        Set-Service -Name $svc -StartupType Disabled -ErrorAction SilentlyContinue
    }
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_phone_link() -> tuple[bool, str]:
    """Deshabilita Phone Link / Tu Teléfono."""
    cmd = '''
    Get-AppxPackage *YourPhone* | Remove-AppxPackage -ErrorAction SilentlyContinue
    Get-AppxPackage *PhoneExperienceHost* | Remove-AppxPackage -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


# ============================================
# TWEAKS DE INTERFAZ WINDOWS 11
# ============================================

def menu_clasico_click_derecho() -> tuple[bool, str]:
    """Restaura el menú contextual clásico de Windows 10."""
    cmd = '''
    New-Item -Path "HKCU:\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32" -Force | Out-Null
    Set-ItemProperty -Path "HKCU:\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32" -Name "(Default)" -Value "" -Force
    '''
    return ejecutar_powershell(cmd)


def menu_nuevo_click_derecho() -> tuple[bool, str]:
    """Restaura el menú contextual nuevo de Windows 11."""
    cmd = '''
    Remove-Item -Path "HKCU:\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" -Recurse -Force -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def barra_tareas_izquierda() -> tuple[bool, str]:
    """Alinea la barra de tareas a la izquierda."""
    cmd = '''
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "TaskbarAl" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def barra_tareas_centro() -> tuple[bool, str]:
    """Alinea la barra de tareas al centro."""
    cmd = '''
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "TaskbarAl" -Value 1 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_widgets() -> tuple[bool, str]:
    """Deshabilita Widgets de Windows 11."""
    cmd = '''
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "TaskbarDa" -Value 0 -Type DWord -Force
    # Desinstalar Widgets
    Get-AppxPackage *WebExperience* | Remove-AppxPackage -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_chat_teams() -> tuple[bool, str]:
    """Deshabilita el chat de Teams en la barra de tareas."""
    cmd = '''
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "TaskbarMn" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_busqueda_barra() -> tuple[bool, str]:
    """Oculta la barra de búsqueda."""
    cmd = '''
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" -Name "SearchboxTaskbarMode" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


def deshabilitar_copilot() -> tuple[bool, str]:
    """Deshabilita Windows Copilot."""
    cmd = '''
    New-Item -Path "HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" -Force | Out-Null
    Set-ItemProperty -Path "HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" -Name "TurnOffWindowsCopilot" -Value 1 -Type DWord -Force
    Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "ShowCopilotButton" -Value 0 -Type DWord -Force
    '''
    return ejecutar_powershell(cmd)


# ============================================
# LISTA DE TODOS LOS TWEAKS
# ============================================

TWEAKS_DISPONIBLES: list[Tweak] = [
    # RENDIMIENTO
    Tweak(
        id="deshabilitar_superfetch",
        nombre="Deshabilitar Superfetch/SysMain",
        descripcion="Reduce uso de disco y memoria. Puede afectar tiempos de carga de apps frecuentes.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_superfetch,
        revertir=habilitar_superfetch
    ),
    Tweak(
        id="deshabilitar_indexacion",
        nombre="Deshabilitar Indexación",
        descripcion="Reduce uso de disco y CPU. La búsqueda de archivos será más lenta.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_indexacion,
        revertir=habilitar_indexacion
    ),
    Tweak(
        id="optimizar_visual",
        nombre="Optimizar Efectos Visuales",
        descripcion="Deshabilita animaciones y transparencias para mejor rendimiento.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.BAJO,
        aplicar=optimizar_efectos_visuales,
        revertir=restaurar_efectos_visuales
    ),
    Tweak(
        id="deshabilitar_game_bar",
        nombre="Deshabilitar Xbox Game Bar",
        descripcion="Deshabilita Game Bar y DVR. Mejora rendimiento en juegos.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_game_bar
    ),
    Tweak(
        id="plan_ultimate",
        nombre="Plan Ultimate Performance",
        descripcion="Activa el plan de energía de máximo rendimiento.",
        categoria=CategoriaTweak.ENERGIA,
        riesgo=NivelRiesgo.BAJO,
        aplicar=plan_energia_ultimate
    ),
    Tweak(
        id="deshabilitar_hibernacion",
        nombre="Deshabilitar Hibernación",
        descripcion="Libera espacio en disco (tamaño de RAM). Pierde inicio rápido.",
        categoria=CategoriaTweak.ALMACENAMIENTO,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_hibernacion,
        revertir=habilitar_hibernacion
    ),

    # PRIVACIDAD
    Tweak(
        id="deshabilitar_telemetria",
        nombre="Deshabilitar Telemetría",
        descripcion="Detiene el envío de datos de diagnóstico a Microsoft.",
        categoria=CategoriaTweak.PRIVACIDAD,
        riesgo=NivelRiesgo.MEDIO,
        aplicar=deshabilitar_telemetria
    ),
    Tweak(
        id="deshabilitar_cortana",
        nombre="Deshabilitar Cortana",
        descripcion="Deshabilita Cortana y búsqueda web desde el menú inicio.",
        categoria=CategoriaTweak.PRIVACIDAD,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_cortana
    ),
    Tweak(
        id="deshabilitar_historial",
        nombre="Deshabilitar Historial de Actividad",
        descripcion="Deshabilita Timeline y sincronización de actividad.",
        categoria=CategoriaTweak.PRIVACIDAD,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_historial_actividad
    ),
    Tweak(
        id="deshabilitar_ads",
        nombre="Deshabilitar ID de Publicidad",
        descripcion="Deshabilita el identificador para anuncios personalizados.",
        categoria=CategoriaTweak.PRIVACIDAD,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_advertising_id
    ),
    Tweak(
        id="deshabilitar_ubicacion",
        nombre="Deshabilitar Ubicación",
        descripcion="Deshabilita servicios de localización.",
        categoria=CategoriaTweak.PRIVACIDAD,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_ubicacion
    ),
    Tweak(
        id="deshabilitar_background",
        nombre="Deshabilitar Apps en Segundo Plano",
        descripcion="Impide que las apps se ejecuten en segundo plano.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.MEDIO,
        aplicar=deshabilitar_apps_background
    ),

    # SERVICIOS
    Tweak(
        id="deshabilitar_xbox",
        nombre="Deshabilitar Servicios Xbox",
        descripcion="Deshabilita todos los servicios de Xbox Live.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_servicios_xbox
    ),
    Tweak(
        id="deshabilitar_impresion",
        nombre="Deshabilitar Servicios de Impresión",
        descripcion="Deshabilita Print Spooler. Solo si no usas impresora.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.MEDIO,
        aplicar=deshabilitar_servicios_impresion
    ),
    Tweak(
        id="deshabilitar_remoto",
        nombre="Deshabilitar Escritorio Remoto",
        descripcion="Deshabilita servicios de Remote Desktop.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_escritorio_remoto
    ),
    Tweak(
        id="deshabilitar_phone",
        nombre="Desinstalar Phone Link",
        descripcion="Elimina la app Tu Teléfono/Phone Link. Libera ~700MB RAM.",
        categoria=CategoriaTweak.RENDIMIENTO,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_phone_link
    ),

    # INTERFAZ
    Tweak(
        id="menu_clasico",
        nombre="Menú Contextual Clásico",
        descripcion="Restaura el menú de click derecho de Windows 10.",
        categoria=CategoriaTweak.INTERFAZ,
        riesgo=NivelRiesgo.BAJO,
        aplicar=menu_clasico_click_derecho,
        revertir=menu_nuevo_click_derecho,
        requiere_reinicio=True
    ),
    Tweak(
        id="barra_izquierda",
        nombre="Barra de Tareas a la Izquierda",
        descripcion="Alinea los iconos de la barra de tareas a la izquierda.",
        categoria=CategoriaTweak.INTERFAZ,
        riesgo=NivelRiesgo.BAJO,
        aplicar=barra_tareas_izquierda,
        revertir=barra_tareas_centro
    ),
    Tweak(
        id="deshabilitar_widgets",
        nombre="Deshabilitar Widgets",
        descripcion="Elimina el panel de Widgets de Windows 11.",
        categoria=CategoriaTweak.INTERFAZ,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_widgets
    ),
    Tweak(
        id="deshabilitar_chat",
        nombre="Ocultar Chat de Teams",
        descripcion="Oculta el icono de Chat de la barra de tareas.",
        categoria=CategoriaTweak.INTERFAZ,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_chat_teams
    ),
    Tweak(
        id="ocultar_busqueda",
        nombre="Ocultar Barra de Búsqueda",
        descripcion="Oculta la barra/icono de búsqueda de la barra de tareas.",
        categoria=CategoriaTweak.INTERFAZ,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_busqueda_barra
    ),
    Tweak(
        id="deshabilitar_copilot",
        nombre="Deshabilitar Windows Copilot",
        descripcion="Deshabilita Copilot y oculta su botón.",
        categoria=CategoriaTweak.INTERFAZ,
        riesgo=NivelRiesgo.BAJO,
        aplicar=deshabilitar_copilot
    ),
]


def obtener_tweaks_por_categoria(categoria: CategoriaTweak) -> list[Tweak]:
    """Obtiene los tweaks de una categoría específica."""
    return [t for t in TWEAKS_DISPONIBLES if t.categoria == categoria]


def obtener_tweak_por_id(id: str) -> Tweak | None:
    """Obtiene un tweak por su ID."""
    for t in TWEAKS_DISPONIBLES:
        if t.id == id:
            return t
    return None
