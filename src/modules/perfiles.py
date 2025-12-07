"""Módulo de perfiles de optimización predefinidos."""
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from src.modules import tweaks, servicios, bloatware, limpieza


class NivelPerfil(Enum):
    MINIMO = "Mínimo"
    RECOMENDADO = "Recomendado"
    MAXIMO = "Máximo"
    GAMING = "Gaming"
    PRODUCTIVIDAD = "Productividad"


@dataclass
class ResultadoPerfil:
    """Resultado de aplicar un perfil."""
    nombre: str
    tweaks_aplicados: int
    tweaks_fallidos: int
    servicios_deshabilitados: int
    apps_eliminadas: int
    espacio_liberado_mb: float
    requiere_reinicio: bool


@dataclass
class Perfil:
    """Define un perfil de optimización."""
    nivel: NivelPerfil
    nombre: str
    descripcion: str
    tweaks: list[str]  # IDs de tweaks
    deshabilitar_servicios: bool
    eliminar_bloatware: bool
    limpiar_sistema: bool


# Definición de perfiles
PERFILES = {
    NivelPerfil.MINIMO: Perfil(
        nivel=NivelPerfil.MINIMO,
        nombre="Mínimo",
        descripcion="Optimizaciones básicas y seguras. Solo deshabilita telemetría.",
        tweaks=[
            "deshabilitar_telemetria",
            "deshabilitar_ads",
            "deshabilitar_historial",
        ],
        deshabilitar_servicios=False,
        eliminar_bloatware=False,
        limpiar_sistema=True
    ),

    NivelPerfil.RECOMENDADO: Perfil(
        nivel=NivelPerfil.RECOMENDADO,
        nombre="Recomendado",
        descripcion="Balance entre optimización y funcionalidad. Ideal para la mayoría.",
        tweaks=[
            "deshabilitar_telemetria",
            "deshabilitar_cortana",
            "deshabilitar_ads",
            "deshabilitar_historial",
            "deshabilitar_ubicacion",
            "deshabilitar_game_bar",
            "deshabilitar_xbox",
            "deshabilitar_widgets",
            "deshabilitar_chat",
            "deshabilitar_copilot",
            "optimizar_visual",
            "plan_ultimate",
        ],
        deshabilitar_servicios=True,
        eliminar_bloatware=True,
        limpiar_sistema=True
    ),

    NivelPerfil.MAXIMO: Perfil(
        nivel=NivelPerfil.MAXIMO,
        nombre="Máximo",
        descripcion="Optimización agresiva. Deshabilita todo lo posible para máximo rendimiento.",
        tweaks=[
            "deshabilitar_superfetch",
            "deshabilitar_indexacion",
            "deshabilitar_telemetria",
            "deshabilitar_cortana",
            "deshabilitar_ads",
            "deshabilitar_historial",
            "deshabilitar_ubicacion",
            "deshabilitar_background",
            "deshabilitar_game_bar",
            "deshabilitar_xbox",
            "deshabilitar_widgets",
            "deshabilitar_chat",
            "deshabilitar_copilot",
            "deshabilitar_phone",
            "deshabilitar_hibernacion",
            "optimizar_visual",
            "plan_ultimate",
            "menu_clasico",
            "barra_izquierda",
            "ocultar_busqueda",
        ],
        deshabilitar_servicios=True,
        eliminar_bloatware=True,
        limpiar_sistema=True
    ),

    NivelPerfil.GAMING: Perfil(
        nivel=NivelPerfil.GAMING,
        nombre="Gaming",
        descripcion="Optimizado para juegos. Mantiene Xbox Game Bar funcional.",
        tweaks=[
            "deshabilitar_superfetch",
            "deshabilitar_indexacion",
            "deshabilitar_telemetria",
            "deshabilitar_cortana",
            "deshabilitar_ads",
            "deshabilitar_historial",
            "deshabilitar_ubicacion",
            "deshabilitar_background",
            "deshabilitar_widgets",
            "deshabilitar_chat",
            "deshabilitar_copilot",
            "deshabilitar_phone",
            "optimizar_visual",
            "plan_ultimate",
        ],
        deshabilitar_servicios=True,
        eliminar_bloatware=True,
        limpiar_sistema=True
    ),

    NivelPerfil.PRODUCTIVIDAD: Perfil(
        nivel=NivelPerfil.PRODUCTIVIDAD,
        nombre="Productividad",
        descripcion="Optimizado para trabajo. Mantiene búsqueda e indexación.",
        tweaks=[
            "deshabilitar_telemetria",
            "deshabilitar_cortana",
            "deshabilitar_ads",
            "deshabilitar_historial",
            "deshabilitar_game_bar",
            "deshabilitar_xbox",
            "deshabilitar_widgets",
            "deshabilitar_copilot",
            "plan_ultimate",
            "menu_clasico",
        ],
        deshabilitar_servicios=True,
        eliminar_bloatware=True,
        limpiar_sistema=True
    ),
}


