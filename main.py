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
        self.nav_buttons = []

        self._configurar_pagina()
        self._construir_ui()

    def _configurar_pagina(self):
        """Configura la página principal."""
        self.page.title = "Tecnodespegue Optimizer - Windows 11 25H2"
        self.page.bgcolor = theme.COLORS["background"]
        self.page.padding = 0
        self.page.window.width = 1280
        self.page.window.height = 850
        self.page.window.min_width = 1000
        self.page.window.min_height = 650
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.center()

        # Tema personalizado
        self.page.theme = ft.Theme(
            color_scheme_seed=theme.COLORS["primary"],
            font_family="Segoe UI",
        )

    def _crear_nav_button(self, icono, label, index):
        """Crea un botón de navegación personalizado."""
        is_selected = index == self.pagina_actual

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            icono,
                            size=24,
                            color=theme.COLORS["primary"] if is_selected else theme.COLORS["text_muted"],
                        ),
                        padding=12,
                        border_radius=14,
                        bgcolor=ft.Colors.with_opacity(0.15, theme.COLORS["primary"]) if is_selected else None,
                    ),
                    ft.Text(
                        label,
                        size=11,
                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_400,
                        color=theme.COLORS["text"] if is_selected else theme.COLORS["text_muted"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=4),
            border_radius=16,
            on_click=lambda e, idx=index: self._cambiar_pagina_custom(idx),
            ink=True,
            data=index,
        )

    def _construir_ui(self):
        """Construye la interfaz de usuario."""
        # Verificar permisos de administrador
        if not es_administrador():
            self._mostrar_advertencia_admin()

        # Navegación lateral personalizada
        nav_items = [
            (ft.Icons.DASHBOARD_ROUNDED, "Inicio"),
            (ft.Icons.TUNE_ROUNDED, "Tweaks"),
            (ft.Icons.DELETE_SWEEP_ROUNDED, "Bloatware"),
            (ft.Icons.CLEANING_SERVICES_ROUNDED, "Limpieza"),
            (ft.Icons.MISCELLANEOUS_SERVICES_ROUNDED, "Servicios"),
            (ft.Icons.MEMORY_ROUNDED, "Drivers"),
        ]

        self.nav_buttons = [
            self._crear_nav_button(icono, label, i)
            for i, (icono, label) in enumerate(nav_items)
        ]

        nav_column = ft.Column(
            controls=self.nav_buttons,
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Logo profesional premium
        logo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Stack(
                            controls=[
                                ft.Container(
                                    width=60,
                                    height=60,
                                    border_radius=20,
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.bottom_right,
                                        colors=[theme.COLORS["primary"], theme.COLORS["secondary"]],
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.Icons.ROCKET_LAUNCH_ROUNDED, size=32, color=ft.Colors.WHITE),
                                    width=60,
                                    height=60,
                                    alignment=ft.alignment.center,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "Tecnodespegue",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "OPTIMIZER",
                        size=9,
                        weight=ft.FontWeight.W_600,
                        color=theme.COLORS["primary"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            padding=ft.padding.symmetric(vertical=28, horizontal=10),
            alignment=ft.alignment.center,
        )

        # Estado de admin premium
        is_admin = es_administrador()
        admin_badge = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.VERIFIED_USER_ROUNDED if is_admin else ft.Icons.SHIELD_OUTLINED,
                            size=18,
                            color=ft.Colors.WHITE,
                        ),
                        padding=8,
                        border_radius=10,
                        bgcolor=theme.COLORS["success"] if is_admin else theme.COLORS["warning"],
                    ),
                    ft.Text(
                        "Admin" if is_admin else "Usuario",
                        size=10,
                        weight=ft.FontWeight.W_500,
                        color=theme.COLORS["text_secondary"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            padding=ft.padding.symmetric(vertical=12, horizontal=16),
            margin=ft.margin.symmetric(horizontal=8),
        )

        # Versión
        version_text = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=6,
                        height=6,
                        border_radius=3,
                        bgcolor=theme.COLORS["success"],
                    ),
                    ft.Text(
                        "v1.0.0",
                        size=10,
                        color=theme.COLORS["text_muted"],
                    ),
                ],
                spacing=6,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(bottom=20),
        )

        # Panel lateral premium
        sidebar = ft.Container(
            content=ft.Column(
                controls=[
                    logo,
                    ft.Container(
                        content=ft.Container(
                            width=40,
                            height=2,
                            border_radius=1,
                            bgcolor=theme.COLORS["border"],
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=16),
                    ft.Container(
                        content=nav_column,
                        padding=ft.padding.symmetric(horizontal=8),
                    ),
                    ft.Container(expand=True),
                    admin_badge,
                    version_text,
                ],
                spacing=0,
            ),
            width=140,
            bgcolor=theme.COLORS["surface"],
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

    def _cambiar_pagina_custom(self, index):
        """Cambia la página actual con navegación personalizada."""
        self.pagina_actual = index

        # Actualizar botones de navegación
        for i, btn in enumerate(self.nav_buttons):
            is_selected = i == index
            btn.content.controls[0].bgcolor = ft.Colors.with_opacity(0.15, theme.COLORS["primary"]) if is_selected else None
            btn.content.controls[0].content.color = theme.COLORS["primary"] if is_selected else theme.COLORS["text_muted"]
            btn.content.controls[1].weight = ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_400
            btn.content.controls[1].color = theme.COLORS["text"] if is_selected else theme.COLORS["text_muted"]

        paginas = [
            lambda: PaginaInicio(self.page),
            lambda: PaginaTweaks(self.page),
            lambda: PaginaBloatware(self.page),
            lambda: PaginaLimpieza(self.page),
            lambda: PaginaServicios(self.page),
            lambda: PaginaDrivers(self.page),
        ]

        self.contenido.content = paginas[index]()
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
