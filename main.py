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
        """Construye la interfaz de usuario estilo CleanMyMac."""
        # Verificar permisos de administrador
        if not es_administrador():
            self._mostrar_advertencia_admin()

        # Definir items de navegación
        nav_items = [
            (ft.Icons.SPEED_ROUNDED, "Escaneo"),
            (ft.Icons.TUNE_ROUNDED, "Tweaks"),
            (ft.Icons.DELETE_SWEEP_ROUNDED, "Bloatware"),
            (ft.Icons.CLEANING_SERVICES_ROUNDED, "Limpieza"),
            (ft.Icons.MISCELLANEOUS_SERVICES_ROUNDED, "Servicios"),
            (ft.Icons.DEVELOPER_BOARD_ROUNDED, "Drivers"),
        ]

        # Crear items de navegación estilo CleanMyMac
        self.nav_items_refs = []
        nav_controls = []

        for i, (icono, label) in enumerate(nav_items):
            item = self._crear_sidebar_item(icono, label, i)
            self.nav_items_refs.append(item)
            nav_controls.append(item)

        # Logo grande estilo CleanMyMac
        logo_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Stack(
                            controls=[
                                # Círculo exterior con glow
                                ft.Container(
                                    width=80,
                                    height=80,
                                    border_radius=40,
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.bottom_right,
                                        colors=theme.COLORS["gradient_purple"],
                                    ),
                                    shadow=ft.BoxShadow(
                                        spread_radius=0,
                                        blur_radius=25,
                                        color=ft.Colors.with_opacity(0.4, theme.COLORS["primary"]),
                                        offset=ft.Offset(0, 5)
                                    ),
                                ),
                                # Icono central
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.ROCKET_LAUNCH_ROUNDED,
                                        size=40,
                                        color=ft.Colors.WHITE,
                                    ),
                                    width=80,
                                    height=80,
                                    alignment=ft.alignment.center,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Tecnodespegue",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                    ),
                    ft.Text(
                        "OPTIMIZER",
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color=theme.COLORS["primary"],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=ft.padding.symmetric(vertical=40, horizontal=20),
        )

        # Separador elegante
        separator = ft.Container(
            content=ft.Container(
                width=50,
                height=2,
                border_radius=1,
                gradient=ft.LinearGradient(
                    colors=[
                        ft.Colors.with_opacity(0, theme.COLORS["primary"]),
                        theme.COLORS["primary"],
                        ft.Colors.with_opacity(0, theme.COLORS["primary"]),
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
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=12),
        )

        # Estado de admin con diseño mejorado
        is_admin = es_administrador()
        admin_status = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SHIELD_ROUNDED if is_admin else ft.Icons.SHIELD_OUTLINED,
                            size=16,
                            color=ft.Colors.WHITE,
                        ),
                        width=32,
                        height=32,
                        border_radius=16,
                        bgcolor=theme.COLORS["success"] if is_admin else theme.COLORS["warning"],
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Administrador" if is_admin else "Usuario",
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=theme.COLORS["text"],
                            ),
                            ft.Text(
                                "Activo" if is_admin else "Limitado",
                                size=10,
                                color=theme.COLORS["text_muted"],
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            margin=ft.margin.symmetric(horizontal=12),
            border_radius=theme.BORDER_RADIUS_SM,
            bgcolor=theme.COLORS["surface_light"],
        )

        # Versión
        version_badge = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=8,
                        height=8,
                        border_radius=4,
                        bgcolor=theme.COLORS["success"],
                    ),
                    ft.Text(
                        "v1.0.0",
                        size=11,
                        color=theme.COLORS["text_muted"],
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(bottom=24, top=12),
        )

        # Sidebar completo estilo CleanMyMac
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
            ),
            width=200,
            bgcolor=theme.COLORS["sidebar"],
            border=ft.border.only(right=ft.BorderSide(1, theme.COLORS["border"])),
        )

        # Contenido principal con gradiente sutil
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

    def _crear_sidebar_item(self, icono, texto: str, index: int) -> ft.Container:
        """Crea un item de sidebar estilo CleanMyMac."""
        is_selected = index == self.pagina_actual
        color = theme.COLORS["primary"] if is_selected else theme.COLORS["text_muted"]

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=22, color=color),
                        padding=10,
                        border_radius=12,
                        bgcolor=ft.Colors.with_opacity(0.15, theme.COLORS["primary"]) if is_selected else None,
                    ),
                    ft.Text(
                        texto,
                        size=14,
                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_400,
                        color=theme.COLORS["text"] if is_selected else theme.COLORS["text_muted"],
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            border_radius=theme.BORDER_RADIUS_SM,
            bgcolor=theme.COLORS["sidebar_active"] if is_selected else None,
            on_click=lambda e, idx=index: self._cambiar_pagina(idx),
            ink=True,
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT),
            data=index,
        )

    def _cambiar_pagina(self, index: int):
        """Cambia la página actual."""
        self.pagina_actual = index

        # Actualizar estilos de navegación
        for i, item in enumerate(self.nav_items_refs):
            is_selected = i == index
            color = theme.COLORS["primary"] if is_selected else theme.COLORS["text_muted"]

            # Actualizar icono
            item.content.controls[0].bgcolor = ft.Colors.with_opacity(0.15, theme.COLORS["primary"]) if is_selected else None
            item.content.controls[0].content.color = color

            # Actualizar texto
            item.content.controls[1].weight = ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_400
            item.content.controls[1].color = theme.COLORS["text"] if is_selected else theme.COLORS["text_muted"]

            # Actualizar fondo
            item.bgcolor = theme.COLORS["sidebar_active"] if is_selected else None

        # Páginas disponibles
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
            self.page.window.close()
            solicitar_admin()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.SHIELD_ROUNDED, color=ft.Colors.WHITE, size=24),
                        padding=10,
                        border_radius=12,
                        bgcolor=theme.COLORS["primary"],
                    ),
                    ft.Text("Permisos Requeridos", size=20, weight=ft.FontWeight.BOLD),
                ],
                spacing=16,
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
                        ft.Container(height=12),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=18, color=theme.COLORS["info"]),
                                    ft.Text(
                                        "Sin privilegios elevados, algunas funciones estarán limitadas.",
                                        size=13,
                                        color=theme.COLORS["info"],
                                    ),
                                ],
                                spacing=10,
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
                            ft.Icon(ft.Icons.SHIELD_ROUNDED, size=18, color=ft.Colors.WHITE),
                            ft.Text("Ejecutar como Admin", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=12,
                    gradient=ft.LinearGradient(
                        colors=theme.COLORS["gradient_blue"],
                    ),
                    on_click=solicitar_permisos,
                    ink=True,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=20),
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
