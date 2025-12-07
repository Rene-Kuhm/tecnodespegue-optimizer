"""Módulo para gestionar y eliminar bloatware de Windows 11."""
from dataclasses import dataclass
from enum import Enum
from src.utils.admin import ejecutar_powershell


class CategoriaBloat(Enum):
    MICROSOFT = "Microsoft"
    JUEGOS = "Juegos"
    COMUNICACION = "Comunicación"
    MULTIMEDIA = "Multimedia"
    UTILIDADES = "Utilidades"
    TERCEROS = "Terceros"


@dataclass
class AppBloat:
    """Representa una aplicación bloatware."""
    nombre: str
    paquete: str
    descripcion: str
    categoria: CategoriaBloat
    recomendado_eliminar: bool = True


# Lista de bloatware común en Windows 11
BLOATWARE_APPS: list[AppBloat] = [
    # MICROSOFT
    AppBloat("Cortana", "*Microsoft.549981C3F5F10*", "Asistente de voz", CategoriaBloat.MICROSOFT),
    AppBloat("Microsoft News", "*Microsoft.BingNews*", "Noticias de Bing", CategoriaBloat.MICROSOFT),
    AppBloat("Microsoft Weather", "*Microsoft.BingWeather*", "Clima de Bing", CategoriaBloat.MICROSOFT),
    AppBloat("Get Help", "*Microsoft.GetHelp*", "Ayuda de Windows", CategoriaBloat.MICROSOFT),
    AppBloat("Microsoft Tips", "*Microsoft.Getstarted*", "Consejos de Windows", CategoriaBloat.MICROSOFT),
    AppBloat("Office Hub", "*Microsoft.MicrosoftOfficeHub*", "Hub de Office", CategoriaBloat.MICROSOFT),
    AppBloat("Solitaire Collection", "*Microsoft.MicrosoftSolitaireCollection*", "Juegos de cartas", CategoriaBloat.JUEGOS),
    AppBloat("Mixed Reality Portal", "*Microsoft.MixedReality.Portal*", "Portal de realidad mixta", CategoriaBloat.MICROSOFT),
    AppBloat("OneNote", "*Microsoft.Office.OneNote*", "OneNote UWP", CategoriaBloat.MICROSOFT, False),
    AppBloat("Paint 3D", "*Microsoft.MSPaint*", "Paint 3D", CategoriaBloat.MULTIMEDIA),
    AppBloat("3D Viewer", "*Microsoft.Microsoft3DViewer*", "Visor 3D", CategoriaBloat.MULTIMEDIA),
    AppBloat("People", "*Microsoft.People*", "Contactos", CategoriaBloat.COMUNICACION),
    AppBloat("Skype", "*Microsoft.SkypeApp*", "Skype UWP", CategoriaBloat.COMUNICACION),
    AppBloat("Voice Recorder", "*Microsoft.WindowsSoundRecorder*", "Grabadora de voz", CategoriaBloat.MULTIMEDIA, False),
    AppBloat("Sticky Notes", "*Microsoft.MicrosoftStickyNotes*", "Notas adhesivas", CategoriaBloat.UTILIDADES, False),
    AppBloat("Microsoft To Do", "*Microsoft.Todos*", "Lista de tareas", CategoriaBloat.UTILIDADES, False),
    AppBloat("Feedback Hub", "*Microsoft.WindowsFeedbackHub*", "Centro de comentarios", CategoriaBloat.MICROSOFT),
    AppBloat("Maps", "*Microsoft.WindowsMaps*", "Mapas de Windows", CategoriaBloat.MICROSOFT),
    AppBloat("Alarms & Clock", "*Microsoft.WindowsAlarms*", "Alarmas y reloj", CategoriaBloat.UTILIDADES, False),
    AppBloat("Camera", "*Microsoft.WindowsCamera*", "Cámara", CategoriaBloat.MULTIMEDIA, False),
    AppBloat("Mail & Calendar", "*microsoft.windowscommunicationsapps*", "Correo y calendario", CategoriaBloat.COMUNICACION),
    AppBloat("Your Phone", "*Microsoft.YourPhone*", "Tu Teléfono / Phone Link", CategoriaBloat.COMUNICACION),
    AppBloat("Xbox App", "*Microsoft.Xbox.TCUI*", "Xbox UI", CategoriaBloat.JUEGOS),
    AppBloat("Xbox Game Bar", "*Microsoft.XboxGamingOverlay*", "Game Bar", CategoriaBloat.JUEGOS),
    AppBloat("Xbox Identity", "*Microsoft.XboxIdentityProvider*", "Identidad Xbox", CategoriaBloat.JUEGOS),
    AppBloat("Xbox Speech", "*Microsoft.XboxSpeechToTextOverlay*", "Xbox Speech", CategoriaBloat.JUEGOS),
    AppBloat("Clipchamp", "*Clipchamp.Clipchamp*", "Editor de video", CategoriaBloat.MULTIMEDIA),
    AppBloat("Microsoft Family", "*MicrosoftCorporationII.MicrosoftFamily*", "Control parental", CategoriaBloat.MICROSOFT),
    AppBloat("Quick Assist", "*MicrosoftCorporationII.QuickAssist*", "Asistencia rápida", CategoriaBloat.MICROSOFT),
    AppBloat("Widgets", "*MicrosoftWindows.Client.WebExperience*", "Panel de Widgets", CategoriaBloat.MICROSOFT),
    AppBloat("Power Automate", "*Microsoft.PowerAutomateDesktop*", "Automatización", CategoriaBloat.MICROSOFT),
    AppBloat("Teams (Personal)", "*MicrosoftTeams*", "Teams chat personal", CategoriaBloat.COMUNICACION),
    AppBloat("Dev Home", "*Microsoft.Windows.DevHome*", "Dev Home (desarrolladores)", CategoriaBloat.MICROSOFT, False),
    AppBloat("Copilot", "*Microsoft.Copilot*", "Windows Copilot", CategoriaBloat.MICROSOFT),
    AppBloat("Outlook (New)", "*Microsoft.OutlookForWindows*", "Nuevo Outlook", CategoriaBloat.COMUNICACION),

    # TERCEROS (preinstalados)
    AppBloat("Spotify", "*SpotifyAB.SpotifyMusic*", "Spotify preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("Disney+", "*Disney*", "Disney+ preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("TikTok", "*TikTok*", "TikTok preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("Instagram", "*Instagram*", "Instagram preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("Facebook", "*Facebook*", "Facebook preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("Messenger", "*Messenger*", "Messenger preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("Amazon", "*Amazon*", "Amazon preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("Netflix", "*Netflix*", "Netflix preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("Candy Crush", "*king.com*", "Candy Crush y juegos King", CategoriaBloat.JUEGOS),
    AppBloat("LinkedIn", "*LinkedIn*", "LinkedIn preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("Twitter/X", "*Twitter*", "Twitter/X preinstalado", CategoriaBloat.TERCEROS),
    AppBloat("WhatsApp", "*WhatsApp*", "WhatsApp Desktop", CategoriaBloat.COMUNICACION, False),
]


def obtener_apps_instaladas() -> list[str]:
    """Obtiene la lista de paquetes UWP instalados."""
    cmd = "Get-AppxPackage | Select-Object -ExpandProperty Name"
    exito, salida = ejecutar_powershell(cmd)
    if exito:
        return [app.strip() for app in salida.split('\n') if app.strip()]
    return []


def verificar_app_instalada(paquete: str) -> bool:
    """Verifica si una app está instalada."""
    # Remover asteriscos para búsqueda
    paquete_limpio = paquete.replace('*', '')
    cmd = f"Get-AppxPackage -Name '*{paquete_limpio}*' | Select-Object -First 1"
    exito, salida = ejecutar_powershell(cmd)
    return exito and len(salida.strip()) > 0


def desinstalar_app(paquete: str) -> tuple[bool, str]:
    """Desinstala una app UWP."""
    cmd = f'''
    Get-AppxPackage -AllUsers {paquete} | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue
    Get-AppxProvisionedPackage -Online | Where-Object {{ $_.DisplayName -like "{paquete.replace('*', '')}" }} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue
    '''
    return ejecutar_powershell(cmd)


def desinstalar_multiples_apps(paquetes: list[str]) -> dict[str, tuple[bool, str]]:
    """Desinstala múltiples apps y retorna el resultado de cada una."""
    resultados = {}
    for paquete in paquetes:
        resultados[paquete] = desinstalar_app(paquete)
    return resultados


def obtener_bloatware_instalado() -> list[AppBloat]:
    """Obtiene la lista de bloatware que está instalado."""
    instalado = []
    for app in BLOATWARE_APPS:
        if verificar_app_instalada(app.paquete):
            instalado.append(app)
    return instalado


def eliminar_todo_bloatware_recomendado() -> tuple[int, int]:
    """Elimina todo el bloatware recomendado. Retorna (exitosos, fallidos)."""
    exitosos = 0
    fallidos = 0

    for app in BLOATWARE_APPS:
        if app.recomendado_eliminar:
            exito, _ = desinstalar_app(app.paquete)
            if exito:
                exitosos += 1
            else:
                fallidos += 1

    return exitosos, fallidos


def obtener_apps_por_categoria(categoria: CategoriaBloat) -> list[AppBloat]:
    """Obtiene las apps de una categoría específica."""
    return [app for app in BLOATWARE_APPS if app.categoria == categoria]