def aplicar_perfil(nivel: NivelPerfil, callback: Callable[[str, int], None] | None = None) -> ResultadoPerfil:
    """
    Aplica un perfil de optimización completo.

    Args:
        nivel: El nivel de perfil a aplicar
        callback: Función opcional para reportar progreso (mensaje, porcentaje)

    Returns:
        ResultadoPerfil con los resultados de la operación
    """
    perfil = PERFILES[nivel]

    tweaks_ok = 0
    tweaks_fail = 0
    servicios_ok = 0
    apps_ok = 0
    espacio = 0.0
    reinicio = False

    total_pasos = len(perfil.tweaks)
    if perfil.deshabilitar_servicios:
        total_pasos += 1
    if perfil.eliminar_bloatware:
        total_pasos += 1
    if perfil.limpiar_sistema:
        total_pasos += 1

    paso_actual = 0

    # 1. Aplicar tweaks
    for tweak_id in perfil.tweaks:
        paso_actual += 1
        tweak = tweaks.obtener_tweak_por_id(tweak_id)

        if tweak:
            if callback:
                callback(f"Aplicando: {tweak.nombre}", int((paso_actual / total_pasos) * 100))

            exito, _ = tweak.aplicar()
            if exito:
                tweaks_ok += 1
                if tweak.requiere_reinicio:
                    reinicio = True
            else:
                tweaks_fail += 1

    # 2. Deshabilitar servicios
    if perfil.deshabilitar_servicios:
        paso_actual += 1
        if callback:
            callback("Deshabilitando servicios...", int((paso_actual / total_pasos) * 100))

        if nivel == NivelPerfil.MAXIMO:
            ok, _ = servicios.aplicar_perfil_maximo()
        elif nivel == NivelPerfil.MINIMO:
            ok, _ = servicios.aplicar_perfil_minimo()
        else:
            ok, _ = servicios.aplicar_perfil_recomendado()
        servicios_ok = ok

    # 3. Eliminar bloatware
    if perfil.eliminar_bloatware:
        paso_actual += 1
        if callback:
            callback("Eliminando bloatware...", int((paso_actual / total_pasos) * 100))

        ok, _ = bloatware.eliminar_todo_bloatware_recomendado()
        apps_ok = ok

    # 4. Limpiar sistema
    if perfil.limpiar_sistema:
        paso_actual += 1
        if callback:
            callback("Limpiando sistema...", int((paso_actual / total_pasos) * 100))

        resultados = limpieza.ejecutar_limpieza_completa()
        for r in resultados:
            espacio += r.espacio_liberado_mb

    if callback:
        callback("¡Completado!", 100)

    return ResultadoPerfil(
        nombre=perfil.nombre,
        tweaks_aplicados=tweaks_ok,
        tweaks_fallidos=tweaks_fail,
        servicios_deshabilitados=servicios_ok,
        apps_eliminadas=apps_ok,
        espacio_liberado_mb=round(espacio, 2),
        requiere_reinicio=reinicio
    )


def obtener_descripcion_perfil(nivel: NivelPerfil) -> str:
    """Obtiene la descripción de un perfil."""
    return PERFILES[nivel].descripcion


def obtener_tweaks_perfil(nivel: NivelPerfil) -> list[str]:
    """Obtiene la lista de tweaks de un perfil."""
    return PERFILES[nivel].tweaks
