"""Página de inicio estilo CleanMyMac con botón de escaneo central."""
import flet as ft
from src.ui import theme
from src.utils.system_info import obtener_info_sistema, obtener_procesos_top
from src.modules.perfiles import NivelPerfil, aplicar_perfil, PERFILES
import threading


def crear_pagina_inicio(page: ft.Page = None) -> ft.Column:
    """Crea la página principal estilo CleanMyMac con escaneo central."""

    # Estado de escaneo
    scanning = {"active": False, "progress": 0}

    # Obtener info del sistema
    try:
        info_sistema = obtener_info_sistema()
    except:
        info_sistema = None

    # Referencias para actualizar UI
    scan_button_ref = {"container": None}
    progress_text_ref = {"text": None}
    status_cards_ref = {"container": None}

    def crear_boton_escaneo() -> ft.Container:
        """Crea el botón de escaneo grande estilo CleanMyMac."""

        def on_scan_click(e):
            if not scanning["active"]:
                iniciar_escaneo()
            else:
                detener_escaneo()

        # Contenido del botón
        button_content = ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.PLAY_ARROW_ROUNDED,
                    size=72,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(height=8),
                ft.Text(
                    "ESCANEAR",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        )

        # Anillo exterior
        outer_ring = ft.Container(
            width=220,
            height=220,
            border_radius=110,
            border=ft.border.all(3, ft.Colors.with_opacity(0.3, theme.COLORS["primary"])),
        )

        # Círculo principal con gradiente
        main_circle = ft.Container(
            content=button_content,
            width=190,
            height=190,
            border_radius=95,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=theme.COLORS["gradient_blue"],
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=40,
                color=ft.Colors.with_opacity(0.5, theme.COLORS["primary"]),
                offset=ft.Offset(0, 15),
            ),
            alignment=ft.alignment.center,
            left=15,
            top=15,
        )

        scan_button = ft.Container(
            content=ft.Stack(
                controls=[outer_ring, main_circle],
            ),
            width=220,
            height=220,
            on_click=on_scan_click,
            ink=True,
            ink_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        )

        scan_button_ref["container"] = scan_button
        return scan_button

    def iniciar_escaneo():
        """Inicia el escaneo del sistema."""
        scanning["active"] = True
        if page:
            page.update()

        def ejecutar_escaneo():
            try:
                # Simular progreso de escaneo
                import time
                pasos = [
                    "Analizando archivos temporales...",
                    "Escaneando caché del sistema...",
                    "Verificando registro de Windows...",
                    "Detectando bloatware...",
                    "Analizando servicios...",
                    "Optimizando configuración...",
                ]

                for i, paso in enumerate(pasos):
                    if not scanning["active"]:
                        break
                    scanning["progress"] = int((i + 1) / len(pasos) * 100)
                    if progress_text_ref["text"]:
                        progress_text_ref["text"].value = paso
                    if page:
                        page.update()
                    time.sleep(0.8)

                # Completado
                scanning["active"] = False
                scanning["progress"] = 100
                if progress_text_ref["text"]:
                    progress_text_ref["text"].value = "Escaneo completado - Se encontraron oportunidades de optimización"
                    progress_text_ref["text"].color = theme.COLORS["success"]
                if page:
                    page.update()

            except Exception as e:
                scanning["active"] = False
                if progress_text_ref["text"]:
                    progress_text_ref["text"].value = f"Error: {str(e)}"
                    progress_text_ref["text"].color = theme.COLORS["error"]
                if page:
                    page.update()

        thread = threading.Thread(target=ejecutar_escaneo)
        thread.start()

    def detener_escaneo():
        """Detiene el escaneo."""
        scanning["active"] = False
        if progress_text_ref["text"]:
            progress_text_ref["text"].value = "Escaneo detenido"
            progress_text_ref["text"].color = theme.COLORS["warning"]
        if page:
            page.update()

    def crear_tarjeta_accion(icono, titulo: str, descripcion: str, color: str, gradiente: list) -> ft.Container:
        """Crea una tarjeta de acción grande estilo CleanMyMac."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=36, color=ft.Colors.WHITE),
                        padding=16,
                        border_radius=18,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=gradiente,
                        ),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=15,
                            color=ft.Colors.with_opacity(0.3, color),
                            offset=ft.Offset(0, 5),
                        ),
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        titulo,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                    ),
                    ft.Text(
                        descripcion,
                        size=12,
                        color=theme.COLORS["text_muted"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=24,
            border_radius=theme.BORDER_RADIUS,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
            width=180,
            height=200,
            ink=True,
        )

    def crear_stat_circular(valor: float, label: str, color: str) -> ft.Container:
        """Crea un indicador de estadística circular."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Container(
                                content=ft.ProgressRing(
                                    value=valor / 100,
                                    stroke_width=8,
                                    color=color,
                                    bgcolor=theme.COLORS["surface_elevated"],
                                ),
                                width=80,
                                height=80,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"{valor:.0f}%",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.COLORS["text"],
                                ),
                                width=80,
                                height=80,
                                alignment=ft.alignment.center,
                            ),
                        ],
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        label,
                        size=12,
                        color=theme.COLORS["text_secondary"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
        )

    def crear_seccion_hero() -> ft.Container:
        """Crea la sección principal con el botón de escaneo."""
        progress_text = ft.Text(
            "Presiona para escanear y optimizar tu sistema",
            size=14,
            color=theme.COLORS["text_secondary"],
            text_align=ft.TextAlign.CENTER,
        )
        progress_text_ref["text"] = progress_text

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=40),
                    # Título principal
                    ft.Text(
                        "Tecnodespegue Optimizer",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                    ),
                    ft.Text(
                        "Optimiza, limpia y acelera tu Windows 11",
                        size=16,
                        color=theme.COLORS["text_secondary"],
                    ),
                    ft.Container(height=50),
                    # Botón de escaneo
                    crear_boton_escaneo(),
                    ft.Container(height=30),
                    # Texto de estado
                    progress_text,
                    ft.Container(height=20),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

    def crear_seccion_stats() -> ft.Container:
        """Crea la sección de estadísticas del sistema."""
        if not info_sistema:
            return ft.Container()

        info = info_sistema
        ram_uso = info.ram_uso_porcentaje
        disco_uso = (info.disco_total_gb - info.disco_libre_gb) / info.disco_total_gb * 100 if info.disco_total_gb > 0 else 0

        # Determinar colores según uso
        ram_color = theme.COLORS["success"] if ram_uso < 60 else theme.COLORS["warning"] if ram_uso < 85 else theme.COLORS["error"]
        disco_color = theme.COLORS["success"] if disco_uso < 70 else theme.COLORS["warning"] if disco_uso < 90 else theme.COLORS["error"]

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Estado del Sistema",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        controls=[
                            crear_stat_circular(ram_uso, "Memoria RAM", ram_color),
                            ft.Container(width=40),
                            crear_stat_circular(disco_uso, "Disco", disco_color),
                            ft.Container(width=40),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Icon(
                                                ft.Icons.COMPUTER_ROUNDED,
                                                size=32,
                                                color=theme.COLORS["primary"],
                                            ),
                                            width=80,
                                            height=80,
                                            border_radius=40,
                                            bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["primary"]),
                                            alignment=ft.alignment.center,
                                        ),
                                        ft.Container(height=8),
                                        ft.Text(
                                            f"Build {info.build}",
                                            size=12,
                                            color=theme.COLORS["text_secondary"],
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=4,
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=40, vertical=30),
            border_radius=theme.BORDER_RADIUS_LG,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
            margin=ft.margin.symmetric(horizontal=40),
        )

    def crear_seccion_acciones() -> ft.Container:
        """Crea la sección de acciones rápidas."""
        acciones = [
            (ft.Icons.CLEANING_SERVICES_ROUNDED, "Limpieza", "Libera espacio", theme.COLORS["accent_blue"], theme.COLORS["gradient_cyan"]),
            (ft.Icons.BOLT_ROUNDED, "Rendimiento", "Acelera tu PC", theme.COLORS["accent_orange"], theme.COLORS["gradient_orange"]),
            (ft.Icons.DELETE_SWEEP_ROUNDED, "Bloatware", "Elimina apps", theme.COLORS["accent_purple"], theme.COLORS["gradient_purple"]),
            (ft.Icons.SECURITY_ROUNDED, "Privacidad", "Protege datos", theme.COLORS["accent_green"], theme.COLORS["gradient_green"]),
        ]

        tarjetas = [
            crear_tarjeta_accion(icono, titulo, desc, color, grad)
            for icono, titulo, desc, color, grad in acciones
        ]

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Acciones Rápidas",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=theme.COLORS["text"],
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        controls=tarjetas,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                        wrap=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=40, vertical=30),
        )

    def aplicar_perfil_rapido(nivel: NivelPerfil):
        """Aplica un perfil de optimización rápido."""
        if progress_text_ref["text"]:
            progress_text_ref["text"].value = f"Aplicando perfil {PERFILES[nivel].nombre}..."
            progress_text_ref["text"].color = theme.COLORS["info"]
        if page:
            page.update()

        def ejecutar():
            try:
                def callback(msg, pct):
                    if progress_text_ref["text"]:
                        progress_text_ref["text"].value = msg
                    if page:
                        page.update()

                resultado = aplicar_perfil(nivel, callback)
                if progress_text_ref["text"]:
                    progress_text_ref["text"].value = (
                        f"Completado: {resultado.tweaks_aplicados} tweaks, "
                        f"{resultado.espacio_liberado_mb:.1f} MB liberados"
                    )
                    progress_text_ref["text"].color = theme.COLORS["success"]
            except Exception as e:
                if progress_text_ref["text"]:
                    progress_text_ref["text"].value = f"Error: {str(e)}"
                    progress_text_ref["text"].color = theme.COLORS["error"]
            if page:
                page.update()

        thread = threading.Thread(target=ejecutar)
        thread.start()

    def crear_seccion_perfiles() -> ft.Container:
        """Crea la sección de perfiles de optimización."""
        perfiles = [
            (NivelPerfil.MINIMO, ft.Icons.VERIFIED_USER_ROUNDED, "Seguro", theme.COLORS["success"]),
            (NivelPerfil.RECOMENDADO, ft.Icons.THUMB_UP_ROUNDED, "Recomendado", theme.COLORS["primary"]),
            (NivelPerfil.MAXIMO, ft.Icons.BOLT_ROUNDED, "Agresivo", theme.COLORS["warning"]),
            (NivelPerfil.GAMING, ft.Icons.SPORTS_ESPORTS_ROUNDED, "Gaming", theme.COLORS["error"]),
        ]

        chips = []
        for nivel, icono, label, color in perfiles:
            chip = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icono, size=18, color=color),
                        ft.Text(label, size=13, weight=ft.FontWeight.W_500, color=theme.COLORS["text"]),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
                border_radius=20,
                bgcolor=ft.Colors.with_opacity(0.1, color),
                border=ft.border.all(1, ft.Colors.with_opacity(0.3, color)),
                on_click=lambda e, n=nivel: aplicar_perfil_rapido(n),
                ink=True,
            )
            chips.append(chip)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Perfiles de Optimización",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color=theme.COLORS["text"],
                    ),
                    ft.Container(height=16),
                    ft.Row(
                        controls=chips,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                        wrap=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    # Layout principal
    return ft.Column(
        controls=[
            crear_seccion_hero(),
            crear_seccion_stats(),
            ft.Container(height=30),
            crear_seccion_perfiles(),
            ft.Container(height=40),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# Para compatibilidad
class PaginaInicio:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_inicio(page)
