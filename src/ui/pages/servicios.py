"""Página de gestión de servicios de Windows."""
import flet as ft
from src.ui import theme
from src.modules.servicios import (
    obtener_servicios_deshabilitables, deshabilitar_servicio, habilitar_servicio,
    EstadoServicio, TipoInicio,
    deshabilitar_servicios_telemetria, deshabilitar_servicios_xbox, deshabilitar_servicios_hyperv
)
import threading


def crear_pagina_servicios(page: ft.Page = None) -> ft.Column:
    """Página para gestionar servicios de Windows."""

    servicios_lista = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)
    estado_texto = ft.Text("", size=14, visible=False)

    def cargar_servicios():
        servicios_lista.controls.clear()
        servicios_lista.controls.append(
            ft.Container(
                content=ft.Row(controls=[ft.ProgressRing(width=20, height=20, stroke_width=2), ft.Text("Cargando servicios...", color=theme.COLORS["text_secondary"])], spacing=12),
                padding=20,
            )
        )
        if page:
            page.update()

        def cargar():
            servicios = obtener_servicios_deshabilitables()
            servicios_lista.controls.clear()
            for servicio in servicios:
                esta_deshabilitado = servicio.tipo_inicio == TipoInicio.DESHABILITADO
                color_estado = theme.COLORS["warning"] if esta_deshabilitado else (theme.COLORS["success"] if servicio.estado == EstadoServicio.EJECUTANDO else theme.COLORS["text_secondary"])
                texto_estado = "Deshabilitado" if esta_deshabilitado else ("Ejecutando" if servicio.estado == EstadoServicio.EJECUTANDO else "Detenido")

                item = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(controls=[
                                        ft.Text(servicio.nombre, size=14, weight=ft.FontWeight.W_500, color=theme.COLORS["text"]),
                                        ft.Container(content=ft.Text(texto_estado, size=11, color=ft.Colors.WHITE), padding=ft.padding.symmetric(horizontal=8, vertical=2), border_radius=10, bgcolor=color_estado),
                                    ], spacing=8),
                                    ft.Text(servicio.descripcion or servicio.nombre_display, size=12, color=theme.COLORS["text_secondary"]),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Row(controls=[
                                ft.IconButton(icon=ft.Icons.STOP_CIRCLE, icon_color=theme.COLORS["error"], on_click=lambda e, s=servicio: accion_servicio(s, False), disabled=esta_deshabilitado),
                                ft.IconButton(icon=ft.Icons.PLAY_CIRCLE, icon_color=theme.COLORS["success"], on_click=lambda e, s=servicio: accion_servicio(s, True), disabled=not esta_deshabilitado),
                            ], spacing=0),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                    border_radius=theme.BORDER_RADIUS_SM,
                    bgcolor=theme.COLORS["surface_light"],
                )
                servicios_lista.controls.append(item)

            if not servicios:
                servicios_lista.controls.append(ft.Text("No se encontraron servicios", color=theme.COLORS["text_secondary"]))
            if page:
                page.update()

        threading.Thread(target=cargar).start()

    def accion_servicio(servicio, habilitar: bool):
        estado_texto.visible = True
        estado_texto.value = f"{'Habilitando' if habilitar else 'Deshabilitando'} {servicio.nombre}..."
        if page:
            page.update()

        def ejecutar():
            if habilitar:
                exito, _ = habilitar_servicio(servicio.nombre)
            else:
                exito, _ = deshabilitar_servicio(servicio.nombre)
            estado_texto.value = f"{servicio.nombre} {'habilitado' if habilitar else 'deshabilitado'}" if exito else f"Error"
            estado_texto.color = theme.COLORS["success"] if exito else theme.COLORS["error"]
            cargar_servicios()

        threading.Thread(target=ejecutar).start()

    def accion_rapida(funcion, nombre: str):
        estado_texto.visible = True
        estado_texto.value = f"Deshabilitando {nombre}..."
        if page:
            page.update()

        def ejecutar():
            exitosos, _ = funcion()
            estado_texto.value = f"{nombre}: {exitosos} servicios deshabilitados"
            estado_texto.color = theme.COLORS["success"]
            cargar_servicios()

        threading.Thread(target=ejecutar).start()

    acciones_rapidas = ft.Row(
        controls=[
            ft.Container(
                content=ft.Row(controls=[ft.Icon(ft.Icons.VISIBILITY_OFF, color=theme.COLORS["warning"], size=20), ft.Text("Telemetría", size=13, color=theme.COLORS["text"])], spacing=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                border_radius=theme.BORDER_RADIUS_SM,
                bgcolor=theme.COLORS["surface_light"],
                on_click=lambda e: accion_rapida(deshabilitar_servicios_telemetria, "Telemetría"),
                ink=True,
            ),
            ft.Container(
                content=ft.Row(controls=[ft.Icon(ft.Icons.SPORTS_ESPORTS, color=theme.COLORS["error"], size=20), ft.Text("Xbox", size=13, color=theme.COLORS["text"])], spacing=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                border_radius=theme.BORDER_RADIUS_SM,
                bgcolor=theme.COLORS["surface_light"],
                on_click=lambda e: accion_rapida(deshabilitar_servicios_xbox, "Xbox"),
                ink=True,
            ),
            ft.Container(
                content=ft.Row(controls=[ft.Icon(ft.Icons.COMPUTER, color=theme.COLORS["info"], size=20), ft.Text("Hyper-V", size=13, color=theme.COLORS["text"])], spacing=8),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                border_radius=theme.BORDER_RADIUS_SM,
                bgcolor=theme.COLORS["surface_light"],
                on_click=lambda e: accion_rapida(deshabilitar_servicios_hyperv, "Hyper-V"),
                ink=True,
            ),
        ],
        spacing=12,
        wrap=True,
    )

    cargar_servicios()

    return ft.Column(
        controls=[
            ft.Container(content=ft.Column(controls=[theme.crear_titulo("Gestión de Servicios", 24), theme.crear_subtitulo("Deshabilita servicios innecesarios")]), padding=20),
            ft.Container(
                content=theme.crear_card(ft.Column(controls=[
                    ft.Row(controls=[theme.crear_titulo("Acciones Rápidas", 18), ft.Icon(ft.Icons.FLASH_ON, color=theme.COLORS["warning"])], spacing=8),
                    ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
                    acciones_rapidas,
                ])),
                padding=ft.padding.symmetric(horizontal=20),
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Container(
                content=theme.crear_card(ft.Column(controls=[
                    ft.Row(controls=[
                        theme.crear_titulo("Servicios Deshabilitables", 18),
                        ft.IconButton(icon=ft.Icons.REFRESH, icon_color=theme.COLORS["primary"], on_click=lambda e: cargar_servicios()),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    estado_texto,
                    ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
                    servicios_lista,
                ])),
                padding=ft.padding.symmetric(horizontal=20),
                expand=True,
            ),
        ],
        expand=True,
    )


class PaginaServicios:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_servicios(page)
