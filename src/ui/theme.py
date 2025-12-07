"""Tema estilo CleanMyMac - Diseño minimalista y elegante."""
import flet as ft

# Paleta de colores estilo CleanMyMac
COLORS = {
    # Fondo principal - degradado oscuro
    "background": "#1a1a2e",
    "background_dark": "#16162a",
    "background_gradient_start": "#1a1a2e",
    "background_gradient_end": "#0f0f1a",

    # Sidebar
    "sidebar": "#0d0d1a",
    "sidebar_hover": "#252540",
    "sidebar_active": "#2d2d4a",

    # Superficies
    "surface": "#252542",
    "surface_light": "#2d2d4f",
    "surface_elevated": "#353560",

    # Colores de acento - Gradientes llamativos
    "primary": "#667eea",
    "primary_light": "#7c94f4",
    "primary_dark": "#5a67d8",

    "accent_blue": "#4facfe",
    "accent_purple": "#667eea",
    "accent_pink": "#f093fb",
    "accent_orange": "#f5576c",
    "accent_green": "#4facfe",
    "accent_yellow": "#ffecd2",

    # Gradientes para botones grandes
    "gradient_blue": ["#667eea", "#764ba2"],
    "gradient_green": ["#11998e", "#38ef7d"],
    "gradient_orange": ["#f5576c", "#f093fb"],
    "gradient_purple": ["#667eea", "#f093fb"],
    "gradient_cyan": ["#4facfe", "#00f2fe"],

    # Texto
    "text": "#ffffff",
    "text_secondary": "#a0a0b8",
    "text_muted": "#6b6b80",
    "text_dark": "#1a1a2e",

    # Estados
    "success": "#38ef7d",
    "warning": "#ffc107",
    "error": "#f5576c",
    "info": "#4facfe",

    # Bordes
    "border": "#3d3d5c",
    "border_light": "#4d4d6a",
}

# Radios de borde
BORDER_RADIUS = 20
BORDER_RADIUS_SM = 12
BORDER_RADIUS_LG = 28
BORDER_RADIUS_XL = 36

# Sombras suaves
SHADOW = ft.BoxShadow(
    spread_radius=0,
    blur_radius=30,
    color=ft.Colors.with_opacity(0.3, "#000000"),
    offset=ft.Offset(0, 10)
)

SHADOW_GLOW = ft.BoxShadow(
    spread_radius=4,
    blur_radius=20,
    color=ft.Colors.with_opacity(0.4, COLORS["primary"]),
    offset=ft.Offset(0, 0)
)


def crear_boton_grande(
    texto: str,
    subtexto: str = None,
    icono=None,
    gradiente: list = None,
    on_click=None,
    width: int = 280,
    height: int = 180
) -> ft.Container:
    """Crea un botón grande estilo CleanMyMac."""
    if gradiente is None:
        gradiente = COLORS["gradient_blue"]

    contenido = ft.Column(
        controls=[
            ft.Container(
                content=ft.Icon(icono, size=48, color=ft.Colors.WHITE) if icono else None,
                padding=16,
            ),
            ft.Text(
                texto,
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                subtexto,
                size=12,
                color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                text_align=ft.TextAlign.CENTER,
            ) if subtexto else ft.Container(),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    )

    return ft.Container(
        content=contenido,
        width=width,
        height=height,
        border_radius=BORDER_RADIUS_LG,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=gradiente,
        ),
        shadow=SHADOW,
        on_click=on_click,
        ink=True,
        animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def crear_boton_circular(
    icono,
    texto: str,
    color: str = None,
    on_click=None,
    size: int = 120
) -> ft.Container:
    """Crea un botón circular grande estilo CleanMyMac."""
    if color is None:
        color = COLORS["primary"]

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Icon(icono, size=36, color=ft.Colors.WHITE),
                    width=70,
                    height=70,
                    border_radius=35,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[color, ft.Colors.with_opacity(0.7, color)],
                    ),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=15,
                        color=ft.Colors.with_opacity(0.4, color),
                        offset=ft.Offset(0, 5)
                    ),
                ),
                ft.Container(height=8),
                ft.Text(
                    texto,
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=COLORS["text"],
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        width=size,
        on_click=on_click,
        ink=True,
        padding=10,
        border_radius=BORDER_RADIUS,
    )


