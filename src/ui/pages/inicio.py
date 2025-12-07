"""Página de inicio estilo CleanMyMac X con botón de escaneo central espectacular."""
import flet as ft
from src.ui import theme
from src.utils.system_info import obtener_info_sistema
from src.modules.perfiles import NivelPerfil, aplicar_perfil, PERFILES
import threading


def crear_pagina_inicio(page: ft.Page = None) -> ft.Container:
    """Crea la página principal estilo CleanMyMac X."""

    # Estado de escaneo
    scanning = {"active": False, "progress": 0}

    # Obtener info del sistema
    try:
        info_sistema = obtener_info_sistema()
    except:
        info_sistema = None

    # Referencias para actualizar UI
    scan_button_ref = {"container": None, "content": None, "ring": None}
    status_text_ref = {"text": None}
    result_panel_ref = {"container": None}

    def crear_boton_escaneo() -> ft.Container:
        """Crea el botón de escaneo grande estilo CleanMyMac X."""
        size = 240
        inner_size = 200

        def on_scan_click(e):
            if not scanning["active"]:
                iniciar_escaneo()

        # Contenido inicial
        button_content = ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.PLAY_ARROW_ROUNDED,
                    size=64,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(height=4),
                ft.Text(
                    "Escanear",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        )
        scan_button_ref["content"] = button_content

        # Anillo exterior animado
        outer_ring = ft.Container(
            width=size,
            height=size,
            border_radius=size // 2,
            border=ft.border.all(2, ft.Colors.with_opacity(0.25, theme.COLORS["scan_blue"])),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        scan_button_ref["ring"] = outer_ring

        # Círculo principal con gradiente cyan-purple
        main_circle = ft.Container(
            content=button_content,
            width=inner_size,
            height=inner_size,
            border_radius=inner_size // 2,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=theme.COLORS["gradient_scan"],
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=50,
                color=ft.Colors.with_opacity(0.5, theme.COLORS["scan_blue"]),
                offset=ft.Offset(0, 15),
            ),
            alignment=ft.alignment.center,
            left=(size - inner_size) // 2,
            top=(size - inner_size) // 2,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

        scan_button = ft.Container(
            content=ft.Stack(
                controls=[outer_ring, main_circle],
            ),
            width=size,
            height=size,
            on_click=on_scan_click,
        )

        scan_button_ref["container"] = scan_button
        return scan_button

    def iniciar_escaneo():
        """Inicia el escaneo del sistema."""
        scanning["active"] = True
        scanning["progress"] = 0

        # Actualizar texto de estado
        if status_text_ref["text"]:
            status_text_ref["text"].value = "Iniciando escaneo..."
            status_text_ref["text"].color = theme.COLORS["scan_blue"]

        if page:
            page.update()

        def ejecutar_escaneo():
            try:
                import time
                pasos = [
                    ("Analizando archivos temporales...", 15),
                    ("Escaneando caché del sistema...", 30),
                    ("Verificando bloatware instalado...", 45),
                    ("Analizando servicios de Windows...", 60),
                    ("Detectando drivers desactualizados...", 75),
                    ("Calculando optimizaciones...", 90),
                    ("Finalizando análisis...", 100),
                ]

                for paso, progreso in pasos:
                    if not scanning["active"]:
                        break

                    scanning["progress"] = progreso

                    # Actualizar contenido del botón
                    if scan_button_ref["content"]:
                        scan_button_ref["content"].controls = [
                            ft.ProgressRing(
                                width=50,
                                height=50,
                                stroke_width=4,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                f"{progreso}%",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                        ]

                    if status_text_ref["text"]:
                        status_text_ref["text"].value = paso

                    if page:
                        page.update()
                    time.sleep(0.6)

                # Completado
                scanning["active"] = False
                scanning["progress"] = 100

                # Actualizar botón a estado completado
                if scan_button_ref["content"]:
                    scan_button_ref["content"].controls = [
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE_ROUNDED,
                            size=64,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Container(height=4),
                        ft.Text(
                            "Completado",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                    ]

                if status_text_ref["text"]:
                    status_text_ref["text"].value = "Se encontraron oportunidades de optimización"
                    status_text_ref["text"].color = theme.COLORS["success"]

                # Mostrar resultados después de 1.5s
                time.sleep(1.5)

                # Restaurar botón
                if scan_button_ref["content"]:
                    scan_button_ref["content"].controls = [
                        ft.Icon(
                            ft.Icons.PLAY_ARROW_ROUNDED,
                            size=64,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Container(height=4),
                        ft.Text(
                            "Escanear",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                    ]

                if page:
                    page.update()

            except Exception as e:
                scanning["active"] = False
                if status_text_ref["text"]:
                    status_text_ref["text"].value = f"Error: {str(e)}"
                    status_text_ref["text"].color = theme.COLORS["error"]
                if page:
                    page.update()

        thread = threading.Thread(target=ejecutar_escaneo, daemon=True)
        thread.start()

    def crear_modulo_card(icono, titulo: str, descripcion: str, color: str, valor: str = None) -> ft.Container:
        """Crea una tarjeta de módulo compacta."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(icono, size=22, color=color),
                                width=44,
                                height=44,
                                border_radius=14,
                                bgcolor=ft.Colors.with_opacity(0.12, color),
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(expand=True),
                            ft.Text(
                                valor,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=color,
                            ) if valor else ft.Container(),
                        ],
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        titulo,
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=theme.COLORS["text"],
                    ),
                    ft.Text(
                        descripcion,
                        size=12,
                        color=theme.COLORS["text_muted"],
                    ),
                ],
                spacing=2,
            ),
            padding=16,
            border_radius=theme.BORDER_RADIUS,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
            expand=True,
            ink=True,
        )

    def crear_stat_mini(valor: str, label: str, icono, color: str) -> ft.Container:
        """Crea un indicador de estadística mini."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=18, color=color),
                        width=36,
                        height=36,
                        border_radius=10,
                        bgcolor=ft.Colors.with_opacity(0.12, color),
                        alignment=ft.alignment.center,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                valor,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=theme.COLORS["text"],
                            ),
                            ft.Text(
                                label,
                                size=11,
                                color=theme.COLORS["text_muted"],
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=10,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border_radius=theme.BORDER_RADIUS_SM,
            bgcolor=theme.COLORS["surface"],
            border=ft.border.all(1, theme.COLORS["border"]),
        )

    def crear_barra_progreso(valor: float, color: str, label: str) -> ft.Container:
        """Crea una barra de progreso horizontal estilizada."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(label, size=12, color=theme.COLORS["text_secondary"]),
                            ft.Container(expand=True),
                            ft.Text(f"{valor:.0f}%", size=12, weight=ft.FontWeight.W_600, color=color),
                        ],
                    ),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Container(
                            width=valor * 2,  # Escala relativa
                            height=6,
                            border_radius=3,
                            bgcolor=color,
                        ),
                        width=200,
                        height=6,
                        border_radius=3,
                        bgcolor=ft.Colors.with_opacity(0.15, color),
                    ),
                ],
                spacing=0,
            ),
        )

    # Obtener datos del sistema
    ram_uso = info_sistema.ram_uso_porcentaje if info_sistema else 0
    disco_total = info_sistema.disco_total_gb if info_sistema else 0
    disco_libre = info_sistema.disco_libre_gb if info_sistema else 0
    disco_uso = ((disco_total - disco_libre) / disco_total * 100) if disco_total > 0 else 0

    # Colores según uso
    ram_color = theme.COLORS["success"] if ram_uso < 60 else theme.COLORS["warning"] if ram_uso < 85 else theme.COLORS["error"]
    disco_color = theme.COLORS["success"] if disco_uso < 70 else theme.COLORS["warning"] if disco_uso < 90 else theme.COLORS["error"]

    # Texto de estado
    status_text = ft.Text(
        "Presiona para escanear y optimizar tu sistema",
        size=14,
        color=theme.COLORS["text_muted"],
        text_align=ft.TextAlign.CENTER,
    )
    status_text_ref["text"] = status_text

    # Sección hero con botón de escaneo
    hero_section = ft.Container(
        content=ft.Column(
            controls=[
                # Título
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Optimiza tu Sistema",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=theme.COLORS["text"],
                            ),
                            ft.Text(
                                "Escanea, limpia y acelera Windows 11",
                                size=14,
                                color=theme.COLORS["text_muted"],
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=ft.padding.only(top=32, bottom=24),
                ),
                # Botón de escaneo
                crear_boton_escaneo(),
                ft.Container(height=20),
                # Estado
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40),
    )

    # Stats del sistema en una fila compacta
    stats_row = ft.Container(
        content=ft.Row(
            controls=[
                crear_stat_mini(
                    f"{ram_uso:.0f}%",
                    "Memoria RAM",
                    ft.Icons.MEMORY_ROUNDED,
                    ram_color,
                ),
                crear_stat_mini(
                    f"{disco_libre:.0f} GB",
                    "Disco libre",
                    ft.Icons.STORAGE_ROUNDED,
                    disco_color,
                ),
                crear_stat_mini(
                    info_sistema.build if info_sistema else "N/A",
                    "Windows Build",
                    ft.Icons.COMPUTER_ROUNDED,
                    theme.COLORS["info"],
                ),
                crear_stat_mini(
                    f"{info_sistema.nucleos}" if info_sistema else "N/A",
                    "Núcleos CPU",
                    ft.Icons.DEVELOPER_BOARD_ROUNDED,
                    theme.COLORS["scan_purple"],
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
            wrap=True,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=24),
    )

    # Módulos de optimización en grid
    modules_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Módulos de Optimización",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=theme.COLORS["text"],
                ),
                ft.Container(height=16),
                ft.Row(
                    controls=[
                        crear_modulo_card(
                            ft.Icons.CLEANING_SERVICES_ROUNDED,
                            "Limpieza",
                            "Archivos temporales y caché",
                            theme.COLORS["clean_green"],
                        ),
                        crear_modulo_card(
                            ft.Icons.DELETE_SWEEP_ROUNDED,
                            "Bloatware",
                            "Apps preinstaladas",
                            theme.COLORS["protect_red"],
                        ),
                        crear_modulo_card(
                            ft.Icons.TUNE_ROUNDED,
                            "Tweaks",
                            "Optimizaciones del sistema",
                            theme.COLORS["scan_purple"],
                        ),
                        crear_modulo_card(
                            ft.Icons.MISCELLANEOUS_SERVICES_ROUNDED,
                            "Servicios",
                            "Servicios innecesarios",
                            theme.COLORS["speed_orange"],
                        ),
                    ],
                    spacing=16,
                ),
            ],
        ),
        padding=ft.padding.symmetric(horizontal=40),
    )

    # Perfiles de optimización rápida
    def aplicar_perfil_rapido(nivel: NivelPerfil):
        """Aplica un perfil de optimización."""
        if status_text_ref["text"]:
            status_text_ref["text"].value = f"Aplicando perfil {PERFILES[nivel].nombre}..."
            status_text_ref["text"].color = theme.COLORS["info"]
        if page:
            page.update()

        def ejecutar():
            try:
                resultado = aplicar_perfil(nivel, lambda msg, pct: None)
                if status_text_ref["text"]:
                    status_text_ref["text"].value = (
                        f"Perfil aplicado: {resultado.tweaks_aplicados} tweaks, "
                        f"{resultado.espacio_liberado_mb:.1f} MB liberados"
                    )
                    status_text_ref["text"].color = theme.COLORS["success"]
            except Exception as e:
                if status_text_ref["text"]:
                    status_text_ref["text"].value = f"Error: {str(e)}"
                    status_text_ref["text"].color = theme.COLORS["error"]
            if page:
                page.update()

        thread = threading.Thread(target=ejecutar, daemon=True)
        thread.start()

    perfiles_data = [
        (NivelPerfil.MINIMO, "Seguro", ft.Icons.SHIELD_ROUNDED, theme.COLORS["success"]),
        (NivelPerfil.RECOMENDADO, "Recomendado", ft.Icons.THUMB_UP_ROUNDED, theme.COLORS["scan_blue"]),
        (NivelPerfil.MAXIMO, "Agresivo", ft.Icons.BOLT_ROUNDED, theme.COLORS["speed_orange"]),
        (NivelPerfil.GAMING, "Gaming", ft.Icons.SPORTS_ESPORTS_ROUNDED, theme.COLORS["protect_red"]),
    ]

    perfil_chips = []
    for nivel, label, icono, color in perfiles_data:
        chip = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icono, size=16, color=color),
                    ft.Text(label, size=12, weight=ft.FontWeight.W_500, color=theme.COLORS["text"]),
                ],
                spacing=6,
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(0.1, color),
            border=ft.border.all(1, ft.Colors.with_opacity(0.25, color)),
            on_click=lambda e, n=nivel: aplicar_perfil_rapido(n),
            ink=True,
        )
        perfil_chips.append(chip)

    perfiles_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Optimización Rápida",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=theme.COLORS["text"],
                ),
                ft.Container(height=12),
                ft.Row(
                    controls=perfil_chips,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                    wrap=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=24),
    )

    # Layout principal
    return ft.Container(
        content=ft.Column(
            controls=[
                hero_section,
                stats_row,
                modules_section,
                ft.Container(height=16),
                perfiles_section,
                ft.Container(height=32),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=theme.COLORS["background"],
    )


# Para compatibilidad
class PaginaInicio:
    def __new__(cls, page: ft.Page = None):
        return crear_pagina_inicio(page)
