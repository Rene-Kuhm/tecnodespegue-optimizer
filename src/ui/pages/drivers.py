"""Página de gestión de drivers - Estilo CleanMyMac."""
import flet as ft
from src.ui import theme
from src.modules.drivers import (
    escanear_drivers, actualizar_todos_drivers, buscar_actualizaciones_windows,
    verificar_estado_drivers, EstadoDriver, CategoriaDriver, DriverInfo, ResultadoEscaneo
)
import threading


def crear_pagina_drivers(page: ft.Page = None) -> ft.Column:
    """Página para escanear y actualizar drivers del sistema con estilo CleanMyMac."""

    resultado_escaneo: ResultadoEscaneo = None
    categoria_actual = [None]  # None = todas

    # UI Elements
    contenedor_drivers = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    estado_texto = ft.Text("", size=14, visible=False)
    progreso_bar = ft.ProgressBar(
        value=0,
        color=theme.COLORS["primary"],
        bgcolor=theme.COLORS["surface_elevated"],
        height=8,
        border_radius=4,
        visible=False
    )

    # Banner de estado "¡Perfecto!"
    banner_perfecto = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=32, color=ft.Colors.WHITE),
                    padding=12,
                    border_radius=16,
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "¡Todo Perfecto!",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Text(
                            "Todos los drivers están instalados y actualizados",
                            size=13,
                            color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.Icon(ft.Icons.VERIFIED_ROUNDED, size=40, color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE)),
            ],
            spacing=16,
        ),
        padding=24,
        border_radius=theme.BORDER_RADIUS,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=theme.COLORS["gradient_green"],
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=25,
            color=ft.Colors.with_opacity(0.4, theme.COLORS["success"]),
            offset=ft.Offset(0, 10),
        ),
        visible=False,
    )

    # Stats cards
    stat_total = ft.Text("--", size=32, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"])
    stat_ok = ft.Text("--", size=32, weight=ft.FontWeight.BOLD, color=theme.COLORS["success"])
    stat_problemas = ft.Text("--", size=32, weight=ft.FontWeight.BOLD, color=theme.COLORS["warning"])
    stat_faltantes = ft.Text("--", size=32, weight=ft.FontWeight.BOLD, color=theme.COLORS["error"])

    btn_escanear = None
    btn_actualizar = None

    def crear_stat_card(titulo: str, valor_widget: ft.Text, icono, color: str, gradiente: list) -> ft.Container:
        """Crea una tarjeta de estadística con estilo CleanMyMac."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=24, color=ft.Colors.WHITE),
                        padding=14,
                        border_radius=16,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=gradiente,
                        ),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=12,
                            color=ft.Colors.with_opacity(0.25, color),
                            offset=ft.Offset(0, 4),
                        ),
                    ),
                    ft.Container(height=12),
                    valor_widget,
                    ft.Text(titulo, size=12, color=theme.COLORS["text_muted"]),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=24,
            border_radius=theme.BORDER_RADIUS,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
            width=160,
        )

    def crear_driver_item(driver: DriverInfo) -> ft.Container:
        """Crea un item de driver con estilo CleanMyMac."""
        # Color según estado
        if driver.estado == EstadoDriver.OK:
            color_estado = theme.COLORS["success"]
            icono_estado = ft.Icons.CHECK_CIRCLE_ROUNDED
            texto_estado = "OK"
        elif driver.estado == EstadoDriver.FALTANTE:
            color_estado = theme.COLORS["error"]
            icono_estado = ft.Icons.ERROR_ROUNDED
            texto_estado = "Faltante"
        elif driver.estado == EstadoDriver.PROBLEMA:
            color_estado = theme.COLORS["warning"]
            icono_estado = ft.Icons.WARNING_ROUNDED
            texto_estado = "Problema"
        else:
            color_estado = theme.COLORS["text_muted"]
            icono_estado = ft.Icons.HELP_ROUNDED
            texto_estado = "Desconocido"

        # Icono de categoría
        iconos_cat = {
            CategoriaDriver.DISPLAY: (ft.Icons.MONITOR_ROUNDED, theme.COLORS["accent_purple"]),
            CategoriaDriver.NETWORK: (ft.Icons.WIFI_ROUNDED, theme.COLORS["accent_blue"]),
            CategoriaDriver.AUDIO: (ft.Icons.VOLUME_UP_ROUNDED, theme.COLORS["accent_orange"]),
            CategoriaDriver.USB: (ft.Icons.USB_ROUNDED, theme.COLORS["primary"]),
            CategoriaDriver.STORAGE: (ft.Icons.STORAGE_ROUNDED, theme.COLORS["success"]),
            CategoriaDriver.BLUETOOTH: (ft.Icons.BLUETOOTH_ROUNDED, theme.COLORS["info"]),
            CategoriaDriver.INPUT: (ft.Icons.KEYBOARD_ROUNDED, theme.COLORS["accent_pink"]),
            CategoriaDriver.PRINTER: (ft.Icons.PRINT_ROUNDED, theme.COLORS["warning"]),
            CategoriaDriver.SYSTEM: (ft.Icons.SETTINGS_ROUNDED, theme.COLORS["text_secondary"]),
            CategoriaDriver.OTHER: (ft.Icons.DEVICES_OTHER_ROUNDED, theme.COLORS["text_muted"]),
        }

        icono_cat, color_cat = iconos_cat.get(driver.categoria, (ft.Icons.DEVICES_OTHER_ROUNDED, theme.COLORS["primary"]))

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono_cat, size=22, color=color_cat),
                        padding=12,
                        border_radius=14,
                        bgcolor=ft.Colors.with_opacity(0.1, color_cat),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                (driver.nombre or "Dispositivo desconocido")[:50] + ("..." if driver.nombre and len(driver.nombre) > 50 else ""),
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=theme.COLORS["text"]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(driver.fabricante or "Desconocido", size=12, color=theme.COLORS["text_secondary"]),
                                    ft.Container(
                                        width=4,
                                        height=4,
                                        border_radius=2,
                                        bgcolor=theme.COLORS["text_muted"],
                                    ),
                                    ft.Text(f"v{driver.version or 'N/A'}", size=12, color=theme.COLORS["text_muted"]),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(icono_estado, size=16, color=ft.Colors.WHITE),
                                ft.Text(texto_estado, size=11, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                            ],
                            spacing=6,
                        ),
                        padding=ft.padding.symmetric(horizontal=14, vertical=8),
                        border_radius=16,
                        bgcolor=color_estado,
                    ),
                ],
                spacing=16,
            ),
            padding=18,
            border_radius=theme.BORDER_RADIUS,
            bgcolor=theme.COLORS["surface"],
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
                            ft.Container(
                                content=ft.Icon(ft.Icons.SEARCH_ROUNDED, size=48, color=theme.COLORS["primary"]),
                                padding=20,
                                border_radius=30,
                                bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                            ),
                            ft.Container(height=16),
                            ft.Text(
                                "Escanea tus drivers",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=theme.COLORS["text"],
                            ),
                            ft.Text(
                                "Haz clic en 'Escanear Drivers' para comenzar",
                                size=14,
                                color=theme.COLORS["text_secondary"],
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=60,
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
        estado_texto.value = "Iniciando escaneo de drivers..."
        estado_texto.color = theme.COLORS["info"]
        banner_perfecto.visible = False
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

                # Mostrar banner si todo está perfecto
                if resultado_escaneo.todos_ok:
                    banner_perfecto.visible = True
                    estado_texto.value = "¡Todos los drivers están perfectos!"
                    estado_texto.color = theme.COLORS["success"]
                else:
                    banner_perfecto.visible = False
                    problemas_total = resultado_escaneo.faltantes + resultado_escaneo.con_problemas
                    estado_texto.value = f"Escaneo completado: {problemas_total} drivers necesitan atención"
                    estado_texto.color = theme.COLORS["warning"] if problemas_total > 0 else theme.COLORS["success"]

                actualizar_lista_drivers()

            except Exception as ex:
                estado_texto.value = f"Error: {str(ex)}"
                estado_texto.color = theme.COLORS["error"]
                banner_perfecto.visible = False

            progreso_bar.visible = False
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    def actualizar_driver_en_lista(device_id: str, exito: bool):
        """Actualiza el estado de un driver específico en la lista sin re-escanear."""
        nonlocal resultado_escaneo

        if not resultado_escaneo:
            return

        # Buscar el driver en la lista y actualizar su estado
        for driver in resultado_escaneo.drivers:
            if driver.device_id == device_id:
                if exito:
                    driver.estado = EstadoDriver.OK
                    driver.necesita_actualizacion = False
                    # Actualizar contadores
                    resultado_escaneo.faltantes = max(0, resultado_escaneo.faltantes - 1)
                    resultado_escaneo.con_problemas = max(0, resultado_escaneo.con_problemas - 1)
                    resultado_escaneo.actualizados += 1
                break

        # Verificar si todos están OK
        resultado_escaneo.todos_ok = (
            resultado_escaneo.faltantes == 0 and
            resultado_escaneo.con_problemas == 0
        )

        # Actualizar stats en UI
        stat_ok.value = str(resultado_escaneo.actualizados)
        stat_problemas.value = str(resultado_escaneo.con_problemas)
        stat_faltantes.value = str(resultado_escaneo.faltantes)

        # Actualizar la lista visual
        actualizar_lista_drivers()

        if page:
            page.update()

    def actualizar_click(e):
        """Actualiza todos los drivers."""
        nonlocal resultado_escaneo

        progreso_bar.visible = True
        progreso_bar.value = None
        estado_texto.visible = True
        estado_texto.value = "Buscando actualizaciones de drivers..."
        estado_texto.color = theme.COLORS["info"]
        banner_perfecto.visible = False
        if page:
            page.update()

        def callback(mensaje: str, porcentaje: int):
            estado_texto.value = mensaje
            if porcentaje > 0:
                progreso_bar.value = porcentaje / 100
            if page:
                page.update()

        def on_driver_installed(device_id: str, exito: bool):
            """Callback cuando un driver se instala - actualiza UI inmediatamente."""
            actualizar_driver_en_lista(device_id, exito)

        def ejecutar():
            nonlocal resultado_escaneo

            try:
                exitosos, fallidos, mensaje = actualizar_todos_drivers(callback, on_driver_installed)

                # Actualizar stats finales
                if resultado_escaneo:
                    stat_total.value = str(resultado_escaneo.total)
                    stat_ok.value = str(resultado_escaneo.actualizados)
                    stat_problemas.value = str(resultado_escaneo.con_problemas)
                    stat_faltantes.value = str(resultado_escaneo.faltantes)

                # Mostrar resultado final
                if resultado_escaneo and resultado_escaneo.todos_ok:
                    banner_perfecto.visible = True
                    estado_texto.value = "¡Perfecto! Todos los drivers están actualizados."
                    estado_texto.color = theme.COLORS["success"]
                elif fallidos == 0 and exitosos > 0:
                    banner_perfecto.visible = True
                    estado_texto.value = f"¡Perfecto! Se instalaron {exitosos} drivers correctamente."
                    estado_texto.color = theme.COLORS["success"]
                elif exitosos > 0:
                    banner_perfecto.visible = False
                    estado_texto.value = f"Se instalaron {exitosos} drivers. {fallidos} requieren atención manual."
                    estado_texto.color = theme.COLORS["warning"]
                else:
                    banner_perfecto.visible = False
                    estado_texto.value = mensaje
                    estado_texto.color = theme.COLORS["info"] if "Perfecto" in mensaje else theme.COLORS["warning"]

                    # Si el mensaje dice perfecto, mostrar banner
                    if "Perfecto" in mensaje or "perfecto" in mensaje:
                        banner_perfecto.visible = True
                        estado_texto.color = theme.COLORS["success"]

                actualizar_lista_drivers()

            except Exception as ex:
                estado_texto.value = f"Error: {str(ex)}"
                estado_texto.color = theme.COLORS["error"]
                banner_perfecto.visible = False

            progreso_bar.visible = False
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    def cambiar_categoria(cat):
        """Cambia el filtro de categoría."""
        categoria_actual[0] = cat
        actualizar_lista_drivers()
        if page:
            page.update()

    # Botones principales con gradiente
    btn_escanear = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.SEARCH_ROUNDED, size=20, color=ft.Colors.WHITE),
                ft.Text("Escanear Drivers", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ],
            spacing=10,
        ),
        padding=ft.padding.symmetric(horizontal=28, vertical=14),
        border_radius=theme.BORDER_RADIUS_SM,
        gradient=ft.LinearGradient(
            colors=theme.COLORS["gradient_blue"],
        ),
        on_click=escanear_click,
        ink=True,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, theme.COLORS["primary"]),
            offset=ft.Offset(0, 5),
        ),
    )

    btn_actualizar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.SYSTEM_UPDATE_ROUNDED, size=20, color=ft.Colors.WHITE),
                ft.Text("Actualizar Todo", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ],
            spacing=10,
        ),
        padding=ft.padding.symmetric(horizontal=28, vertical=14),
        border_radius=theme.BORDER_RADIUS_SM,
        gradient=ft.LinearGradient(
            colors=theme.COLORS["gradient_green"],
        ),
        on_click=actualizar_click,
        ink=True,
    )

    # Filtros de categoría
    filtros = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text("Todas", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE if not categoria_actual[0] else theme.COLORS["text_muted"]),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                border_radius=20,
                bgcolor=theme.COLORS["primary"] if not categoria_actual[0] else theme.COLORS["surface_light"],
                on_click=lambda e: cambiar_categoria(None),
                ink=True,
            ),
        ] + [
            ft.Container(
                content=ft.Text(cat.value, size=12, weight=ft.FontWeight.W_500, color=theme.COLORS["text_muted"]),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                border_radius=20,
                bgcolor=theme.COLORS["surface_light"],
                on_click=lambda e, c=cat: cambiar_categoria(c),
                ink=True,
            )
            for cat in [CategoriaDriver.DISPLAY, CategoriaDriver.NETWORK, CategoriaDriver.AUDIO, CategoriaDriver.STORAGE]
        ],
        wrap=True,
        spacing=10,
    )

    # Inicializar lista vacía
    actualizar_lista_drivers()

    # Layout principal
    return ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.DEVELOPER_BOARD_ROUNDED, size=40, color=ft.Colors.WHITE),
                            padding=16,
                            border_radius=20,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=theme.COLORS["gradient_purple"],
                            ),
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=20,
                                color=ft.Colors.with_opacity(0.3, theme.COLORS["accent_purple"]),
                                offset=ft.Offset(0, 8),
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Gestión de Drivers",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.COLORS["text"],
                                ),
                                ft.Text(
                                    "Escanea, detecta y actualiza los drivers de tu sistema",
                                    size=14,
                                    color=theme.COLORS["text_secondary"],
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=20,
                ),
                padding=ft.padding.symmetric(horizontal=30, vertical=24),
            ),

            # Stats
            ft.Container(
                content=ft.Row(
                    controls=[
                        crear_stat_card("Total", stat_total, ft.Icons.DEVELOPER_BOARD_ROUNDED, theme.COLORS["primary"], theme.COLORS["gradient_blue"]),
                        crear_stat_card("Actualizados", stat_ok, ft.Icons.CHECK_CIRCLE_ROUNDED, theme.COLORS["success"], theme.COLORS["gradient_green"]),
                        crear_stat_card("Problemas", stat_problemas, ft.Icons.WARNING_ROUNDED, theme.COLORS["warning"], theme.COLORS["gradient_orange"]),
                        crear_stat_card("Faltantes", stat_faltantes, ft.Icons.ERROR_ROUNDED, theme.COLORS["error"], ["#f5576c", "#f093fb"]),
                    ],
                    spacing=16,
                    wrap=True,
                ),
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=20),

            # Banner de "¡Todo Perfecto!"
            ft.Container(
                content=banner_perfecto,
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=16),

            # Botones de acción
            ft.Container(
                content=ft.Row(
                    controls=[btn_escanear, btn_actualizar],
                    spacing=16,
                ),
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=12),

            # Progreso y estado
            ft.Container(
                content=ft.Column(controls=[progreso_bar, estado_texto], spacing=8),
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=16),

            # Filtros
            ft.Container(content=filtros, padding=ft.padding.symmetric(horizontal=30)),

            ft.Container(height=16),

            # Lista de drivers
            ft.Container(
                content=contenedor_drivers,
                padding=ft.padding.symmetric(horizontal=30),
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
