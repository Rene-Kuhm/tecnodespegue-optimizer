"""Página de gestión de servicios de Windows - Estilo CleanMyMac."""
import flet as ft
from src.ui import theme
from src.modules.servicios import (
    obtener_servicios_deshabilitables, deshabilitar_servicio, habilitar_servicio,
    EstadoServicio, TipoInicio,
    deshabilitar_servicios_telemetria, deshabilitar_servicios_xbox, deshabilitar_servicios_hyperv
)
import threading


def crear_pagina_servicios(page: ft.Page = None) -> ft.Column:
    """Página para gestionar servicios de Windows con estilo CleanMyMac."""

    servicios_lista = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    estado_texto = ft.Text("", size=14, visible=False)

    def cargar_servicios():
        servicios_lista.controls.clear()
        servicios_lista.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ProgressRing(width=40, height=40, stroke_width=3, color=theme.COLORS["primary"]),
                        ft.Text("Cargando servicios del sistema...", size=14, color=theme.COLORS["text_secondary"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        )
        if page:
            page.update()

        def cargar():
            servicios = obtener_servicios_deshabilitables()
            servicios_lista.controls.clear()

            for servicio in servicios:
                esta_deshabilitado = servicio.tipo_inicio == TipoInicio.DESHABILITADO
                esta_ejecutando = servicio.estado == EstadoServicio.EJECUTANDO

                if esta_deshabilitado:
                    color_estado = theme.COLORS["warning"]
                    texto_estado = "Deshabilitado"
                    icono_estado = ft.Icons.PAUSE_CIRCLE_ROUNDED
                elif esta_ejecutando:
                    color_estado = theme.COLORS["success"]
                    texto_estado = "Ejecutando"
                    icono_estado = ft.Icons.PLAY_CIRCLE_ROUNDED
                else:
                    color_estado = theme.COLORS["text_muted"]
                    texto_estado = "Detenido"
                    icono_estado = ft.Icons.STOP_CIRCLE_ROUNDED

                item = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(ft.Icons.MISCELLANEOUS_SERVICES_ROUNDED, size=20, color=theme.COLORS["primary"]),
                                padding=10,
                                border_radius=12,
                                bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text(
                                                servicio.nombre,
                                                size=14,
                                                weight=ft.FontWeight.W_600,
                                                color=theme.COLORS["text"]
                                            ),
                                            ft.Container(
                                                content=ft.Row(
                                                    controls=[
                                                        ft.Icon(icono_estado, size=14, color=ft.Colors.WHITE),
                                                        ft.Text(texto_estado, size=10, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                                                    ],
                                                    spacing=4,
                                                ),
                                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                                border_radius=12,
                                                bgcolor=color_estado,
                                            ),
                                        ],
                                        spacing=10,
                                    ),
                                    ft.Text(
                                        servicio.descripcion or servicio.nombre_display,
                                        size=12,
                                        color=theme.COLORS["text_muted"],
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Icon(
                                            ft.Icons.STOP_ROUNDED,
                                            size=18,
                                            color=theme.COLORS["error"] if not esta_deshabilitado else theme.COLORS["text_muted"]
                                        ),
                                        padding=8,
                                        border_radius=8,
                                        bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["error"]) if not esta_deshabilitado else None,
                                        on_click=lambda e, s=servicio: accion_servicio(s, False) if not esta_deshabilitado else None,
                                        ink=True if not esta_deshabilitado else False,
                                    ),
                                    ft.Container(
                                        content=ft.Icon(
                                            ft.Icons.PLAY_ARROW_ROUNDED,
                                            size=18,
                                            color=theme.COLORS["success"] if esta_deshabilitado else theme.COLORS["text_muted"]
                                        ),
                                        padding=8,
                                        border_radius=8,
                                        bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["success"]) if esta_deshabilitado else None,
                                        on_click=lambda e, s=servicio: accion_servicio(s, True) if esta_deshabilitado else None,
                                        ink=True if esta_deshabilitado else False,
                                    ),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=14,
                    ),
                    padding=18,
                    border_radius=theme.BORDER_RADIUS,
                    bgcolor=theme.COLORS["surface"],
                    border=ft.border.all(1, theme.COLORS["border"]),
                )
                servicios_lista.controls.append(item)

            if not servicios:
                servicios_lista.controls.append(
                    ft.Container(
                        content=ft.Text("No se encontraron servicios deshabilitables", color=theme.COLORS["text_secondary"]),
                        padding=20,
                    )
                )
            if page:
                page.update()

        threading.Thread(target=cargar).start()

    def accion_servicio(servicio, habilitar: bool):
        estado_texto.visible = True
        estado_texto.value = f"{'Habilitando' if habilitar else 'Deshabilitando'} {servicio.nombre}..."
        estado_texto.color = theme.COLORS["info"]
        if page:
            page.update()

        def ejecutar():
            if habilitar:
                exito, _ = habilitar_servicio(servicio.nombre)
            else:
                exito, _ = deshabilitar_servicio(servicio.nombre)
            estado_texto.value = f"{servicio.nombre} {'habilitado' if habilitar else 'deshabilitado'}" if exito else "Error en la operación"
            estado_texto.color = theme.COLORS["success"] if exito else theme.COLORS["error"]
            cargar_servicios()

        threading.Thread(target=ejecutar).start()

    def accion_rapida(funcion, nombre: str):
        estado_texto.visible = True
        estado_texto.value = f"Deshabilitando servicios de {nombre}..."
        estado_texto.color = theme.COLORS["info"]
        if page:
            page.update()

        def ejecutar():
            exitosos, _ = funcion()
            estado_texto.value = f"{nombre}: {exitosos} servicios deshabilitados"
            estado_texto.color = theme.COLORS["success"]
            cargar_servicios()

        threading.Thread(target=ejecutar).start()

    # Acciones rápidas con estilo CleanMyMac
    acciones_rapidas = [
        ("Telemetría", ft.Icons.VISIBILITY_OFF_ROUNDED, deshabilitar_servicios_telemetria, theme.COLORS["warning"], "Privacidad"),
        ("Xbox", ft.Icons.SPORTS_ESPORTS_ROUNDED, deshabilitar_servicios_xbox, theme.COLORS["success"], "Gaming"),
        ("Hyper-V", ft.Icons.COMPUTER_ROUNDED, deshabilitar_servicios_hyperv, theme.COLORS["info"], "Virtualización"),
    ]

    acciones_widgets = []
    for nombre, icono, funcion, color, categoria in acciones_rapidas:
        widget = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=28, color=ft.Colors.WHITE),
                        padding=16,
                        border_radius=16,
                        bgcolor=color,
                    ),
                    ft.Container(height=8),
                    ft.Text(nombre, size=14, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
                    ft.Text(categoria, size=11, color=theme.COLORS["text_muted"]),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=20,
            border_radius=theme.BORDER_RADIUS,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
            on_click=lambda e, f=funcion, n=nombre: accion_rapida(f, n),
            ink=True,
            width=140,
        )
        acciones_widgets.append(widget)

    cargar_servicios()

    return ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.MISCELLANEOUS_SERVICES_ROUNDED, size=40, color=ft.Colors.WHITE),
                            padding=16,
                            border_radius=20,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=theme.COLORS["gradient_cyan"],
                            ),
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=20,
                                color=ft.Colors.with_opacity(0.3, theme.COLORS["info"]),
                                offset=ft.Offset(0, 8),
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Gestión de Servicios",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.COLORS["text"],
                                ),
                                ft.Text(
                                    "Deshabilita servicios innecesarios para mejorar el rendimiento",
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

            # Acciones rápidas
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.FLASH_ON_ROUNDED, size=22, color=theme.COLORS["warning"]),
                                ft.Text("Acciones Rápidas", size=18, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
                            ],
                            spacing=10,
                        ),
                        ft.Container(height=16),
                        ft.Row(
                            controls=acciones_widgets,
                            spacing=16,
                            wrap=True,
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=24),

            # Lista de servicios
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Servicios Deshabilitables", size=18, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
                                ft.Container(expand=True),
                                estado_texto,
                                ft.Container(
                                    content=ft.Icon(ft.Icons.REFRESH_ROUNDED, size=20, color=theme.COLORS["primary"]),
                                    padding=10,
                                    border_radius=10,
                                    bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                                    on_click=lambda e: cargar_servicios(),
                                    ink=True,
                                ),
                            ],
                            spacing=12,
                        ),
                        ft.Container(height=12),
                        servicios_lista,
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=30),
                expand=True,
            ),

            ft.Container(height=24),
        ],
        expand=True,
    )


class PaginaServicios:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_servicios(page)
