"""Página de gestión de bloatware - Estilo CleanMyMac."""
import flet as ft
from src.ui import theme
from src.modules.bloatware import (
    BLOATWARE_APPS, CategoriaBloat, desinstalar_app,
    eliminar_todo_bloatware_recomendado, obtener_apps_instaladas_por_categoria,
    verificar_app_instalada
)
import threading


def crear_pagina_bloatware(page: ft.Page = None) -> ft.Column:
    """Página para eliminar aplicaciones bloatware con estilo CleanMyMac."""

    categoria_actual = [CategoriaBloat.MICROSOFT]
    apps_seleccionadas = set()
    apps_en_lista = []  # Lista local de apps mostradas
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

    def crear_item_app(app):
        """Crea un item de app para la lista."""
        is_recomendado = app.recomendado_eliminar

        return ft.Container(
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
            data=app.paquete,  # Guardar paquete para identificación
        )

    def mostrar_mensaje_limpio():
        """Muestra el mensaje de categoría limpia."""
        contenedor_apps.controls.clear()
        contenedor_apps.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=48, color=theme.COLORS["success"]),
                        ft.Text("¡Limpio!", size=18, weight=ft.FontWeight.BOLD, color=theme.COLORS["text"]),
                        ft.Text("No hay bloatware instalado en esta categoría", size=13, color=theme.COLORS["text_secondary"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        )

    def actualizar_lista_apps():
        nonlocal apps_en_lista

        # Mostrar indicador de carga
        contenedor_apps.controls.clear()
        contenedor_apps.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ProgressRing(width=30, height=30, stroke_width=3, color=theme.COLORS["accent_orange"]),
                        ft.Text("Buscando apps instaladas...", size=13, color=theme.COLORS["text_secondary"]),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        )
        if page:
            page.update()

        def cargar():
            nonlocal apps_en_lista
            # Obtener solo las apps INSTALADAS de esta categoría
            apps_en_lista = obtener_apps_instaladas_por_categoria(categoria_actual[0])
            contenedor_apps.controls.clear()

            if not apps_en_lista:
                mostrar_mensaje_limpio()
            else:
                for app in apps_en_lista:
                    contenedor_apps.controls.append(crear_item_app(app))

            if page:
                page.update()

        threading.Thread(target=cargar).start()

    def eliminar_app_de_lista(paquete: str):
        """Elimina una app de la lista visual sin recargar."""
        nonlocal apps_en_lista
        # Eliminar de la lista local
        apps_en_lista = [a for a in apps_en_lista if a.paquete != paquete]
        # Eliminar de seleccionadas si estaba
        apps_seleccionadas.discard(paquete)

        # Eliminar el contenedor de la UI
        contenedor_apps.controls = [
            ctrl for ctrl in contenedor_apps.controls
            if not (hasattr(ctrl, 'data') and ctrl.data == paquete)
        ]

        # Si no quedan apps, mostrar mensaje de limpio
        if not apps_en_lista:
            mostrar_mensaje_limpio()

        if page:
            page.update()

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
            if exito:
                estado_texto.value = f"{app.nombre} eliminado correctamente"
                estado_texto.color = theme.COLORS["success"]
                # Eliminar de la lista inmediatamente
                eliminar_app_de_lista(app.paquete)
            else:
                estado_texto.value = f"Error al eliminar {app.nombre}"
                estado_texto.color = theme.COLORS["error"]
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
            paquetes_eliminados = []

            for i, paquete in enumerate(list(apps_seleccionadas)):
                estado_texto.value = f"Eliminando aplicación {i + 1} de {total}..."
                progreso_bar.value = (i + 1) / total
                if page:
                    page.update()

                exito, _ = desinstalar_app(paquete)
                if exito:
                    exitosos += 1
                    paquetes_eliminados.append(paquete)
                    # Eliminar de la lista inmediatamente
                    eliminar_app_de_lista(paquete)

            estado_texto.value = f"Completado: {exitosos} de {total} apps eliminadas"
            estado_texto.color = theme.COLORS["success"]
            progreso_bar.visible = False
            apps_seleccionadas.clear()

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
            nonlocal apps_en_lista

            # Obtener apps recomendadas de la lista actual
            apps_recomendadas = [a for a in apps_en_lista if a.recomendado_eliminar]
            total = len(apps_recomendadas)
            exitosos = 0

            for i, app in enumerate(apps_recomendadas):
                estado_texto.value = f"Eliminando {app.nombre}... ({i + 1}/{total})"
                progreso_bar.value = (i + 1) / total
                if page:
                    page.update()

                exito, _ = desinstalar_app(app.paquete)
                if exito:
                    exitosos += 1
                    # Eliminar de la lista inmediatamente
                    eliminar_app_de_lista(app.paquete)

            estado_texto.value = f"Completado: {exitosos} aplicaciones eliminadas"
            estado_texto.color = theme.COLORS["success"]
            progreso_bar.visible = False

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
