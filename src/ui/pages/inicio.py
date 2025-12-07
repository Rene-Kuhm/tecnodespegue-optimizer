"""Página de inicio con información del sistema y perfiles rápidos."""
import flet as ft
from src.ui import theme
from src.utils.system_info import obtener_info_sistema, obtener_procesos_top
from src.modules.perfiles import NivelPerfil, aplicar_perfil, PERFILES
import threading


def crear_pagina_inicio(page: ft.Page = None) -> ft.Column:
    """Crea la página principal con dashboard del sistema."""

    # Obtener info del sistema
    try:
        info_sistema = obtener_info_sistema()
    except:
        info_sistema = None

    # Barra de progreso (oculta inicialmente)
    progreso_bar = ft.ProgressBar(
        value=0,
        color=theme.COLORS["primary"],
        bgcolor=theme.COLORS["surface_light"],
        height=8,
        border_radius=4,
        visible=False,
    )

    estado_texto = ft.Text(
        "",
        size=14,
        color=theme.COLORS["text_secondary"],
        visible=False,
    )

    def crear_header() -> ft.Container:
        """Crea el encabezado de bienvenida premium."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.ROCKET_LAUNCH_ROUNDED, size=56, color=theme.COLORS["primary"]),
                        padding=16,
                        border_radius=20,
                        bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Tecnodespegue Optimizer",
                                size=36,
                                weight=ft.FontWeight.BOLD,
                                color=theme.COLORS["text"],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text("Windows 11", size=12, color=theme.COLORS["secondary"]),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                        border_radius=12,
                                        bgcolor=ft.Colors.with_opacity(0.15, theme.COLORS["secondary"]),
                                    ),
                                    ft.Container(
                                        content=ft.Text("25H2", size=12, color=theme.COLORS["primary"]),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                        border_radius=12,
                                        bgcolor=ft.Colors.with_opacity(0.15, theme.COLORS["primary"]),
                                    ),
                                    ft.Text(
                                        "Optimiza, limpia y acelera tu sistema",
                                        size=14,
                                        color=theme.COLORS["text_secondary"],
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=20,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=20),
        )

    def crear_stat_card(titulo: str, valor: str, subtitulo: str, icono, color: str, porcentaje: float = None) -> ft.Container:
        """Crea una tarjeta de estadística premium."""
        contenido = [
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=24, color=color),
                        padding=12,
                        border_radius=12,
                        bgcolor=ft.Colors.with_opacity(0.15, color),
                    ),
                ],
            ),
            ft.Container(height=16),
            ft.Text(valor, size=22, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
            ft.Text(titulo, size=13, weight=ft.FontWeight.W_500, color=theme.COLORS["text_secondary"]),
            ft.Text(subtitulo, size=11, color=theme.COLORS["text_muted"]),
        ]

        # Añadir barra de progreso si hay porcentaje
        if porcentaje is not None:
            contenido.append(ft.Container(height=8))
            contenido.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                width=porcentaje * 1.4,
                                height=6,
                                border_radius=3,
                                bgcolor=color,
                            ),
                        ],
                    ),
                    width=140,
                    height=6,
                    border_radius=3,
                    bgcolor=theme.COLORS["surface_elevated"],
                )
            )

        return ft.Container(
            content=ft.Column(controls=contenido, spacing=4),
            padding=20,
            border_radius=theme.BORDER_RADIUS,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
            width=200,
        )

    def crear_info_sistema() -> ft.Container:
        """Crea la sección de información del sistema."""
        if not info_sistema:
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.WARNING_ROUNDED, color=theme.COLORS["warning"]),
                        ft.Text("No se pudo obtener información del sistema", color=theme.COLORS["warning"]),
                    ],
                    spacing=10,
                ),
                padding=20,
            )

        info = info_sistema

        stats = ft.Row(
            controls=[
                crear_stat_card(
                    "Procesador",
                    info.cpu[:20] + "..." if len(info.cpu) > 20 else info.cpu,
                    f"{info.nucleos} núcleos disponibles",
                    ft.Icons.MEMORY_ROUNDED,
                    theme.COLORS["primary"],
                ),
                crear_stat_card(
                    "Memoria RAM",
                    f"{info.ram_disponible_gb:.1f} GB",
                    f"de {info.ram_total_gb:.1f} GB totales",
                    ft.Icons.STORAGE_ROUNDED,
                    theme.COLORS["secondary"] if info.ram_uso_porcentaje < 70 else theme.COLORS["warning"],
                    porcentaje=info.ram_uso_porcentaje,
                ),
                crear_stat_card(
                    "Disco Principal",
                    f"{info.disco_libre_gb:.1f} GB",
                    f"de {info.disco_total_gb:.1f} GB totales",
                    ft.Icons.SD_STORAGE_ROUNDED,
                    theme.COLORS["info"],
                    porcentaje=(info.disco_total_gb - info.disco_libre_gb) / info.disco_total_gb * 100 if info.disco_total_gb > 0 else 0,
                ),
                crear_stat_card(
                    "Sistema",
                    f"Build {info.build}",
                    info.arquitectura,
                    ft.Icons.DESKTOP_WINDOWS_ROUNDED,
                    theme.COLORS["primary"],
                ),
            ],
            wrap=True,
            spacing=16,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    theme.crear_seccion_header(
                        "Estado del Sistema",
                        "Información en tiempo real de tu equipo",
                    ),
                    stats,
                ],
            ),
            padding=ft.padding.symmetric(horizontal=24),
        )

    def aplicar_perfil_click(nivel: NivelPerfil):
        """Aplica un perfil de optimización."""
        progreso_bar.visible = True
        estado_texto.visible = True
        progreso_bar.value = 0
        estado_texto.value = "Iniciando optimización..."
        estado_texto.color = theme.COLORS["text_secondary"]
        if page:
            page.update()

        def callback(mensaje: str, porcentaje: int):
            progreso_bar.value = porcentaje / 100
            estado_texto.value = mensaje
            if page:
                page.update()

        def ejecutar():
            try:
                resultado = aplicar_perfil(nivel, callback)
                estado_texto.value = (
                    f"Completado: {resultado.tweaks_aplicados} tweaks, "
                    f"{resultado.servicios_deshabilitados} servicios, "
                    f"{resultado.apps_eliminadas} apps, "
                    f"{resultado.espacio_liberado_mb:.1f} MB liberados"
                )
                estado_texto.color = theme.COLORS["success"]
                if resultado.requiere_reinicio:
                    estado_texto.value += " - Reinicio recomendado"
            except Exception as e:
                estado_texto.value = f"Error: {str(e)}"
                estado_texto.color = theme.COLORS["error"]
            progreso_bar.visible = False
            if page:
                page.update()

        thread = threading.Thread(target=ejecutar)
        thread.start()

    def crear_perfiles_rapidos() -> ft.Container:
        """Crea la sección de perfiles de optimización rápida."""
        perfiles = [
            (NivelPerfil.MINIMO, ft.Icons.VERIFIED_USER_ROUNDED, "Seguro", theme.COLORS["success"], "Sin riesgos"),
            (NivelPerfil.RECOMENDADO, ft.Icons.THUMB_UP_ROUNDED, "Recomendado", theme.COLORS["primary"], "Equilibrado"),
            (NivelPerfil.MAXIMO, ft.Icons.BOLT_ROUNDED, "Agresivo", theme.COLORS["warning"], "Máximo rendimiento"),
            (NivelPerfil.GAMING, ft.Icons.SPORTS_ESPORTS_ROUNDED, "Gaming", theme.COLORS["error"], "Para juegos"),
            (NivelPerfil.PRODUCTIVIDAD, ft.Icons.WORK_ROUNDED, "Trabajo", theme.COLORS["info"], "Productividad"),
        ]

        botones = []
        for nivel, icono, etiqueta, color, desc in perfiles:
            perfil = PERFILES[nivel]
            btn = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icono, size=32, color=color),
                            padding=14,
                            border_radius=16,
                            bgcolor=ft.Colors.with_opacity(0.15, color),
                        ),
                        ft.Container(height=8),
                        ft.Text(perfil.nombre, size=14, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
                        ft.Text(desc, size=11, color=theme.COLORS["text_muted"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                padding=20,
                border_radius=theme.BORDER_RADIUS,
                bgcolor=theme.COLORS["surface"],
                border=ft.border.all(1, theme.COLORS["border"]),
                on_click=lambda e, n=nivel: aplicar_perfil_click(n),
                ink=True,
                width=150,
            )
            botones.append(btn)

        return ft.Container(
            content=ft.Column(
                controls=[
                    theme.crear_seccion_header(
                        "Optimización Rápida",
                        "Selecciona un perfil para optimizar tu sistema",
                    ),
                    ft.Row(controls=botones, wrap=True, spacing=16),
                    ft.Container(height=16),
                    progreso_bar,
                    estado_texto,
                ],
            ),
            padding=ft.padding.symmetric(horizontal=24),
        )

    def crear_procesos_top() -> ft.Container:
        """Crea la sección de procesos que más consumen."""
        try:
            procesos = obtener_procesos_top(6)
        except:
            procesos = []

        if not procesos:
            return ft.Container()

        max_memoria = max(p['memoria_mb'] for p in procesos) if procesos else 1

        filas = []
        for i, proc in enumerate(procesos):
            porcentaje = (proc['memoria_mb'] / max_memoria) * 100
            color = theme.COLORS["primary"] if i < 2 else theme.COLORS["secondary"] if i < 4 else theme.COLORS["info"]

            filas.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(f"{i+1}", size=12, weight=ft.FontWeight.BOLD, color=theme.COLORS["text_muted"]),
                                width=24,
                                height=24,
                                border_radius=12,
                                bgcolor=theme.COLORS["surface_elevated"],
                                alignment=ft.alignment.center,
                            ),
                            ft.Text(proc['nombre'][:28], size=13, color=theme.COLORS["text"], expand=True),
                            ft.Text(f"{proc['memoria_mb']:.0f} MB", size=13, weight=ft.FontWeight.W_500, color=color),
                            ft.Container(
                                content=ft.Container(
                                    width=porcentaje,
                                    height=8,
                                    border_radius=4,
                                    bgcolor=color,
                                ),
                                width=100,
                                height=8,
                                border_radius=4,
                                bgcolor=theme.COLORS["surface_elevated"],
                            ),
                        ],
                        spacing=16,
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=16),
                    border_radius=theme.BORDER_RADIUS_SM,
                    bgcolor=theme.COLORS["surface_light"] if i % 2 == 0 else theme.COLORS["surface"],
                )
            )

        return ft.Container(
            content=ft.Column(
                controls=[
                    theme.crear_seccion_header(
                        "Consumo de Recursos",
                        "Procesos que más memoria utilizan",
                    ),
                    ft.Container(
                        content=ft.Column(controls=filas, spacing=4),
                        border_radius=theme.BORDER_RADIUS,
                        bgcolor=theme.COLORS["surface"],
                        border=ft.border.all(1, theme.COLORS["border"]),
                        padding=8,
                    ),
                ],
            ),
            padding=ft.padding.symmetric(horizontal=24),
        )

    return ft.Column(
        controls=[
            crear_header(),
            ft.Container(height=10),
            crear_info_sistema(),
            ft.Container(height=24),
            crear_perfiles_rapidos(),
            ft.Container(height=24),
            crear_procesos_top(),
            ft.Container(height=24),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


# Para compatibilidad
class PaginaInicio:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_inicio(page)
