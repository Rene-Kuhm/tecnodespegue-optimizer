"""Página de tweaks individuales - Estilo CleanMyMac."""
import flet as ft
from src.ui import theme
from src.modules.tweaks import (
    TWEAKS_DISPONIBLES, CategoriaTweak, NivelRiesgo,
    obtener_tweaks_por_categoria
)
import threading


def crear_pagina_tweaks(page: ft.Page = None) -> ft.Column:
    """Página para aplicar tweaks individuales con estilo CleanMyMac."""

    categoria_actual = [CategoriaTweak.RENDIMIENTO]
    tweaks_seleccionados = set()
    contenedor_tweaks = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    estado_texto = ft.Text("", size=14, visible=False)

    def actualizar_lista_tweaks():
        """Actualiza la lista de tweaks mostrados."""
        tweaks = obtener_tweaks_por_categoria(categoria_actual[0])
        contenedor_tweaks.controls.clear()

        for tweak in tweaks:
            color_riesgo = {
                NivelRiesgo.BAJO: theme.COLORS["success"],
                NivelRiesgo.MEDIO: theme.COLORS["warning"],
                NivelRiesgo.ALTO: theme.COLORS["error"],
            }.get(tweak.riesgo, theme.COLORS["text_secondary"])

            checkbox = ft.Checkbox(
                value=tweak.id in tweaks_seleccionados,
                on_change=lambda e, t=tweak: toggle_tweak(t.id, e.control.value),
                active_color=theme.COLORS["primary"],
            )

            item = ft.Container(
                content=ft.Row(
                    controls=[
                        checkbox,
                        ft.Container(
                            content=ft.Icon(ft.Icons.TUNE_ROUNDED, size=20, color=theme.COLORS["primary"]),
                            padding=10,
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            tweak.nombre,
                                            size=14,
                                            weight=ft.FontWeight.W_600,
                                            color=theme.COLORS["text"]
                                        ),
                                        ft.Container(
                                            content=ft.Text(
                                                tweak.riesgo.value,
                                                size=10,
                                                weight=ft.FontWeight.W_500,
                                                color=ft.Colors.WHITE
                                            ),
                                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                            border_radius=12,
                                            bgcolor=color_riesgo,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                ft.Text(
                                    tweak.descripcion,
                                    size=12,
                                    color=theme.COLORS["text_muted"]
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                    ],
                    spacing=14,
                ),
                padding=18,
                border_radius=theme.BORDER_RADIUS,
                bgcolor=theme.COLORS["surface"],
                border=ft.border.all(1, theme.COLORS["border"]),
            )
            contenedor_tweaks.controls.append(item)

    def toggle_tweak(tweak_id: str, seleccionado: bool):
        if seleccionado:
            tweaks_seleccionados.add(tweak_id)
        else:
            tweaks_seleccionados.discard(tweak_id)
        if page:
            page.update()

    def cambiar_categoria(categoria: CategoriaTweak):
        categoria_actual[0] = categoria
        actualizar_lista_tweaks()
        # Actualizar estilos de botones de categoría
        for i, control in enumerate(categorias.controls):
            cat = list(CategoriaTweak)[i]
            is_active = cat == categoria
            control.bgcolor = theme.COLORS["primary"] if is_active else theme.COLORS["surface_light"]
            control.content.color = ft.Colors.WHITE if is_active else theme.COLORS["text_muted"]
        if page:
            page.update()

    def aplicar_seleccionados(e):
        if not tweaks_seleccionados:
            return
        estado_texto.visible = True
        estado_texto.value = "Aplicando tweaks..."
        estado_texto.color = theme.COLORS["info"]
        if page:
            page.update()

        def ejecutar():
            exitosos = 0
            for tweak_id in tweaks_seleccionados:
                for tweak in TWEAKS_DISPONIBLES:
                    if tweak.id == tweak_id:
                        try:
                            exito, _ = tweak.aplicar()
                            if exito:
                                exitosos += 1
                        except:
                            pass
                        break
            estado_texto.value = f"Completado: {exitosos} tweaks aplicados"
            estado_texto.color = theme.COLORS["success"]
            tweaks_seleccionados.clear()
            actualizar_lista_tweaks()
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    # Botones de categoría estilo CleanMyMac
    categorias = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(
                    cat.value,
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.WHITE if cat == categoria_actual[0] else theme.COLORS["text_muted"]
                ),
                padding=ft.padding.symmetric(horizontal=18, vertical=10),
                border_radius=20,
                bgcolor=theme.COLORS["primary"] if cat == categoria_actual[0] else theme.COLORS["surface_light"],
                on_click=lambda e, c=cat: cambiar_categoria(c),
                ink=True,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )
            for cat in CategoriaTweak
        ],
        wrap=True,
        spacing=10,
    )

    # Botón de aplicar con gradiente
    btn_aplicar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=20, color=ft.Colors.WHITE),
                ft.Text("Aplicar Seleccionados", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=28, vertical=14),
        border_radius=theme.BORDER_RADIUS_SM,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=theme.COLORS["gradient_blue"],
        ),
        on_click=aplicar_seleccionados,
        ink=True,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, theme.COLORS["primary"]),
            offset=ft.Offset(0, 5),
        ),
    )

    actualizar_lista_tweaks()

    return ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.TUNE_ROUNDED, size=40, color=ft.Colors.WHITE),
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
                                color=ft.Colors.with_opacity(0.3, theme.COLORS["primary"]),
                                offset=ft.Offset(0, 8),
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Tweaks del Sistema",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.COLORS["text"],
                                ),
                                ft.Text(
                                    "Personaliza las optimizaciones de Windows",
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

            # Categorías
            ft.Container(
                content=categorias,
                padding=ft.padding.symmetric(horizontal=30),
            ),

            ft.Container(height=16),

            # Lista de tweaks
            ft.Container(
                content=contenedor_tweaks,
                padding=ft.padding.symmetric(horizontal=30),
                expand=True,
            ),

            # Footer con botón y estado
            ft.Container(
                content=ft.Row(
                    controls=[
                        estado_texto,
                        ft.Container(expand=True),
                        btn_aplicar,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.symmetric(horizontal=30, vertical=20),
                bgcolor=theme.COLORS["surface"],
                border=ft.border.only(top=ft.BorderSide(1, theme.COLORS["border"])),
            ),
        ],
        expand=True,
    )


class PaginaTweaks:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_tweaks(page)
