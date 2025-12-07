"""Página de limpieza del sistema."""
import flet as ft
from src.ui import theme
from src.modules.limpieza import (
    limpiar_temp_usuario, limpiar_temp_windows, limpiar_prefetch,
    limpiar_cache_windows_update, limpiar_thumbnails, limpiar_logs_windows,
    limpiar_papelera, ejecutar_limpieza_completa
)
import threading


def crear_pagina_limpieza(page: ft.Page = None) -> ft.Column:
    """Página de limpieza del sistema."""

    resultados_lista = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)
    total_liberado = ft.Text("0 MB liberados", size=32, weight=ft.FontWeight.BOLD, color=theme.COLORS["primary"])
    progreso_bar = ft.ProgressBar(value=0, color=theme.COLORS["primary"], bgcolor=theme.COLORS["surface_light"], height=8, visible=False)

    total_acumulado = [0.0]

    def agregar_resultado(resultado):
        icono = ft.Icons.CHECK_CIRCLE if resultado.exito else ft.Icons.ERROR
        color = theme.COLORS["success"] if resultado.exito else theme.COLORS["error"]
        item = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icono, color=color, size=20),
                    ft.Text(resultado.nombre, size=14, color=theme.COLORS["text"], expand=True),
                    ft.Text(f"{resultado.espacio_liberado_mb:.2f} MB", size=14, weight=ft.FontWeight.BOLD, color=theme.COLORS["secondary"]),
                ],
                spacing=12,
            ),
            padding=12,
            border_radius=theme.BORDER_RADIUS_SM,
            bgcolor=theme.COLORS["surface_light"],
        )
        resultados_lista.controls.insert(0, item)

    def actualizar_total(mb: float):
        total_acumulado[0] += mb
        total_liberado.value = f"{total_acumulado[0]:.2f} MB liberados"

    def limpiar_individual(funcion, nombre: str):
        def ejecutar():
            resultado = funcion()
            agregar_resultado(resultado)
            actualizar_total(resultado.espacio_liberado_mb)
            if page:
                page.update()
        threading.Thread(target=ejecutar).start()

    def limpiar_todo(e):
        progreso_bar.visible = True
        progreso_bar.value = None
        btn_limpiar.disabled = True
        resultados_lista.controls.clear()
        total_acumulado[0] = 0
        total_liberado.value = "0 MB liberados"
        if page:
            page.update()

        def ejecutar():
            resultados = ejecutar_limpieza_completa()
            for i, resultado in enumerate(resultados):
                progreso_bar.value = (i + 1) / len(resultados)
                agregar_resultado(resultado)
                total_acumulado[0] += resultado.espacio_liberado_mb
                if page:
                    page.update()
            total_liberado.value = f"{total_acumulado[0]:.2f} MB liberados"
            progreso_bar.visible = False
            btn_limpiar.disabled = False
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    # Opciones de limpieza
    opciones = [
        ("Archivos Temporales (Usuario)", ft.Icons.FOLDER_DELETE, limpiar_temp_usuario),
        ("Archivos Temporales (Windows)", ft.Icons.FOLDER_DELETE, limpiar_temp_windows),
        ("Prefetch", ft.Icons.SPEED, limpiar_prefetch),
        ("Caché de Windows Update", ft.Icons.UPDATE, limpiar_cache_windows_update),
        ("Caché de Miniaturas", ft.Icons.IMAGE, limpiar_thumbnails),
        ("Logs de Windows", ft.Icons.DESCRIPTION, limpiar_logs_windows),
        ("Papelera de Reciclaje", ft.Icons.DELETE_SWEEP, limpiar_papelera),
    ]

    items_limpieza = []
    for nombre, icono, funcion in opciones:
        item = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icono, color=theme.COLORS["primary"], size=24),
                    ft.Text(nombre, size=14, color=theme.COLORS["text"], expand=True),
                    ft.IconButton(icon=ft.Icons.CLEANING_SERVICES, icon_color=theme.COLORS["secondary"], on_click=lambda e, f=funcion, n=nombre: limpiar_individual(f, n)),
                ],
                spacing=12,
            ),
            padding=16,
            border_radius=theme.BORDER_RADIUS_SM,
            bgcolor=theme.COLORS["surface_light"],
        )
        items_limpieza.append(item)

    btn_limpiar = ft.ElevatedButton(
        text="Limpieza Completa",
        icon=ft.Icons.AUTO_DELETE,
        on_click=limpiar_todo,
        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=theme.COLORS["primary"], padding=ft.padding.symmetric(horizontal=32, vertical=16)),
    )

    return ft.Column(
        controls=[
            ft.Container(content=ft.Column(controls=[theme.crear_titulo("Limpieza del Sistema", 24), theme.crear_subtitulo("Elimina archivos temporales y libera espacio")]), padding=20),
            ft.Container(
                content=theme.crear_card(ft.Row(controls=[
                    ft.Column(controls=[ft.Text("Espacio Liberado", size=14, color=theme.COLORS["text_secondary"]), total_liberado], spacing=4),
                    ft.VerticalDivider(width=1, color=theme.COLORS["surface_light"]),
                    ft.Column(controls=[progreso_bar, btn_limpiar], spacing=16, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                ], spacing=32)),
                padding=ft.padding.symmetric(horizontal=20),
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Container(
                content=theme.crear_card(ft.Column(controls=[theme.crear_titulo("Opciones de Limpieza", 18), ft.Divider(height=12, color=ft.Colors.TRANSPARENT), *items_limpieza])),
                padding=ft.padding.symmetric(horizontal=20),
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Container(
                content=theme.crear_card(ft.Column(controls=[theme.crear_titulo("Resultados", 18), ft.Divider(height=12, color=ft.Colors.TRANSPARENT), resultados_lista])),
                padding=ft.padding.symmetric(horizontal=20),
                expand=True,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


class PaginaLimpieza:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_limpieza(page)
