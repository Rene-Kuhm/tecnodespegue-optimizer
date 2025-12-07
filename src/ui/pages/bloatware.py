"""Página de gestión de bloatware."""
import flet as ft
from src.ui import theme
from src.modules.bloatware import BLOATWARE_APPS, CategoriaBloat, desinstalar_app, eliminar_todo_bloatware_recomendado, obtener_apps_por_categoria
import threading


def crear_pagina_bloatware(page: ft.Page = None) -> ft.Column:
    """Página para eliminar aplicaciones bloatware."""

    categoria_actual = [CategoriaBloat.MICROSOFT]
    apps_seleccionadas = set()
    contenedor_apps = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)
    estado_texto = ft.Text("", size=14, visible=False)
    progreso_bar = ft.ProgressBar(value=0, color=theme.COLORS["primary"], bgcolor=theme.COLORS["surface_light"], height=6, visible=False)

    def actualizar_lista_apps():
        apps = obtener_apps_por_categoria(categoria_actual[0])
        contenedor_apps.controls.clear()
        for app in apps:
            item = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Checkbox(
                            value=app.paquete in apps_seleccionadas,
                            on_change=lambda e, a=app: toggle_app(a.paquete, e.control.value),
                            active_color=theme.COLORS["primary"],
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(controls=[
                                    ft.Text(app.nombre, size=14, weight=ft.FontWeight.W_500, color=theme.COLORS["text"]),
                                    ft.Container(
                                        content=ft.Text("Eliminar" if app.recomendado_eliminar else "Útil", size=11, color=ft.Colors.WHITE),
                                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                        border_radius=10,
                                        bgcolor=theme.COLORS["warning"] if app.recomendado_eliminar else theme.COLORS["success"],
                                    ),
                                ], spacing=8),
                                ft.Text(app.descripcion, size=12, color=theme.COLORS["text_secondary"]),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=theme.COLORS["error"], on_click=lambda e, a=app: eliminar_app_individual(a)),
                    ],
                    spacing=12,
                ),
                padding=16,
                border_radius=theme.BORDER_RADIUS_SM,
                bgcolor=theme.COLORS["surface_light"],
            )
            contenedor_apps.controls.append(item)

    def toggle_app(paquete: str, seleccionado: bool):
        if seleccionado:
            apps_seleccionadas.add(paquete)
        else:
            apps_seleccionadas.discard(paquete)
        btn_eliminar.disabled = len(apps_seleccionadas) == 0
        if page:
            page.update()

    def cambiar_categoria(categoria: CategoriaBloat):
        categoria_actual[0] = categoria
        actualizar_lista_apps()
        if page:
            page.update()

    def eliminar_app_individual(app):
        estado_texto.visible = True
        estado_texto.value = f"Eliminando {app.nombre}..."
        if page:
            page.update()

        def ejecutar():
            exito, _ = desinstalar_app(app.paquete)
            estado_texto.value = f"{app.nombre} eliminado" if exito else f"Error al eliminar {app.nombre}"
            estado_texto.color = theme.COLORS["success"] if exito else theme.COLORS["error"]
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    def eliminar_seleccionados(e):
        if not apps_seleccionadas:
            return
        estado_texto.visible = True
        progreso_bar.visible = True
        btn_eliminar.disabled = True
        if page:
            page.update()

        def ejecutar():
            total = len(apps_seleccionadas)
            exitosos = 0
            for i, paquete in enumerate(list(apps_seleccionadas)):
                estado_texto.value = f"Eliminando... ({i + 1}/{total})"
                progreso_bar.value = (i + 1) / total
                if page:
                    page.update()
                exito, _ = desinstalar_app(paquete)
                if exito:
                    exitosos += 1
            estado_texto.value = f"Completado: {exitosos}/{total} apps eliminadas"
            estado_texto.color = theme.COLORS["success"]
            progreso_bar.visible = False
            btn_eliminar.disabled = False
            apps_seleccionadas.clear()
            actualizar_lista_apps()
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

    def eliminar_recomendados(e):
        estado_texto.visible = True
        progreso_bar.visible = True
        progreso_bar.value = None
        estado_texto.value = "Eliminando bloatware recomendado..."
        if page:
            page.update()

        def ejecutar():
            exitosos, fallidos = eliminar_todo_bloatware_recomendado()
            estado_texto.value = f"Completado: {exitosos} eliminados"
            estado_texto.color = theme.COLORS["success"]
            progreso_bar.visible = False
            actualizar_lista_apps()
            if page:
                page.update()

        threading.Thread(target=ejecutar).start()

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
            for cat in CategoriaBloat
        ],
        wrap=True,
        spacing=8,
    )

    btn_eliminar = theme.crear_boton_primario("Eliminar Seleccionados", on_click=eliminar_seleccionados, icono=ft.Icons.DELETE, disabled=True)
    btn_recomendados = ft.ElevatedButton(
        text="Eliminar Todo Recomendado",
        icon=ft.Icons.AUTO_DELETE,
        on_click=eliminar_recomendados,
        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=theme.COLORS["warning"], padding=ft.padding.symmetric(horizontal=24, vertical=12)),
    )

    actualizar_lista_apps()

    return ft.Column(
        controls=[
            ft.Container(content=ft.Column(controls=[theme.crear_titulo("Eliminar Bloatware", 24), theme.crear_subtitulo("Desinstala aplicaciones preinstaladas")]), padding=20),
            ft.Container(content=categorias, padding=ft.padding.symmetric(horizontal=20)),
            ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
            ft.Container(content=contenedor_apps, padding=ft.padding.symmetric(horizontal=20), expand=True),
            ft.Container(content=ft.Column(controls=[progreso_bar, estado_texto, ft.Row(controls=[btn_eliminar, btn_recomendados], spacing=12)], spacing=8), padding=20),
        ],
        expand=True,
    )


class PaginaBloatware:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_bloatware(page)
