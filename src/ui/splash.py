"""Splash Screen profesional animado estilo CleanMyMac."""
import flet as ft
from src.ui import theme
import threading
import time


def mostrar_splash(page: ft.Page, on_complete: callable):
    """Muestra un splash screen animado profesional."""

    # Configurar página para splash
    page.bgcolor = theme.COLORS["background"]
    page.padding = 0

    # Estado de animación
    animation_state = {"progress": 0, "phase": 0}

    # Referencias para animación
    logo_container_ref = {"ref": None}
    progress_bar_ref = {"ref": None}
    status_text_ref = {"ref": None}
    glow_ring_ref = {"ref": None}
    main_container_ref = {"ref": None}

    # Logo con efecto glow animado
    glow_ring = ft.Container(
        width=140,
        height=140,
        border_radius=70,
        opacity=0,
        animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_OUT),
        shadow=ft.BoxShadow(
            spread_radius=8,
            blur_radius=40,
            color=ft.Colors.with_opacity(0.5, theme.COLORS["scan_blue"]),
        ),
    )
    glow_ring_ref["ref"] = glow_ring

    # Logo principal
    logo_circle = ft.Container(
        content=ft.Icon(
            ft.Icons.ROCKET_LAUNCH_ROUNDED,
            size=50,
            color=ft.Colors.WHITE,
        ),
        width=100,
        height=100,
        border_radius=50,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=theme.COLORS["gradient_scan"],
        ),
        alignment=ft.alignment.center,
        opacity=0,
        scale=0.5,
        animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(600, ft.AnimationCurve.ELASTIC_OUT),
    )
    logo_container_ref["ref"] = logo_circle

    # Título
    title_text = ft.Text(
        "Tecnodespegue",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=theme.COLORS["text"],
        opacity=0,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
    )

    subtitle_text = ft.Text(
        "O P T I M I Z E R",
        size=14,
        weight=ft.FontWeight.W_600,
        color=theme.COLORS["scan_blue"],
        opacity=0,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
    )

    # Barra de progreso
    progress_bar = ft.Container(
        content=ft.Container(
            width=0,
            height=4,
            border_radius=2,
            gradient=ft.LinearGradient(
                colors=theme.COLORS["gradient_scan"],
            ),
            animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
        ),
        width=280,
        height=4,
        border_radius=2,
        bgcolor=ft.Colors.with_opacity(0.1, theme.COLORS["scan_blue"]),
        opacity=0,
        animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
    )
    progress_bar_ref["ref"] = progress_bar

    # Texto de estado
    status_text = ft.Text(
        "Iniciando...",
        size=12,
        color=theme.COLORS["text_muted"],
        opacity=0,
        animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
    )
    status_text_ref["ref"] = status_text

    # Versión
    version_text = ft.Text(
        "v1.0.0",
        size=11,
        color=theme.COLORS["text_muted"],
        opacity=0,
        animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
    )

    # Contenedor principal
    main_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=80),
                # Logo con glow
                ft.Container(
                    content=ft.Stack(
                        controls=[
                            ft.Container(
                                content=glow_ring,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(
                                content=logo_circle,
                                alignment=ft.alignment.center,
                                left=20,
                                top=20,
                            ),
                        ],
                        width=140,
                        height=140,
                    ),
                ),
                ft.Container(height=30),
                # Títulos
                title_text,
                ft.Container(height=4),
                subtitle_text,
                ft.Container(height=50),
                # Progreso
                progress_bar,
                ft.Container(height=12),
                status_text,
                ft.Container(expand=True),
                # Versión
                version_text,
                ft.Container(height=30),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=theme.COLORS["background"],
    )
    main_container_ref["ref"] = main_container

    page.add(main_container)
    page.update()

    def run_animation():
        """Ejecuta la secuencia de animación."""
        try:
            # Fase 1: Logo aparece
            time.sleep(0.2)
            logo_circle.opacity = 1
            logo_circle.scale = 1
            glow_ring.opacity = 1
            page.update()

            # Fase 2: Títulos aparecen
            time.sleep(0.4)
            title_text.opacity = 1
            page.update()

            time.sleep(0.2)
            subtitle_text.opacity = 1
            page.update()

            # Fase 3: Barra de progreso
            time.sleep(0.3)
            progress_bar.opacity = 1
            status_text.opacity = 1
            version_text.opacity = 1
            page.update()

            # Fase 4: Progreso animado
            estados = [
                ("Verificando sistema...", 15),
                ("Cargando módulos...", 35),
                ("Inicializando servicios...", 55),
                ("Preparando interfaz...", 75),
                ("Optimizando rendimiento...", 90),
                ("¡Listo!", 100),
            ]

            for texto, progreso in estados:
                status_text.value = texto
                progress_bar.content.width = progreso * 2.8  # 280px max
                page.update()
                time.sleep(0.25)

            # Fase 5: Fade out
            time.sleep(0.5)
            main_container.opacity = 0
            main_container.animate_opacity = ft.Animation(400, ft.AnimationCurve.EASE_IN)
            page.update()

            time.sleep(0.5)

            # Llamar callback de completado
            on_complete()

        except Exception as e:
            print(f"Error en splash: {e}")
            on_complete()

    # Iniciar animación en hilo separado
    thread = threading.Thread(target=run_animation, daemon=True)
    thread.start()
