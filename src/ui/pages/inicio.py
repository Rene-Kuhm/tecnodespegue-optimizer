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
        height=6,
        border_radius=3,
        visible=False,
    )

    estado_texto = ft.Text(
        "",
        size=14,
        color=theme.COLORS["text_secondary"],
        visible=False,
    )

    def crear_header() -> ft.Container:
        """Crea el encabezado de bienvenida."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ROCKET_LAUNCH, size=40, color=theme.COLORS["primary"]),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Tecnodespegue Optimizer",
                                        size=32,
                                        weight=ft.FontWeight.BOLD,
                                        color=theme.COLORS["text"],
                                    ),
                                    ft.Text(
                                        "Optimizador de Windows 11 25H2 en Español",
                                        size=14,
                                        color=theme.COLORS["text_secondary"],
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=16,
                    ),
                ],
            ),
            padding=20,
        )

    def crear_stat_card(titulo: str, valor: str, subtitulo: str, icono, color: str) -> ft.Container:
        """Crea una tarjeta de estadística."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icono, size=24, color=color),
                            ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
                        ],
                        spacing=8,
                    ),
                    ft.Text(valor, size=16, weight=ft.FontWeight.W_500, color=color),
                    ft.Text(subtitulo, size=12, color=theme.COLORS["text_secondary"]),
                ],
                spacing=4,
            ),
            padding=16,
            border_radius=theme.BORDER_RADIUS_SM,
            bgcolor=theme.COLORS["surface_light"],
            width=200,
        )

    def crear_info_sistema() -> ft.Container:
        """Crea la sección de información del sistema."""
        if not info_sistema:
            return ft.Container(
                content=ft.Text("No se pudo obtener información del sistema", color=theme.COLORS["error"]),
            )

        info = info_sistema

        stats = ft.Row(
            controls=[
                crear_stat_card(
                    "CPU",
                    info.cpu[:30] + "..." if len(info.cpu) > 30 else info.cpu,
                    f"{info.nucleos} núcleos",
                    ft.Icons.MEMORY,
                    theme.COLORS["primary"],
                ),
                crear_stat_card(
                    "RAM",
                    f"{info.ram_disponible_gb:.1f} GB libres",
                    f"de {info.ram_total_gb:.1f} GB ({info.ram_uso_porcentaje:.0f}% usado)",
                    ft.Icons.STORAGE,
                    theme.COLORS["secondary"] if info.ram_uso_porcentaje < 70 else theme.COLORS["warning"],
                ),
                crear_stat_card(
                    "Disco C:",
                    f"{info.disco_libre_gb:.1f} GB libres",
                    f"de {info.disco_total_gb:.1f} GB",
                    ft.Icons.DISC_FULL,
                    theme.COLORS["info"],
                ),
                crear_stat_card(
                    "Windows",
                    f"Build {info.build}",
                    info.arquitectura,
                    ft.Icons.WINDOW,
                    theme.COLORS["primary"],
                ),
            ],
            wrap=True,
            spacing=16,
        )

        return theme.crear_card(
            ft.Column(
                controls=[
                    theme.crear_titulo("Estado del Sistema", 18),
                    ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
                    stats,
                ],
            ),
        )

    def aplicar_perfil_click(nivel: NivelPerfil):
        """Aplica un perfil de optimización."""
        progreso_bar.visible = True
        estado_texto.visible = True
        progreso_bar.value = 0
        estado_texto.value = "Iniciando optimización..."
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
                    f"¡Completado! Tweaks: {resultado.tweaks_aplicados}, "
                    f"Servicios: {resultado.servicios_deshabilitados}, "
                    f"Apps: {resultado.apps_eliminadas}, "
                    f"Liberado: {resultado.espacio_liberado_mb:.1f} MB"
                )
                estado_texto.color = theme.COLORS["success"]
                if resultado.requiere_reinicio:
                    estado_texto.value += " (Reinicio recomendado)"
            except Exception as e:
                estado_texto.value = f"Error: {str(e)}"
                estado_texto.color = theme.COLORS["error"]
            if page:
                page.update()

        thread = threading.Thread(target=ejecutar)
        thread.start()

    def crear_perfiles_rapidos() -> ft.Container:
        """Crea la sección de perfiles de optimización rápida."""
        perfiles = [
            (NivelPerfil.MINIMO, ft.Icons.SHIELD, "Seguro", theme.COLORS["success"]),
            (NivelPerfil.RECOMENDADO, ft.Icons.RECOMMEND, "Recomendado", theme.COLORS["primary"]),
            (NivelPerfil.MAXIMO, ft.Icons.BOLT, "Agresivo", theme.COLORS["warning"]),
            (NivelPerfil.GAMING, ft.Icons.SPORTS_ESPORTS, "Juegos", theme.COLORS["error"]),
            (NivelPerfil.PRODUCTIVIDAD, ft.Icons.WORK, "Trabajo", theme.COLORS["info"]),
        ]

        botones = []
        for nivel, icono, etiqueta, color in perfiles:
            perfil = PERFILES[nivel]
            btn = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(icono, size=32, color=color),
                        ft.Text(perfil.nombre, size=14, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
                        ft.Text(etiqueta, size=12, color=theme.COLORS["text_secondary"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                ),
                padding=20,
                border_radius=theme.BORDER_RADIUS,
                bgcolor=theme.COLORS["surface_light"],
                border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
                on_click=lambda e, n=nivel: aplicar_perfil_click(n),
                ink=True,
                width=140,
            )
            botones.append(btn)

        return theme.crear_card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            theme.crear_titulo("Optimización Rápida", 18),
                            ft.Container(
                                content=ft.Text("Click para aplicar", size=12, color=theme.COLORS["text_secondary"]),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        controls=botones,
                        wrap=True,
                        spacing=12,
                    ),
                ],
            ),
        )

    def crear_procesos_top() -> ft.Container:
        """Crea la sección de procesos que más consumen."""
        try:
            procesos = obtener_procesos_top(8)
        except:
            procesos = []

        if not procesos:
            return ft.Container()

        filas = []
        for proc in procesos:
            filas.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(proc['nombre'][:25], size=13, color=theme.COLORS["text"], width=180),
                            ft.Text(f"{proc['memoria_mb']:.0f} MB", size=13, color=theme.COLORS["warning"], width=80),
                            ft.Container(
                                content=ft.Container(
                                    width=min(proc['memoria_mb'] / 10, 100),
                                    height=8,
                                    border_radius=4,
                                    bgcolor=theme.COLORS["primary"],
                                ),
                                width=100,
                                height=8,
                                border_radius=4,
                                bgcolor=theme.COLORS["surface_light"],
                            ),
                        ],
                        spacing=16,
                    ),
                    padding=ft.padding.symmetric(vertical=6),
                )
            )

        return theme.crear_card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            theme.crear_titulo("Procesos con Mayor Consumo", 18),
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=18, color=theme.COLORS["text_secondary"]),
                        ],
                        spacing=8,
                    ),
                    ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
                    *filas,
                ],
            ),
        )

    return ft.Column(
        controls=[
            crear_header(),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            crear_info_sistema(),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            crear_perfiles_rapidos(),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            progreso_bar,
            estado_texto,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            crear_procesos_top(),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


# Para compatibilidad
class PaginaInicio:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_inicio(page)
