"""Página de limpieza del sistema - Estilo CleanMyMac."""
import flet as ft
from src.ui import theme
from src.modules.limpieza import (
    limpiar_temp_usuario, limpiar_temp_windows, limpiar_prefetch,
    limpiar_cache_windows_update, limpiar_thumbnails, limpiar_logs_windows,
    limpiar_papelera, ejecutar_limpieza_completa
)
import threading


def crear_pagina_limpieza(page: ft.Page = None) -> ft.Column:
    """Página de limpieza del sistema con estilo CleanMyMac."""

    resultados_lista = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)
    total_liberado = ft.Text(
        "0 MB",
        size=48,
        weight=ft.FontWeight.BOLD,
        color=theme.COLORS["success"],
    )
    progreso_bar = ft.ProgressBar(
        value=0,
        color=theme.COLORS["success"],
        bgcolor=theme.COLORS["surface_elevated"],
        height=8,
        border_radius=4,
        visible=False
    )

    total_acumulado = [0.0]
    btn_limpiar = None

    def agregar_resultado(resultado):
        icono = ft.Icons.CHECK_CIRCLE_ROUNDED if resultado.exito else ft.Icons.ERROR_ROUNDED
        color = theme.COLORS["success"] if resultado.exito else theme.COLORS["error"]

        item = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=18, color=color),
                        padding=8,
                        border_radius=10,
                        bgcolor=ft.Colors.with_opacity(0.1, color),
                    ),
                    ft.Text(
                        resultado.nombre,
                        size=14,
                        color=theme.COLORS["text"],
                        expand=True
                    ),
                    ft.Text(
                        f"+{resultado.espacio_liberado_mb:.1f} MB",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["success"] if resultado.espacio_liberado_mb > 0 else theme.COLORS["text_muted"]
                    ),
                ],
                spacing=14,
            ),
            padding=14,
            border_radius=theme.BORDER_RADIUS_SM,
            bgcolor=theme.COLORS["surface_light"],
        )
        resultados_lista.controls.insert(0, item)

    def actualizar_total(mb: float):
        total_acumulado[0] += mb
        if total_acumulado[0] >= 1024:
            total_liberado.value = f"{total_acumulado[0] / 1024:.2f} GB"
        else:
            total_liberado.value = f"{total_acumulado[0]:.1f} MB"

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
        resultados_lista.controls.clear()
        total_acumulado[0] = 0
        total_liberado.value = "0 MB"
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

            if total_acumulado[0] >= 1024:
                total_liberado.value = f"{total_acumulado[0] / 1024:.2f} GB"
            else:
                total_liberado.value = f"{total_acumulado[0]:.1f} MB"

            progreso_bar.visible = False
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    # Opciones de limpieza con iconos mejorados
    opciones = [
        ("Archivos Temporales", ft.Icons.FOLDER_DELETE_ROUNDED, limpiar_temp_usuario, theme.COLORS["scan_blue"]),
        ("Caché de Windows", ft.Icons.CACHED_ROUNDED, limpiar_temp_windows, theme.COLORS["scan_purple"]),
        ("Prefetch", ft.Icons.SPEED_ROUNDED, limpiar_prefetch, theme.COLORS["speed_orange"]),
        ("Windows Update", ft.Icons.UPDATE_ROUNDED, limpiar_cache_windows_update, theme.COLORS["primary"]),
        ("Miniaturas", ft.Icons.IMAGE_ROUNDED, limpiar_thumbnails, theme.COLORS["protect_red"]),
        ("Logs del Sistema", ft.Icons.DESCRIPTION_ROUNDED, limpiar_logs_windows, theme.COLORS["info"]),
        ("Papelera", ft.Icons.DELETE_SWEEP_ROUNDED, limpiar_papelera, theme.COLORS["error"]),
    ]

    items_limpieza = []
    for nombre, icono, funcion, color in opciones:
        item = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=22, color=color),
                        padding=12,
                        border_radius=14,
                        bgcolor=ft.Colors.with_opacity(0.1, color),
                    ),
                    ft.Text(
                        nombre,
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=theme.COLORS["text"],
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.CLEANING_SERVICES_ROUNDED, size=18, color=ft.Colors.WHITE),
                        padding=10,
                        border_radius=10,
                        bgcolor=color,
                        on_click=lambda e, f=funcion, n=nombre: limpiar_individual(f, n),
                        ink=True,
                    ),
                ],
                spacing=16,
            ),
            padding=16,
            border_radius=theme.BORDER_RADIUS,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
        )
        items_limpieza.append(item)

    # Botón de limpieza completa
    btn_limpiar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.AUTO_DELETE_ROUNDED, size=24, color=ft.Colors.WHITE),
                ft.Text("Limpieza Completa", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=18),
        border_radius=theme.BORDER_RADIUS,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=theme.COLORS["gradient_clean"],
        ),
        on_click=limpiar_todo,
        ink=True,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=25,
            color=ft.Colors.with_opacity(0.4, theme.COLORS["success"]),
            offset=ft.Offset(0, 10),
        ),
    )

    return ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.CLEANING_SERVICES_ROUNDED, size=40, color=ft.Colors.WHITE),
                            padding=16,
                            border_radius=20,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=theme.COLORS["gradient_clean"],
                            ),
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=20,
                                color=ft.Colors.with_opacity(0.3, theme.COLORS["success"]),
                                offset=ft.Offset(0, 8),
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Limpieza del Sistema",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.COLORS["text"],
                                ),
                                ft.Text(
                                    "Elimina archivos temporales y libera espacio en disco",
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

            # Panel de espacio liberado
            ft.Container(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Espacio Liberado",
                                size=14,
                                color=theme.COLORS["text_muted"],
                            ),
                            total_liberado,
                            ft.Container(height=16),
                            progreso_bar,
                            ft.Container(height=16),
                            btn_limpiar,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=40,
                    border_radius=theme.BORDER_RADIUS_LG,
                    bgcolor=theme.COLORS["surface"],
                    border=ft.border.all(1, theme.COLORS["border"]),
                ),
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=24),

            # Grid de opciones
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Opciones de Limpieza",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=theme.COLORS["text"],
                        ),
                        ft.Container(height=16),
                        ft.Row(
                            controls=items_limpieza[:4],
                            wrap=True,
                            spacing=12,
                            run_spacing=12,
                        ),
                        ft.Row(
                            controls=items_limpieza[4:],
                            wrap=True,
                            spacing=12,
                            run_spacing=12,
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=24),

            # Resultados
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Historial de Limpieza",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=theme.COLORS["text"],
                        ),
                        ft.Container(height=12),
                        ft.Container(
                            content=resultados_lista,
                            padding=16,
                            border_radius=theme.BORDER_RADIUS,
                            bgcolor=theme.COLORS["surface"],
                            border=ft.border.all(1, theme.COLORS["border"]),
                            height=200,
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=30),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


class PaginaLimpieza:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_limpieza(page)
