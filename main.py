"""
Tecnodespegue Optimizer - Utilidad de Optimización para Windows 11 25H2
Desarrollado con Python y Flet

Optimiza tu sistema Windows eliminando bloatware, aplicando tweaks de rendimiento,
limpiando archivos temporales y gestionando servicios innecesarios.
"""
import flet as ft
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui import theme
from src.ui.pages.inicio import PaginaInicio
from src.ui.pages.tweaks import PaginaTweaks
from src.ui.pages.bloatware import PaginaBloatware
from src.ui.pages.limpieza import PaginaLimpieza
from src.ui.pages.servicios import PaginaServicios
from src.ui.pages.drivers import PaginaDrivers
from src.utils.admin import es_administrador, solicitar_admin


class TecnodespegueOptimizer:
    """Aplicación principal de Tecnodespegue Optimizer."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.pagina_actual = 0
        self.contenido = None
        self.nav_items_refs = []

        self._configurar_pagina()
        self._construir_ui()

    def _configurar_pagina(self):
        """Configura la página principal."""
        self.page.title = "Tecnodespegue Optimizer"
        self.page.bgcolor = theme.COLORS["background"]
        self.page.padding = 0
        self.page.window.width = 1400
        self.page.window.height = 900
        self.page.window.min_width = 1100
        self.page.window.min_height = 700
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.center()

        # Tema personalizado
        self.page.theme = ft.Theme(
            color_scheme_seed=theme.COLORS["primary"],
            font_family="Segoe UI",
        )

    def _construir_ui(self):
        """Construye la interfaz de usuario estilo CleanMyMac X."""
        # Verificar permisos de administrador
        if not es_administrador():
            self._mostrar_advertencia_admin()

        # Definir items de navegación con colores únicos
        nav_items = [
            (ft.Icons.SPEED_ROUNDED, "Escaneo", theme.COLORS["scan_blue"]),
            (ft.Icons.TUNE_ROUNDED, "Tweaks", theme.COLORS["scan_purple"]),
            (ft.Icons.DELETE_SWEEP_ROUNDED, "Bloatware", theme.COLORS["protect_red"]),
            (ft.Icons.CLEANING_SERVICES_ROUNDED, "Limpieza", theme.COLORS["clean_green"]),
            (ft.Icons.MISCELLANEOUS_SERVICES_ROUNDED, "Servicios", theme.COLORS["speed_orange"]),
            (ft.Icons.DEVELOPER_BOARD_ROUNDED, "Drivers", theme.COLORS["apps_cyan"]),
        ]

        # Crear items de navegación
        self.nav_items_refs = []
        nav_controls = []

        for i, (icono, label, color) in enumerate(nav_items):
            item = self._crear_nav_item(icono, label, color, i)
            self.nav_items_refs.append(item)
            nav_controls.append(item)

        # Logo con efecto glow
        logo_container = ft.Container(
            content=ft.Column(
                controls=[
                    # Logo circular con gradiente
                    ft.Container(
                        content=ft.Stack(
                            controls=[
                                # Glow effect
                                ft.Container(
                                    width=72,
                                    height=72,
                                    border_radius=36,
                                    shadow=theme.SHADOW_GLOW_CYAN,
                                ),
                                # Main circle
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.ROCKET_LAUNCH_ROUNDED,
                                        size=32,
                                        color=ft.Colors.WHITE,
                                    ),
                                    width=64,
                                    height=64,
                                    border_radius=32,
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.bottom_right,
                                        colors=theme.COLORS["gradient_scan"],
                                    ),
                                    alignment=ft.alignment.center,
                                    left=4,
                                    top=4,
                                ),
                            ],
                        ),
                        width=72,
                        height=72,
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        "Tecnodespegue",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                    ),
                    ft.Text(
                        "O P T I M I Z E R",
                        size=9,
                        weight=ft.FontWeight.W_600,
                        color=theme.COLORS["scan_blue"],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            padding=ft.padding.only(top=32, bottom=24),
        )

        # Separador con gradiente
        separator = ft.Container(
            content=ft.Container(
                width=40,
                height=2,
                border_radius=1,
                gradient=ft.LinearGradient(
                    colors=[
                        ft.Colors.TRANSPARENT,
                        theme.COLORS["scan_blue"],
                        ft.Colors.TRANSPARENT,
                    ],
                ),
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=20),
        )

        # Navegación
        nav_column = ft.Container(
            content=ft.Column(
                controls=nav_controls,
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=8),
        )

        # Estado de admin
        is_admin = es_administrador()
        admin_status = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SHIELD_ROUNDED if is_admin else ft.Icons.SHIELD_OUTLINED,
                            size=18,
                            color=ft.Colors.WHITE,
                        ),
                        width=36,
                        height=36,
                        border_radius=18,
                        bgcolor=theme.COLORS["success"] if is_admin else theme.COLORS["warning"],
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Admin" if is_admin else "Usuario",
                        size=10,
                        weight=ft.FontWeight.W_500,
                        color=theme.COLORS["text_muted"],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=ft.padding.only(bottom=8),
        )

        # Versión
        version_badge = ft.Container(
            content=ft.Text(
                "v1.0.0",
                size=10,
                color=theme.COLORS["text_muted"],
            ),
            padding=ft.padding.only(bottom=16),
        )

        # Sidebar estilo CleanMyMac
        sidebar = ft.Container(
            content=ft.Column(
                controls=[
                    logo_container,
                    separator,
                    nav_column,
                    ft.Container(expand=True),
                    admin_status,
                    version_badge,
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=110,
            bgcolor=theme.COLORS["sidebar"],
            border=ft.border.only(right=ft.BorderSide(1, theme.COLORS["border"])),
        )

        # Contenido principal
        self.contenido = ft.Container(
            content=PaginaInicio(self.page),
            expand=True,
            padding=0,
            bgcolor=theme.COLORS["background"],
        )

        # Layout principal
        self.page.add(
            ft.Row(
                controls=[
                    sidebar,
                    self.contenido,
                ],
                expand=True,
                spacing=0,
            )
        )

    def _crear_nav_item(self, icono, texto: str, color: str, index: int) -> ft.Container:
        """Crea un item de navegación vertical estilo CleanMyMac."""
        is_selected = index == self.pagina_actual

        # Contenedor del icono
        icon_container = ft.Container(
            content=ft.Icon(
                icono,
                size=22,
                color=color if is_selected else theme.COLORS["text_muted"],
            ),
            width=44,
            height=44,
            border_radius=14,
            bgcolor=ft.Colors.with_opacity(0.15, color) if is_selected else None,
            alignment=ft.alignment.center,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    icon_container,
                    ft.Text(
                        texto,
                        size=10,
                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_400,
                        color=color if is_selected else theme.COLORS["text_muted"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=4),
            border_radius=theme.BORDER_RADIUS,
            bgcolor=ft.Colors.with_opacity(0.08, color) if is_selected else None,
            on_click=lambda e, idx=index: self._cambiar_pagina(idx),
            ink=True,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            data={"index": index, "color": color},
        )

    def _cambiar_pagina(self, index: int):
        """Cambia la página actual."""
        self.pagina_actual = index

        # Colores por índice
        colores = [
            theme.COLORS["scan_blue"],
            theme.COLORS["scan_purple"],
            theme.COLORS["protect_red"],
            theme.COLORS["clean_green"],
            theme.COLORS["speed_orange"],
            theme.COLORS["apps_cyan"],
        ]

        # Actualizar estilos de navegación
        for i, item in enumerate(self.nav_items_refs):
            is_selected = i == index
            color = colores[i]

            # Actualizar contenedor del icono
            icon_container = item.content.controls[0]
            icon_container.content.color = color if is_selected else theme.COLORS["text_muted"]
            icon_container.bgcolor = ft.Colors.with_opacity(0.15, color) if is_selected else None

            # Actualizar texto
            item.content.controls[1].weight = ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_400
            item.content.controls[1].color = color if is_selected else theme.COLORS["text_muted"]

            # Actualizar fondo del item
            item.bgcolor = ft.Colors.with_opacity(0.08, color) if is_selected else None

        # Crear la página según el índice
        nueva_pagina = None
        if index == 0:
            nueva_pagina = PaginaInicio(self.page)
        elif index == 1:
            nueva_pagina = PaginaTweaks(self.page)
        elif index == 2:
            nueva_pagina = PaginaBloatware(self.page)
        elif index == 3:
            nueva_pagina = PaginaLimpieza(self.page)
        elif index == 4:
            nueva_pagina = PaginaServicios(self.page)
        elif index == 5:
            nueva_pagina = PaginaDrivers(self.page)

        if nueva_pagina:
            self.contenido.content = nueva_pagina
            self.page.update()

    def _mostrar_advertencia_admin(self):
        """Muestra una advertencia si no hay permisos de admin."""
        def cerrar_dialogo(e):
            dialogo.open = False
            self.page.update()

        def solicitar_permisos(e):
            dialogo.open = False
            self.page.update()
            self.page.window.close()
            solicitar_admin()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.SHIELD_ROUNDED, color=ft.Colors.WHITE, size=22),
                        width=44,
                        height=44,
                        border_radius=14,
                        gradient=ft.LinearGradient(
                            colors=theme.COLORS["gradient_scan"],
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=12),
                    ft.Text("Permisos Requeridos", size=18, weight=ft.FontWeight.BOLD),
                ],
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Tecnodespegue Optimizer necesita permisos de administrador "
                            "para aplicar las optimizaciones del sistema.",
                            size=14,
                            color=theme.COLORS["text_secondary"],
                        ),
                        ft.Container(height=16),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.INFO_OUTLINE_ROUNDED,
                                        size=18,
                                        color=theme.COLORS["info"],
                                    ),
                                    ft.Container(width=8),
                                    ft.Text(
                                        "Sin privilegios elevados, algunas funciones estarán limitadas.",
                                        size=13,
                                        color=theme.COLORS["info"],
                                    ),
                                ],
                            ),
                            padding=16,
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["info"]),
                        ),
                    ],
                ),
                width=420,
            ),
            actions=[
                ft.TextButton(
                    "Continuar sin admin",
                    on_click=cerrar_dialogo,
                    style=ft.ButtonStyle(color=theme.COLORS["text_muted"]),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SHIELD_ROUNDED, size=16, color=ft.Colors.WHITE),
                            ft.Container(width=6),
                            ft.Text(
                                "Ejecutar como Admin",
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=10,
                    gradient=ft.LinearGradient(
                        colors=theme.COLORS["gradient_scan"],
                    ),
                    on_click=solicitar_permisos,
                    ink=True,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=theme.COLORS["surface"],
        )

        self.page.overlay.append(dialogo)
        dialogo.open = True
        self.page.update()


def main(page: ft.Page):
    """Punto de entrada de la aplicación."""
    TecnodespegueOptimizer(page)


if __name__ == "__main__":
    ft.app(target=main)
