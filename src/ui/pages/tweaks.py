"""Página de tweaks individuales."""
import flet as ft
from src.ui import theme
from src.modules.tweaks import (
    TWEAKS_DISPONIBLES, CategoriaTweak, NivelRiesgo,
    obtener_tweaks_por_categoria
)
import threading


def crear_pagina_tweaks(page: ft.Page = None) -> ft.Column:
    """Página para aplicar tweaks individuales."""

    categoria_actual = [CategoriaTweak.RENDIMIENTO]
    tweaks_seleccionados = set()
    contenedor_tweaks = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)
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
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(tweak.nombre, size=14, weight=ft.FontWeight.W_500, color=theme.COLORS["text"]),
                                        ft.Container(
                                            content=ft.Text(tweak.riesgo.value, size=11, color=ft.Colors.WHITE),
                                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                            border_radius=10,
                                            bgcolor=color_riesgo,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                ft.Text(tweak.descripcion, size=12, color=theme.COLORS["text_secondary"]),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                    ],
                    spacing=12,
                ),
                padding=16,
                border_radius=theme.BORDER_RADIUS_SM,
                bgcolor=theme.COLORS["surface_light"],
            )
            contenedor_tweaks.controls.append(item)

    def toggle_tweak(tweak_id: str, seleccionado: bool):
        if seleccionado:
            tweaks_seleccionados.add(tweak_id)
        else:
            tweaks_seleccionados.discard(tweak_id)
        btn_aplicar.disabled = len(tweaks_seleccionados) == 0
        if page:
            page.update()

    def cambiar_categoria(categoria: CategoriaTweak):
        categoria_actual[0] = categoria
        actualizar_lista_tweaks()
        if page:
            page.update()

    def aplicar_seleccionados(e):
        if not tweaks_seleccionados:
            return
        estado_texto.visible = True
        estado_texto.value = "Aplicando tweaks..."
        estado_texto.color = theme.COLORS["text_secondary"]
        btn_aplicar.disabled = True
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
            btn_aplicar.disabled = False
            tweaks_seleccionados.clear()
            actualizar_lista_tweaks()
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    # Botones de categoría
    categorias = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(cat.value, size=13, color=ft.Colors.WHITE if cat == categoria_actual[0] else theme.COLORS["text_secondary"]),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                border_radius=20,
                bgcolor=theme.COLORS["primary"] if cat == categoria_actual[0] else theme.COLORS["surface_light"],
                on_click=lambda e, c=cat: cambiar_categoria(c),
                ink=True,
            )
            for cat in CategoriaTweak
        ],
        wrap=True,
        spacing=8,
    )

    btn_aplicar = theme.crear_boton_primario("Aplicar Seleccionados", on_click=aplicar_seleccionados, icono=ft.Icons.CHECK_CIRCLE, disabled=True)

    actualizar_lista_tweaks()

    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Column(controls=[
                    theme.crear_titulo("Tweaks del Sistema", 24),
                    theme.crear_subtitulo("Personaliza las optimizaciones de Windows"),
                ]),
                padding=20,
            ),
            ft.Container(content=categorias, padding=ft.padding.symmetric(horizontal=20)),
            ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
            ft.Container(content=contenedor_tweaks, padding=ft.padding.symmetric(horizontal=20), expand=True),
            ft.Container(
                content=ft.Column(controls=[estado_texto, btn_aplicar], spacing=8),
                padding=20,
            ),
        ],
        expand=True,
    )


class PaginaTweaks:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_tweaks(page)
