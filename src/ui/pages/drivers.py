"""Página de gestión de drivers."""
import flet as ft
from src.ui import theme
from src.modules.drivers import (
    escanear_drivers, actualizar_todos_drivers, buscar_actualizaciones_windows,
    EstadoDriver, CategoriaDriver, DriverInfo, ResultadoEscaneo
)
import threading


def crear_pagina_drivers(page: ft.Page = None) -> ft.Column:
    """Página para escanear y actualizar drivers del sistema."""

    resultado_escaneo: ResultadoEscaneo = None
    categoria_actual = [None]  # None = todas

    # UI Elements
    contenedor_drivers = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)
    estado_texto = ft.Text("", size=14, visible=False)
    progreso_bar = ft.ProgressBar(
        value=0,
        color=theme.COLORS["primary"],
        bgcolor=theme.COLORS["surface_light"],
        height=8,
        border_radius=4,
        visible=False
    )

    # Stats cards
    stat_total = ft.Text("--", size=28, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"])
    stat_ok = ft.Text("--", size=28, weight=ft.FontWeight.BOLD, color=theme.COLORS["success"])
    stat_problemas = ft.Text("--", size=28, weight=ft.FontWeight.BOLD, color=theme.COLORS["warning"])
    stat_faltantes = ft.Text("--", size=28, weight=ft.FontWeight.BOLD, color=theme.COLORS["error"])

    btn_escanear = None
    btn_actualizar = None

    def crear_stat_card(titulo: str, valor_widget: ft.Text, icono, color: str) -> ft.Container:
        """Crea una tarjeta de estadística."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(icono, size=20, color=color),
                                padding=10,
                                border_radius=10,
                                bgcolor=ft.Colors.with_opacity(0.15, color),
                            ),
                        ],
                    ),
                    ft.Container(height=8),
                    valor_widget,
                    ft.Text(titulo, size=12, color=theme.COLORS["text_secondary"]),
                ],
                spacing=4,
            ),
            padding=16,
            border_radius=theme.BORDER_RADIUS,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
            width=150,
        )

    def crear_driver_item(driver: DriverInfo) -> ft.Container:
        """Crea un item de driver."""
        # Color según estado
        if driver.estado == EstadoDriver.OK:
            color_estado = theme.COLORS["success"]
            icono_estado = ft.Icons.CHECK_CIRCLE_ROUNDED
        elif driver.estado == EstadoDriver.FALTANTE:
            color_estado = theme.COLORS["error"]
            icono_estado = ft.Icons.ERROR_ROUNDED
        elif driver.estado == EstadoDriver.PROBLEMA:
            color_estado = theme.COLORS["warning"]
            icono_estado = ft.Icons.WARNING_ROUNDED
        else:
            color_estado = theme.COLORS["text_muted"]
            icono_estado = ft.Icons.HELP_ROUNDED

        # Icono de categoría
        iconos_cat = {
            CategoriaDriver.DISPLAY: ft.Icons.MONITOR_ROUNDED,
            CategoriaDriver.NETWORK: ft.Icons.WIFI_ROUNDED,
            CategoriaDriver.AUDIO: ft.Icons.VOLUME_UP_ROUNDED,
            CategoriaDriver.USB: ft.Icons.USB_ROUNDED,
            CategoriaDriver.STORAGE: ft.Icons.STORAGE_ROUNDED,
            CategoriaDriver.BLUETOOTH: ft.Icons.BLUETOOTH_ROUNDED,
            CategoriaDriver.INPUT: ft.Icons.KEYBOARD_ROUNDED,
            CategoriaDriver.PRINTER: ft.Icons.PRINT_ROUNDED,
            CategoriaDriver.SYSTEM: ft.Icons.SETTINGS_ROUNDED,
            CategoriaDriver.OTHER: ft.Icons.DEVICES_OTHER_ROUNDED,
        }

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            iconos_cat.get(driver.categoria, ft.Icons.DEVICES_OTHER_ROUNDED),
                            size=22,
                            color=theme.COLORS["primary"]
                        ),
                        padding=10,
                        border_radius=10,
                        bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                driver.nombre[:50] + "..." if len(driver.nombre) > 50 else driver.nombre,
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=theme.COLORS["text"]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(driver.fabricante, size=12, color=theme.COLORS["text_muted"]),
                                    ft.Text("•", size=12, color=theme.COLORS["text_muted"]),
                                    ft.Text(f"v{driver.version}", size=12, color=theme.COLORS["text_secondary"]),
                                    ft.Text("•", size=12, color=theme.COLORS["text_muted"]),
                                    ft.Text(driver.fecha, size=12, color=theme.COLORS["text_muted"]),
                                ],
                                spacing=6,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(icono_estado, size=16, color=color_estado),
                                ft.Text(driver.estado.value, size=12, color=color_estado),
                            ],
                            spacing=4,
                        ),
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=20,
                        bgcolor=ft.Colors.with_opacity(0.1, color_estado),
                    ),
                ],
                spacing=16,
            ),
            padding=16,
            border_radius=theme.BORDER_RADIUS_SM,
            bgcolor=theme.COLORS["surface_light"],
            border=ft.border.all(1, theme.COLORS["border"]),
        )

    def actualizar_lista_drivers():
        """Actualiza la lista de drivers mostrados."""
        contenedor_drivers.controls.clear()

        if not resultado_escaneo or not resultado_escaneo.drivers:
            contenedor_drivers.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.SEARCH_ROUNDED, size=48, color=theme.COLORS["text_muted"]),
                            ft.Text(
                                "Haz clic en 'Escanear Drivers' para comenzar",
                                size=14,
                                color=theme.COLORS["text_secondary"]
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
            return

        drivers = resultado_escaneo.drivers

        # Filtrar por categoría si es necesario
        if categoria_actual[0]:
            drivers = [d for d in drivers if d.categoria == categoria_actual[0]]

        # Ordenar: primero los que tienen problemas
        drivers_ordenados = sorted(drivers, key=lambda d: (
            0 if d.estado == EstadoDriver.FALTANTE else
            1 if d.estado == EstadoDriver.PROBLEMA else
            2 if d.estado == EstadoDriver.DESACTUALIZADO else 3
        ))

        for driver in drivers_ordenados:
            contenedor_drivers.controls.append(crear_driver_item(driver))

    def escanear_click(e):
        """Inicia el escaneo de drivers."""
        nonlocal resultado_escaneo

        progreso_bar.visible = True
        progreso_bar.value = 0
        estado_texto.visible = True
        estado_texto.value = "Iniciando escaneo..."
        estado_texto.color = theme.COLORS["text_secondary"]
        btn_escanear.disabled = True
        if page:
            page.update()

        def callback(mensaje: str, porcentaje: int):
            progreso_bar.value = porcentaje / 100
            estado_texto.value = mensaje
            if page:
                page.update()

        def ejecutar():
            nonlocal resultado_escaneo
            try:
                resultado_escaneo = escanear_drivers(callback)

                # Actualizar stats
                stat_total.value = str(resultado_escaneo.total)
                stat_ok.value = str(resultado_escaneo.actualizados)
                stat_problemas.value = str(resultado_escaneo.con_problemas)
                stat_faltantes.value = str(resultado_escaneo.faltantes)

                estado_texto.value = f"Escaneo completado: {resultado_escaneo.total} drivers encontrados"
                estado_texto.color = theme.COLORS["success"]

                actualizar_lista_drivers()

            except Exception as ex:
                estado_texto.value = f"Error: {str(ex)}"
                estado_texto.color = theme.COLORS["error"]

            progreso_bar.visible = False
            btn_escanear.disabled = False
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    def actualizar_click(e):
        """Actualiza todos los drivers."""
        progreso_bar.visible = True
        progreso_bar.value = None  # Indeterminado
        estado_texto.visible = True
        estado_texto.value = "Buscando actualizaciones..."
        estado_texto.color = theme.COLORS["text_secondary"]
        btn_actualizar.disabled = True
        btn_escanear.disabled = True
        if page:
            page.update()

        def callback(mensaje: str, porcentaje: int):
            estado_texto.value = mensaje
            if porcentaje > 0:
                progreso_bar.value = porcentaje / 100
            if page:
                page.update()

        def ejecutar():
            try:
                exitosos, fallidos, mensaje = actualizar_todos_drivers(callback)
                estado_texto.value = mensaje
                estado_texto.color = theme.COLORS["success"] if exitosos > 0 else theme.COLORS["info"]
            except Exception as ex:
                estado_texto.value = f"Error: {str(ex)}"
                estado_texto.color = theme.COLORS["error"]

            progreso_bar.visible = False
            btn_actualizar.disabled = False
            btn_escanear.disabled = False
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    def cambiar_categoria(cat):
        """Cambia el filtro de categoría."""
        categoria_actual[0] = cat
        actualizar_lista_drivers()
        if page:
            page.update()

    # Botones principales
    btn_escanear = ft.ElevatedButton(
        text="Escanear Drivers",
        icon=ft.Icons.SEARCH_ROUNDED,
        on_click=escanear_click,
        style=ft.ButtonStyle(
            bgcolor=theme.COLORS["primary"],
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
        ),
    )

    btn_actualizar = ft.ElevatedButton(
        text="Actualizar Todo",
        icon=ft.Icons.SYSTEM_UPDATE_ROUNDED,
        on_click=actualizar_click,
        style=ft.ButtonStyle(
            bgcolor=theme.COLORS["secondary"],
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
        ),
    )

    # Filtros de categoría
    filtros = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text("Todas", size=12, color=theme.COLORS["text"]),
                padding=ft.padding.symmetric(horizontal=14, vertical=8),
                border_radius=20,
                bgcolor=theme.COLORS["primary"] if not categoria_actual[0] else theme.COLORS["surface_light"],
                on_click=lambda e: cambiar_categoria(None),
                ink=True,
            ),
        ] + [
            ft.Container(
                content=ft.Text(cat.value, size=12, color=theme.COLORS["text_secondary"]),
                padding=ft.padding.symmetric(horizontal=14, vertical=8),
                border_radius=20,
                bgcolor=theme.COLORS["surface_light"],
                on_click=lambda e, c=cat: cambiar_categoria(c),
                ink=True,
            )
            for cat in [CategoriaDriver.DISPLAY, CategoriaDriver.NETWORK, CategoriaDriver.AUDIO, CategoriaDriver.STORAGE]
        ],
        wrap=True,
        spacing=8,
    )

    # Layout principal
    return ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.MEMORY_ROUNDED, size=48, color=theme.COLORS["primary"]),
                            padding=14,
                            border_radius=16,
                            bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Gestión de Drivers", size=28, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
                                ft.Text(
                                    "Escanea, detecta y actualiza los drivers de tu sistema",
                                    size=14,
                                    color=theme.COLORS["text_secondary"]
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=20,
                ),
                padding=ft.padding.symmetric(horizontal=24, vertical=20),
            ),

            # Stats
            ft.Container(
                content=ft.Row(
                    controls=[
                        crear_stat_card("Total Drivers", stat_total, ft.Icons.DEVELOPER_BOARD_ROUNDED, theme.COLORS["primary"]),
                        crear_stat_card("Actualizados", stat_ok, ft.Icons.CHECK_CIRCLE_ROUNDED, theme.COLORS["success"]),
                        crear_stat_card("Con Problemas", stat_problemas, ft.Icons.WARNING_ROUNDED, theme.COLORS["warning"]),
                        crear_stat_card("Faltantes", stat_faltantes, ft.Icons.ERROR_ROUNDED, theme.COLORS["error"]),
                    ],
                    spacing=16,
                    wrap=True,
                ),
                padding=ft.padding.symmetric(horizontal=24),
            ),

            ft.Container(height=16),

            # Botones de acción
            ft.Container(
                content=ft.Row(
                    controls=[btn_escanear, btn_actualizar],
                    spacing=12,
                ),
                padding=ft.padding.symmetric(horizontal=24),
            ),

            ft.Container(height=8),

            # Progreso y estado
            ft.Container(
                content=ft.Column(controls=[progreso_bar, estado_texto], spacing=8),
                padding=ft.padding.symmetric(horizontal=24),
            ),

            ft.Container(height=16),

            # Filtros
            ft.Container(content=filtros, padding=ft.padding.symmetric(horizontal=24)),

            ft.Container(height=12),

            # Lista de drivers
            ft.Container(
                content=contenedor_drivers,
                padding=ft.padding.symmetric(horizontal=24),
                expand=True,
            ),

            ft.Container(height=24),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


class PaginaDrivers:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_drivers(page)
