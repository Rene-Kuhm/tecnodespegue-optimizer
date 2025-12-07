"""
Tecnodespegue Optimizer - Utilidad de Optimización para Windows 11 25H2
Desarrollado con Python y Flet
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

        self._configurar_pagina()
        self._construir_ui()

    def _configurar_pagina(self):
        """Configura la página principal."""
        self.page.title = "Tecnodespegue Optimizer - Windows 11"
        self.page.bgcolor = theme.COLORS["background"]
        self.page.padding = 0
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.min_width = 900
        self.page.window.min_height = 600
        self.page.theme_mode = ft.ThemeMode.DARK

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

        # Navegación lateral
        nav_items = [
            (ft.Icons.DASHBOARD, "Inicio", 0),
            (ft.Icons.TUNE, "Tweaks", 1),
            (ft.Icons.DELETE_SWEEP, "Bloatware", 2),
            (ft.Icons.CLEANING_SERVICES, "Limpieza", 3),
            (ft.Icons.SETTINGS_APPLICATIONS, "Servicios", 4),
        ]

        nav_rail = ft.NavigationRail(
            selected_index=self.pagina_actual,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            bgcolor=theme.COLORS["surface"],
            indicator_color=theme.COLORS["primary"],
            destinations=[
                ft.NavigationRailDestination(
                    icon=icono,
                    selected_icon=icono,
                    label=nombre,
                )
                for icono, nombre, _ in nav_items
            ],
            on_change=self._cambiar_pagina,
        )

        # Logo en la parte superior del nav
        logo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.ROCKET_LAUNCH, size=40, color=theme.COLORS["primary"]),
                    ft.Text(
                        "Tecnodespegue",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Optimizer",
                        size=11,
                        weight=ft.FontWeight.W_500,
                        color=theme.COLORS["primary"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "v1.0",
                        size=11,
                        color=theme.COLORS["text_secondary"],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=20,
            alignment=ft.alignment.center,
        )

        # Estado de admin
        admin_badge = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.ADMIN_PANEL_SETTINGS if es_administrador() else ft.Icons.WARNING,
                        size=16,
                        color=theme.COLORS["success"] if es_administrador() else theme.COLORS["warning"],
                    ),
                    ft.Text(
                        "Admin" if es_administrador() else "Sin Admin",
                        size=11,
                        color=theme.COLORS["success"] if es_administrador() else theme.COLORS["warning"],
                    ),
                ],
                spacing=4,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=8,
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["success"] if es_administrador() else theme.COLORS["warning"]),
        )

        # Panel lateral completo
        sidebar = ft.Container(
            content=ft.Column(
                controls=[
                    logo,
                    ft.Divider(height=1, color=theme.COLORS["surface_light"]),
                    nav_rail,
                    ft.Container(expand=True),
                    admin_badge,
                    ft.Container(height=20),
                ],
                expand=True,
            ),
            width=120,
            bgcolor=theme.COLORS["surface"],
        )

        # Contenido principal
        self.contenido = ft.Container(
            content=PaginaInicio(),
            expand=True,
            padding=0,
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
            PaginaInicio,
            PaginaTweaks,
            PaginaBloatware,
            PaginaLimpieza,
            PaginaServicios,
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
            solicitar_admin()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Permisos de Administrador"),
            content=ft.Text(
                "Tecnodespegue Optimizer necesita permisos de administrador para aplicar "
                "la mayoría de las optimizaciones.\n\n"
                "¿Deseas reiniciar como administrador?"
            ),
            actions=[
                ft.TextButton("Continuar sin admin", on_click=cerrar_dialogo),
                ft.ElevatedButton(
                    "Reiniciar como Admin",
                    on_click=solicitar_permisos,
                    style=ft.ButtonStyle(bgcolor=theme.COLORS["primary"]),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dialogo)
        dialogo.open = True
        self.page.update()


def main(page: ft.Page):
    """Punto de entrada de la aplicación."""
    TecnodespegueOptimizer(page)


if __name__ == "__main__":
    ft.app(target=main)
