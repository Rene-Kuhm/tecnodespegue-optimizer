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
from src.utils.admin import es_administrador, solicitar_admin


class TecnodespegueOptimizer:
    """Aplicación principal de Tecnodespegue Optimizer."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.pagina_actual = 0
        self.contenido = None
        self.nav_rail = None

        self._configurar_pagina()
        self._construir_ui()

    def _configurar_pagina(self):
        """Configura la página principal."""
        self.page.title = "Tecnodespegue Optimizer - Windows 11 25H2"
        self.page.bgcolor = theme.COLORS["background"]
        self.page.padding = 0
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.min_width = 900
        self.page.window.min_height = 600
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.center()

        # Tema personalizado
        self.page.theme = ft.Theme(
            color_scheme_seed=theme.COLORS["primary"],
            font_family="Segoe UI",
        )

    def _construir_ui(self):
        """Construye la interfaz de usuario."""
        # Verificar permisos de administrador
        if not es_administrador():
            self._mostrar_advertencia_admin()

        # Navegación lateral con altura fija
        nav_items = [
            (ft.Icons.DASHBOARD_ROUNDED, "Inicio"),
            (ft.Icons.TUNE_ROUNDED, "Tweaks"),
            (ft.Icons.DELETE_SWEEP_ROUNDED, "Bloatware"),
            (ft.Icons.CLEANING_SERVICES_ROUNDED, "Limpieza"),
            (ft.Icons.SETTINGS_APPLICATIONS_ROUNDED, "Servicios"),
        ]

        self.nav_rail = ft.NavigationRail(
            selected_index=self.pagina_actual,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            bgcolor=theme.COLORS["surface"],
            indicator_color=theme.COLORS["primary"],
            height=300,  # Altura fija para evitar el error
            destinations=[
                ft.NavigationRailDestination(
                    icon=icono,
                    selected_icon=icono,
                    label=nombre,
                )
                for icono, nombre in nav_items
            ],
            on_change=self._cambiar_pagina,
        )

        # Logo profesional en la parte superior
        logo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.ROCKET_LAUNCH_ROUNDED, size=48, color=theme.COLORS["primary"]),
                        padding=10,
                        border_radius=15,
                        bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                    ),
                    ft.Text(
                        "Tecnodespegue",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "OPTIMIZER",
                        size=10,
                        weight=ft.FontWeight.W_600,
                        color=theme.COLORS["primary"],
                        text_align=ft.TextAlign.CENTER,
                        letter_spacing=2,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            padding=ft.padding.symmetric(vertical=24, horizontal=10),
            alignment=ft.alignment.center,
        )

        # Estado de admin con mejor diseño
        is_admin = es_administrador()
        admin_badge = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.VERIFIED_USER_ROUNDED if is_admin else ft.Icons.SHIELD_OUTLINED,
                        size=20,
                        color=theme.COLORS["success"] if is_admin else theme.COLORS["warning"],
                    ),
                    ft.Text(
                        "Administrador" if is_admin else "Usuario",
                        size=10,
                        weight=ft.FontWeight.W_500,
                        color=theme.COLORS["success"] if is_admin else theme.COLORS["warning"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=ft.padding.symmetric(vertical=12, horizontal=16),
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["success"] if is_admin else theme.COLORS["warning"]),
            margin=ft.margin.symmetric(horizontal=10),
        )

        # Versión
        version_text = ft.Container(
            content=ft.Text(
                "v1.0.0",
                size=10,
                color=theme.COLORS["text_secondary"],
                text_align=ft.TextAlign.CENTER,
            ),
            padding=ft.padding.only(bottom=16),
        )

        # Panel lateral completo con altura expandida
        sidebar = ft.Container(
            content=ft.Column(
                controls=[
                    logo,
                    ft.Divider(height=1, color=theme.COLORS["surface_light"]),
                    ft.Container(
                        content=self.nav_rail,
                        padding=ft.padding.symmetric(vertical=10),
                    ),
                    ft.Container(expand=True),  # Espacio flexible
                    admin_badge,
                    version_text,
                ],
                spacing=0,
            ),
            width=130,
            bgcolor=theme.COLORS["surface"],
            expand=True,
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
                    ft.VerticalDivider(width=1, color=theme.COLORS["surface_light"]),
                    self.contenido,
                ],
                expand=True,
                spacing=0,
            )
        )

    def _cambiar_pagina(self, e):
        """Cambia la página actual."""
        self.pagina_actual = e.control.selected_index

        paginas = [
            lambda: PaginaInicio(self.page),
            lambda: PaginaTweaks(self.page),
            lambda: PaginaBloatware(self.page),
            lambda: PaginaLimpieza(self.page),
            lambda: PaginaServicios(self.page),
        ]

        self.contenido.content = paginas[self.pagina_actual]()
        self.page.update()

    def _mostrar_advertencia_admin(self):
        """Muestra una advertencia si no hay permisos de admin."""
        def cerrar_dialogo(e):
            dialogo.open = False
            self.page.update()

        def solicitar_permisos(e):
            dialogo.open = False
            self.page.update()
            # Cerrar esta ventana antes de abrir como admin
            self.page.window.close()
            solicitar_admin()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, color=theme.COLORS["primary"], size=28),
                    ft.Text("Permisos de Administrador", weight=ft.FontWeight.BOLD),
                ],
                spacing=12,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Tecnodespegue Optimizer necesita permisos de administrador "
                            "para aplicar la mayoría de las optimizaciones.",
                            size=14,
                            color=theme.COLORS["text_secondary"],
                        ),
                        ft.Container(height=8),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=16, color=theme.COLORS["info"]),
                                    ft.Text(
                                        "Sin admin, algunas funciones estarán limitadas.",
                                        size=12,
                                        color=theme.COLORS["info"],
                                    ),
                                ],
                                spacing=8,
                            ),
                            padding=12,
                            border_radius=8,
                            bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["info"]),
                        ),
                    ],
                ),
                width=400,
            ),
            actions=[
                ft.TextButton(
                    "Continuar sin admin",
                    on_click=cerrar_dialogo,
                    style=ft.ButtonStyle(color=theme.COLORS["text_secondary"]),
                ),
                ft.ElevatedButton(
                    "Ejecutar como Admin",
                    icon=ft.Icons.SHIELD_ROUNDED,
                    on_click=solicitar_permisos,
                    style=ft.ButtonStyle(
                        bgcolor=theme.COLORS["primary"],
                        color=ft.Colors.WHITE,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16),
        )

        self.page.overlay.append(dialogo)
        dialogo.open = True
        self.page.update()


def main(page: ft.Page):
    """Punto de entrada de la aplicación."""
    TecnodespegueOptimizer(page)


if __name__ == "__main__":
    ft.app(target=main)