def crear_card(content: ft.Control, padding: int = 24) -> ft.Container:
    """Crea una tarjeta con estilo CleanMyMac."""
    return ft.Container(
        content=content,
        padding=padding,
        border_radius=BORDER_RADIUS,
        bgcolor=COLORS["surface"],
        border=ft.border.all(1, COLORS["border"]),
    )


def crear_card_stat(
    valor: str,
    titulo: str,
    icono=None,
    color: str = None
) -> ft.Container:
    """Crea una tarjeta de estadística compacta."""
    if color is None:
        color = COLORS["primary"]

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icono, size=24, color=color) if icono else None,
                    padding=12,
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(0.15, color),
                ) if icono else ft.Container(),
                ft.Column(
                    controls=[
                        ft.Text(valor, size=24, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                        ft.Text(titulo, size=12, color=COLORS["text_secondary"]),
                    ],
                    spacing=2,
                ),
            ],
            spacing=16,
        ),
        padding=20,
        border_radius=BORDER_RADIUS,
        bgcolor=COLORS["surface"],
        border=ft.border.all(1, COLORS["border"]),
    )


def crear_item_lista(
    titulo: str,
    subtitulo: str = None,
    icono=None,
    trailing=None,
    color: str = None,
    on_click=None
) -> ft.Container:
    """Crea un item de lista estilo CleanMyMac."""
    if color is None:
        color = COLORS["primary"]

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icono, size=22, color=color) if icono else None,
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.12, color),
                ) if icono else ft.Container(),
                ft.Column(
                    controls=[
                        ft.Text(titulo, size=14, weight=ft.FontWeight.W_500, color=COLORS["text"]),
                        ft.Text(subtitulo, size=12, color=COLORS["text_muted"]) if subtitulo else ft.Container(),
                    ],
                    spacing=2,
                    expand=True,
                ),
                trailing if trailing else ft.Container(),
            ],
            spacing=14,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
        border_radius=BORDER_RADIUS_SM,
        bgcolor=COLORS["surface_light"],
        on_click=on_click,
        ink=True if on_click else False,
    )


def crear_progreso_circular(
    valor: float,
    texto: str,
    color: str = None,
    size: int = 150
) -> ft.Container:
    """Crea un indicador de progreso circular grande estilo CleanMyMac."""
    if color is None:
        color = COLORS["primary"]

    return ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=ft.ProgressRing(
                        value=valor / 100,
                        stroke_width=8,
                        color=color,
                        bgcolor=COLORS["surface_light"],
                    ),
                    width=size,
                    height=size,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"{valor:.0f}%",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=COLORS["text"],
                            ),
                            ft.Text(
                                texto,
                                size=12,
                                color=COLORS["text_secondary"],
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    width=size,
                    height=size,
                    alignment=ft.alignment.center,
                ),
            ],
        ),
    )


def crear_boton_scan(on_click=None, scanning: bool = False) -> ft.Container:
    """Crea el botón de escaneo principal estilo CleanMyMac."""
    return ft.Container(
        content=ft.Stack(
            controls=[
                # Anillo exterior animado
                ft.Container(
                    width=200,
                    height=200,
                    border_radius=100,
                    border=ft.border.all(3, COLORS["primary"]) if not scanning else None,
                    animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
                ),
                # Círculo interior con gradiente
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(
                                ft.Icons.PLAY_ARROW_ROUNDED if not scanning else ft.Icons.STOP_ROUNDED,
                                size=64,
                                color=ft.Colors.WHITE
                            ),
                            ft.Text(
                                "ESCANEAR" if not scanning else "DETENER",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    width=180,
                    height=180,
                    border_radius=90,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=COLORS["gradient_blue"],
                    ),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=30,
                        color=ft.Colors.with_opacity(0.5, COLORS["primary"]),
                        offset=ft.Offset(0, 10)
                    ),
                    alignment=ft.alignment.center,
                    left=10,
                    top=10,
                ),
            ],
        ),
        width=200,
        height=200,
        on_click=on_click,
        ink=True,
        ink_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
    )


