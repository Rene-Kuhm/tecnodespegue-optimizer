"""Página de gestión de bloatware - Estilo CleanMyMac."""
import flet as ft
from src.ui import theme
from src.modules.bloatware import (
    BLOATWARE_APPS, CategoriaBloat, desinstalar_app,
    eliminar_todo_bloatware_recomendado, obtener_apps_por_categoria
)
import threading


def crear_pagina_bloatware(page: ft.Page = None) -> ft.Column:
    """Página para eliminar aplicaciones bloatware con estilo CleanMyMac."""

    categoria_actual = [CategoriaBloat.MICROSOFT]
    apps_seleccionadas = set()
    contenedor_apps = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    estado_texto = ft.Text("", size=14, visible=False)
    progreso_bar = ft.ProgressBar(
        value=0,
        color=theme.COLORS["accent_orange"],
        bgcolor=theme.COLORS["surface_elevated"],
        height=6,
        border_radius=3,
        visible=False
    )

    def actualizar_lista_apps():
        apps = obtener_apps_por_categoria(categoria_actual[0])
        contenedor_apps.controls.clear()

        for app in apps:
            is_recomendado = app.recomendado_eliminar

            item = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Checkbox(
                            value=app.paquete in apps_seleccionadas,
                            on_change=lambda e, a=app: toggle_app(a.paquete, e.control.value),
                            active_color=theme.COLORS["accent_orange"],
                        ),
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.DELETE_SWEEP_ROUNDED if is_recomendado else ft.Icons.APPS_ROUNDED,
                                size=20,
                                color=theme.COLORS["accent_orange"] if is_recomendado else theme.COLORS["primary"]
                            ),
                            padding=10,
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(
                                0.1,
                                theme.COLORS["accent_orange"] if is_recomendado else theme.COLORS["primary"]
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            app.nombre,
                                            size=14,
                                            weight=ft.FontWeight.W_600,
                                            color=theme.COLORS["text"]
                                        ),
                                        ft.Container(
                                            content=ft.Text(
                                                "Eliminar" if is_recomendado else "Conservar",
                                                size=10,
                                                weight=ft.FontWeight.W_500,
                                                color=ft.Colors.WHITE
                                            ),
                                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                            border_radius=12,
                                            bgcolor=theme.COLORS["warning"] if is_recomendado else theme.COLORS["success"],
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                ft.Text(
                                    app.descripcion,
                                    size=12,
                                    color=theme.COLORS["text_muted"]
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=20, color=theme.COLORS["error"]),
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["error"]),
                            on_click=lambda e, a=app: eliminar_app_individual(a),
                            ink=True,
                        ),
                    ],
                    spacing=14,
                ),
                padding=18,
                border_radius=theme.BORDER_RADIUS,
                bgcolor=theme.COLORS["surface"],
                border=ft.border.all(1, theme.COLORS["border"]),
            )
            contenedor_apps.controls.append(item)

    def toggle_app(paquete: str, seleccionado: bool):
        if seleccionado:
            apps_seleccionadas.add(paquete)
        else:
            apps_seleccionadas.discard(paquete)
        if page:
            page.update()

    def cambiar_categoria(categoria: CategoriaBloat):
        categoria_actual[0] = categoria
        actualizar_lista_apps()
        for i, control in enumerate(categorias.controls):
            cat = list(CategoriaBloat)[i]
            is_active = cat == categoria
            control.bgcolor = theme.COLORS["accent_orange"] if is_active else theme.COLORS["surface_light"]
            control.content.color = ft.Colors.WHITE if is_active else theme.COLORS["text_muted"]
        if page:
            page.update()

    def eliminar_app_individual(app):
        estado_texto.visible = True
        estado_texto.value = f"Eliminando {app.nombre}..."
        estado_texto.color = theme.COLORS["info"]
        if page:
            page.update()

        def ejecutar():
            exito, _ = desinstalar_app(app.paquete)
            estado_texto.value = f"{app.nombre} eliminado correctamente" if exito else f"Error al eliminar {app.nombre}"
            estado_texto.color = theme.COLORS["success"] if exito else theme.COLORS["error"]
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    def eliminar_seleccionados(e):
        if not apps_seleccionadas:
            return
        estado_texto.visible = True
        progreso_bar.visible = True
        if page:
            page.update()

        def ejecutar():
            total = len(apps_seleccionadas)
            exitosos = 0
            for i, paquete in enumerate(list(apps_seleccionadas)):
                estado_texto.value = f"Eliminando aplicación {i + 1} de {total}..."
                progreso_bar.value = (i + 1) / total
                if page:
                    page.update()
                exito, _ = desinstalar_app(paquete)
                if exito:
                    exitosos += 1
            estado_texto.value = f"Completado: {exitosos} de {total} apps eliminadas"
            estado_texto.color = theme.COLORS["success"]
            progreso_bar.visible = False
            apps_seleccionadas.clear()
            actualizar_lista_apps()
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    def eliminar_recomendados(e):
        estado_texto.visible = True
        progreso_bar.visible = True
        progreso_bar.value = None
        estado_texto.value = "Eliminando todo el bloatware recomendado..."
        estado_texto.color = theme.COLORS["info"]
        if page:
            page.update()

        def ejecutar():
            exitosos, fallidos = eliminar_todo_bloatware_recomendado()
            estado_texto.value = f"Completado: {exitosos} aplicaciones eliminadas"
            estado_texto.color = theme.COLORS["success"]
            progreso_bar.visible = False
            actualizar_lista_apps()
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    # Botones de categoría
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
                bgcolor=theme.COLORS["accent_orange"] if cat == categoria_actual[0] else theme.COLORS["surface_light"],
                on_click=lambda e, c=cat: cambiar_categoria(c),
                ink=True,
            )
            for cat in CategoriaBloat
        ],
        wrap=True,
        spacing=10,
    )

    # Botones de acción
    btn_eliminar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.DELETE_ROUNDED, size=20, color=ft.Colors.WHITE),
                ft.Text("Eliminar Seleccionados", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ],
            spacing=10,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=14),
        border_radius=theme.BORDER_RADIUS_SM,
        gradient=ft.LinearGradient(
            colors=theme.COLORS["gradient_orange"],
        ),
        on_click=eliminar_seleccionados,
        ink=True,
    )

    btn_recomendados = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.AUTO_DELETE_ROUNDED, size=20, color=ft.Colors.WHITE),
                ft.Text("Eliminar Todo Recomendado", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ],
            spacing=10,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=14),
        border_radius=theme.BORDER_RADIUS_SM,
        bgcolor=theme.COLORS["warning"],
        on_click=eliminar_recomendados,
        ink=True,
    )

    actualizar_lista_apps()

    return ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.DELETE_SWEEP_ROUNDED, size=40, color=ft.Colors.WHITE),
                            padding=16,
                            border_radius=20,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=theme.COLORS["gradient_orange"],
                            ),
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=20,
                                color=ft.Colors.with_opacity(0.3, theme.COLORS["accent_orange"]),
                                offset=ft.Offset(0, 8),
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Eliminar Bloatware",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.COLORS["text"],
                                ),
                                ft.Text(
                                    "Desinstala aplicaciones preinstaladas innecesarias",
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

            # Lista de apps
            ft.Container(
                content=contenedor_apps,
                padding=ft.padding.symmetric(horizontal=30),
                expand=True,
            ),

            # Footer
            ft.Container(
                content=ft.Column(
                    controls=[
                        progreso_bar,
                        ft.Row(
                            controls=[
                                estado_texto,
                                ft.Container(expand=True),
                                btn_eliminar,
                                btn_recomendados,
                            ],
                            spacing=12,
                        ),
                    ],
                    spacing=12,
                ),
                padding=ft.padding.symmetric(horizontal=30, vertical=20),
                bgcolor=theme.COLORS["surface"],
                border=ft.border.only(top=ft.BorderSide(1, theme.COLORS["border"])),
            ),
        ],
        expand=True,
    )


class PaginaBloatware:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_bloatware(page)