def crear_titulo(texto: str, size: int = 28) -> ft.Text:
    """Crea un título."""
    return ft.Text(
        texto,
        size=size,
        weight=ft.FontWeight.BOLD,
        color=COLORS["text"],
    )


def crear_subtitulo(texto: str) -> ft.Text:
    """Crea un subtítulo."""
    return ft.Text(
        texto,
        size=14,
        color=COLORS["text_secondary"],
    )


def crear_seccion_header(titulo: str, subtitulo: str = None, accion=None) -> ft.Container:
    """Crea un header de sección."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(titulo, size=22, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                        ft.Text(subtitulo, size=13, color=COLORS["text_secondary"]) if subtitulo else ft.Container(),
                    ],
                    spacing=4,
                    expand=True,
                ),
                accion if accion else ft.Container(),
            ],
        ),
        padding=ft.padding.only(bottom=20),
    )


def crear_sidebar_item(icono, texto: str, activo: bool = False, on_click=None) -> ft.Container:
    """Crea un item de sidebar estilo CleanMyMac."""
    color = COLORS["primary"] if activo else COLORS["text_muted"]

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icono, size=22, color=color),
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.15, COLORS["primary"]) if activo else None,
                ),
                ft.Text(
                    texto,
                    size=14,
                    weight=ft.FontWeight.W_600 if activo else ft.FontWeight.W_400,
                    color=COLORS["text"] if activo else COLORS["text_muted"],
                ),
            ],
            spacing=12,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border_radius=BORDER_RADIUS_SM,
        bgcolor=COLORS["sidebar_active"] if activo else None,
        on_click=on_click,
        ink=True,
        animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT),
    )


def crear_boton_primario(texto: str, on_click=None, icono=None, disabled: bool = False) -> ft.Container:
    """Crea un botón primario con gradiente."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icono, size=20, color=ft.Colors.WHITE) if icono else ft.Container(),
                ft.Text(texto, size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=28, vertical=14),
        border_radius=BORDER_RADIUS_SM,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=COLORS["gradient_blue"],
        ) if not disabled else None,
        bgcolor=COLORS["surface_elevated"] if disabled else None,
        on_click=on_click if not disabled else None,
        ink=True,
        opacity=0.5 if disabled else 1,
    )


def crear_chip(texto: str, color: str = None, outlined: bool = False) -> ft.Container:
    """Crea un chip/badge."""
    if color is None:
        color = COLORS["primary"]

    if outlined:
        return ft.Container(
            content=ft.Text(texto, size=11, weight=ft.FontWeight.W_500, color=color),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=20,
            border=ft.border.all(1.5, color),
            bgcolor=ft.Colors.with_opacity(0.1, color),
        )

    return ft.Container(
        content=ft.Text(texto, size=11, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
        bgcolor=color,
    )


def crear_switch_item(titulo: str, descripcion: str, valor: bool = False, on_change=None, data=None) -> ft.Container:
    """Crea un item con switch."""
    switch = ft.Switch(
        value=valor,
        on_change=on_change,
        active_color=COLORS["primary"],
        active_track_color=COLORS["primary_light"],
        inactive_thumb_color=COLORS["text_muted"],
        inactive_track_color=COLORS["surface_elevated"],
        data=data,
    )

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(titulo, size=14, weight=ft.FontWeight.W_500, color=COLORS["text"]),
                        ft.Text(descripcion, size=12, color=COLORS["text_muted"]),
                    ],
                    spacing=4,
                    expand=True,
                ),
                switch,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=16),
        border_radius=BORDER_RADIUS_SM,
        bgcolor=COLORS["surface_light"],
        border=ft.border.all(1, COLORS["border"]),
    )
