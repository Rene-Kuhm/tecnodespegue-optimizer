"""Tema estilo CleanMyMac X - Diseño premium minimalista con efectos glass."""
import flet as ft

# Paleta de colores estilo CleanMyMac X
COLORS = {
    # Fondo principal - negro profundo con tintes azules
    "background": "#0c0c14",
    "background_secondary": "#12121c",
    "background_elevated": "#1a1a28",

    # Sidebar - prácticamente negro con transparencia
    "sidebar": "#08080e",
    "sidebar_hover": "#1a1a2a",
    "sidebar_active": "#252538",

    # Superficies con efecto glass
    "surface": "#16161f",
    "surface_light": "#1e1e2a",
    "surface_elevated": "#262635",
    "surface_glass": "#ffffff08",

    # Colores de acento - Gradientes vibrantes estilo CleanMyMac
    "primary": "#6c5ce7",
    "primary_light": "#a29bfe",
    "primary_dark": "#5541d8",

    # Colores de funciones (estilo CleanMyMac)
    "scan_blue": "#00cec9",
    "scan_purple": "#6c5ce7",
    "clean_green": "#00b894",
    "protect_red": "#fd79a8",
    "speed_orange": "#fdcb6e",
    "apps_cyan": "#74b9ff",

    # Gradientes principales
    "gradient_scan": ["#00cec9", "#6c5ce7"],
    "gradient_clean": ["#00b894", "#55efc4"],
    "gradient_protect": ["#fd79a8", "#e84393"],
    "gradient_speed": ["#fdcb6e", "#f39c12"],
    "gradient_primary": ["#6c5ce7", "#a29bfe"],
    "gradient_accent": ["#00cec9", "#00b894"],
    "gradient_purple_pink": ["#6c5ce7", "#fd79a8"],

    # Texto
    "text": "#ffffff",
    "text_secondary": "#b2b2c2",
    "text_muted": "#636380",
    "text_disabled": "#404050",

    # Estados
    "success": "#00b894",
    "warning": "#fdcb6e",
    "error": "#ff7675",
    "info": "#74b9ff",

    # Bordes sutiles
    "border": "#2a2a3a",
    "border_light": "#3a3a4a",
    "border_glow": "#6c5ce720",
}

# Radios de borde más suaves
BORDER_RADIUS = 16
BORDER_RADIUS_SM = 10
BORDER_RADIUS_LG = 24
BORDER_RADIUS_XL = 32
BORDER_RADIUS_FULL = 100

# Espaciado consistente
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "xxl": 48,
}

# Sombras premium
SHADOW_SM = ft.BoxShadow(
    spread_radius=0,
    blur_radius=10,
    color=ft.Colors.with_opacity(0.2, "#000000"),
    offset=ft.Offset(0, 4)
)

SHADOW_MD = ft.BoxShadow(
    spread_radius=0,
    blur_radius=20,
    color=ft.Colors.with_opacity(0.25, "#000000"),
    offset=ft.Offset(0, 8)
)

SHADOW_LG = ft.BoxShadow(
    spread_radius=0,
    blur_radius=40,
    color=ft.Colors.with_opacity(0.3, "#000000"),
    offset=ft.Offset(0, 16)
)

SHADOW_GLOW = ft.BoxShadow(
    spread_radius=2,
    blur_radius=20,
    color=ft.Colors.with_opacity(0.35, COLORS["primary"]),
    offset=ft.Offset(0, 0)
)

SHADOW_GLOW_CYAN = ft.BoxShadow(
    spread_radius=2,
    blur_radius=25,
    color=ft.Colors.with_opacity(0.4, COLORS["scan_blue"]),
    offset=ft.Offset(0, 0)
)


def crear_glass_container(
    content: ft.Control,
    padding: int = 20,
    border_radius: int = BORDER_RADIUS,
    blur: int = 10,
) -> ft.Container:
    """Crea un contenedor con efecto glass/blur."""
    return ft.Container(
        content=content,
        padding=padding,
        border_radius=border_radius,
        bgcolor=COLORS["surface_glass"],
        border=ft.border.all(1, ft.Colors.with_opacity(0.1, "#ffffff")),
        blur=blur,
    )


def crear_boton_escaneo_grande(
    on_click=None,
    scanning: bool = False,
    progress: float = 0,
) -> ft.Container:
    """Crea el botón de escaneo principal estilo CleanMyMac."""
    size = 220
    inner_size = 180

    # Contenido interior
    if scanning:
        inner_content = ft.Column(
            controls=[
                ft.ProgressRing(
                    width=60,
                    height=60,
                    stroke_width=4,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(height=12),
                ft.Text(
                    f"{int(progress)}%",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    "Escaneando...",
                    size=13,
                    color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        )
    else:
        inner_content = ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.PLAY_ARROW_ROUNDED,
                    size=56,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(height=8),
                ft.Text(
                    "Escanear",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        )

    return ft.Container(
        content=ft.Stack(
            controls=[
                # Anillo exterior con glow
                ft.Container(
                    width=size,
                    height=size,
                    border_radius=size // 2,
                    border=ft.border.all(2, ft.Colors.with_opacity(0.3, COLORS["scan_blue"])),
                    shadow=SHADOW_GLOW_CYAN,
                ),
                # Círculo interior con gradiente
                ft.Container(
                    content=inner_content,
                    width=inner_size,
                    height=inner_size,
                    border_radius=inner_size // 2,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=COLORS["gradient_scan"],
                    ),
                    shadow=SHADOW_LG,
                    alignment=ft.alignment.center,
                    left=(size - inner_size) // 2,
                    top=(size - inner_size) // 2,
                ),
            ],
        ),
        width=size,
        height=size,
        on_click=on_click,
    )


def crear_modulo_card(
    icono,
    titulo: str,
    descripcion: str,
    color: str,
    valor: str = None,
    on_click=None,
) -> ft.Container:
    """Crea una tarjeta de módulo estilo CleanMyMac."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icono, size=24, color=color),
                            width=48,
                            height=48,
                            border_radius=14,
                            bgcolor=ft.Colors.with_opacity(0.15, color),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(expand=True),
                        ft.Text(
                            valor,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=color,
                        ) if valor else ft.Container(),
                    ],
                ),
                ft.Container(height=16),
                ft.Text(
                    titulo,
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=COLORS["text"],
                ),
                ft.Text(
                    descripcion,
                    size=13,
                    color=COLORS["text_muted"],
                ),
            ],
            spacing=4,
        ),
        padding=20,
        border_radius=BORDER_RADIUS,
        bgcolor=COLORS["surface"],
        border=ft.border.all(1, COLORS["border"]),
        on_click=on_click,
        ink=True if on_click else False,
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )


def crear_stat_card(
    valor: str,
    titulo: str,
    icono=None,
    color: str = None,
    tendencia: str = None,
) -> ft.Container:
    """Crea una tarjeta de estadística compacta."""
    if color is None:
        color = COLORS["primary"]

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icono, size=20, color=color),
                            width=40,
                            height=40,
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(0.12, color),
                            alignment=ft.alignment.center,
                        ) if icono else ft.Container(),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(tendencia, size=11, color=COLORS["success"]),
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=8,
                            bgcolor=ft.Colors.with_opacity(0.15, COLORS["success"]),
                        ) if tendencia else ft.Container(),
                    ],
                ),
                ft.Container(height=12),
                ft.Text(
                    valor,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text"],
                ),
                ft.Text(
                    titulo,
                    size=12,
                    color=COLORS["text_muted"],
                ),
            ],
            spacing=2,
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
    on_click=None,
    seleccionado: bool = False,
) -> ft.Container:
    """Crea un item de lista estilo CleanMyMac."""
    if color is None:
        color = COLORS["primary"]

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icono, size=20, color=color),
                    width=40,
                    height=40,
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(0.12, color),
                    alignment=ft.alignment.center,
                ) if icono else ft.Container(),
                ft.Column(
                    controls=[
                        ft.Text(
                            titulo,
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=COLORS["text"],
                        ),
                        ft.Text(
                            subtitulo,
                            size=12,
                            color=COLORS["text_muted"],
                        ) if subtitulo else ft.Container(),
                    ],
                    spacing=2,
                    expand=True,
                ),
                trailing if trailing else ft.Container(),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border_radius=BORDER_RADIUS_SM,
        bgcolor=COLORS["surface_elevated"] if seleccionado else COLORS["surface"],
        border=ft.border.all(1, COLORS["primary"] if seleccionado else COLORS["border"]),
        on_click=on_click,
        ink=True if on_click else False,
    )


def crear_progreso_circular(
    valor: float,
    texto: str = None,
    color: str = None,
    size: int = 120,
    stroke: int = 8,
) -> ft.Container:
    """Crea un indicador de progreso circular."""
    if color is None:
        color = COLORS["primary"]

    return ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    content=ft.ProgressRing(
                        value=valor / 100 if valor else None,
                        stroke_width=stroke,
                        color=color,
                        bgcolor=ft.Colors.with_opacity(0.1, color),
                    ),
                    width=size,
                    height=size,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"{valor:.0f}%" if valor else "...",
                                size=size // 4,
                                weight=ft.FontWeight.BOLD,
                                color=COLORS["text"],
                            ),
                            ft.Text(
                                texto,
                                size=11,
                                color=COLORS["text_muted"],
                                text_align=ft.TextAlign.CENTER,
                            ) if texto else ft.Container(),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    width=size,
                    height=size,
                    alignment=ft.alignment.center,
                ),
            ],
        ),
    )


def crear_boton_primario(
    texto: str,
    on_click=None,
    icono=None,
    disabled: bool = False,
    gradient: list = None,
    expand: bool = False,
) -> ft.Container:
    """Crea un botón primario con gradiente."""
    if gradient is None:
        gradient = COLORS["gradient_primary"]

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icono, size=18, color=ft.Colors.WHITE) if icono else ft.Container(),
                ft.Text(
                    texto,
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE if not disabled else COLORS["text_muted"],
                ),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=12),
        border_radius=BORDER_RADIUS_SM,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=gradient,
        ) if not disabled else None,
        bgcolor=COLORS["surface_elevated"] if disabled else None,
        on_click=on_click if not disabled else None,
        ink=True if not disabled else False,
        opacity=0.5 if disabled else 1,
        expand=expand,
        shadow=SHADOW_SM if not disabled else None,
    )


def crear_boton_secundario(
    texto: str,
    on_click=None,
    icono=None,
    color: str = None,
) -> ft.Container:
    """Crea un botón secundario con borde."""
    if color is None:
        color = COLORS["text_secondary"]

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icono, size=18, color=color) if icono else ft.Container(),
                ft.Text(texto, size=14, weight=ft.FontWeight.W_500, color=color),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=12),
        border_radius=BORDER_RADIUS_SM,
        border=ft.border.all(1.5, COLORS["border"]),
        on_click=on_click,
        ink=True,
    )


def crear_chip(
    texto: str,
    color: str = None,
    icono=None,
    on_click=None,
) -> ft.Container:
    """Crea un chip/badge."""
    if color is None:
        color = COLORS["primary"]

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icono, size=14, color=color) if icono else ft.Container(),
                ft.Text(texto, size=12, weight=ft.FontWeight.W_500, color=color),
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=BORDER_RADIUS_FULL,
        bgcolor=ft.Colors.with_opacity(0.12, color),
        on_click=on_click,
        ink=True if on_click else False,
    )


def crear_switch_item(
    titulo: str,
    descripcion: str = None,
    valor: bool = False,
    on_change=None,
    data=None,
    color: str = None,
) -> ft.Container:
    """Crea un item con switch."""
    if color is None:
        color = COLORS["primary"]

    switch = ft.Switch(
        value=valor,
        on_change=on_change,
        active_color=color,
        active_track_color=ft.Colors.with_opacity(0.4, color),
        inactive_thumb_color=COLORS["text_muted"],
        inactive_track_color=COLORS["surface_elevated"],
        data=data,
    )

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            titulo,
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=COLORS["text"],
                        ),
                        ft.Text(
                            descripcion,
                            size=12,
                            color=COLORS["text_muted"],
                        ) if descripcion else ft.Container(),
                    ],
                    spacing=4,
                    expand=True,
                ),
                switch,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
        border_radius=BORDER_RADIUS_SM,
        bgcolor=COLORS["surface"],
        border=ft.border.all(1, COLORS["border"]),
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


def crear_seccion_header(
    titulo: str,
    subtitulo: str = None,
    accion=None,
) -> ft.Container:
    """Crea un header de sección."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            titulo,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["text"],
                        ),
                        ft.Text(
                            subtitulo,
                            size=13,
                            color=COLORS["text_muted"],
                        ) if subtitulo else ft.Container(),
                    ],
                    spacing=4,
                    expand=True,
                ),
                accion if accion else ft.Container(),
            ],
        ),
        padding=ft.padding.only(bottom=16),
    )


def crear_divider() -> ft.Container:
    """Crea un divisor sutil."""
    return ft.Container(
        height=1,
        bgcolor=COLORS["border"],
        margin=ft.margin.symmetric(vertical=8),
    )


def crear_empty_state(
    icono,
    titulo: str,
    descripcion: str,
    color: str = None,
) -> ft.Container:
    """Crea un estado vacío."""
    if color is None:
        color = COLORS["success"]

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Icon(icono, size=48, color=color),
                    width=100,
                    height=100,
                    border_radius=50,
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=20),
                ft.Text(
                    titulo,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text"],
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    descripcion,
                    size=14,
                    color=COLORS["text_muted"],
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        padding=40,
        alignment=ft.alignment.center,
    )


def crear_badge_estado(
    texto: str,
    tipo: str = "info",
) -> ft.Container:
    """Crea un badge de estado."""
    colores = {
        "success": COLORS["success"],
        "warning": COLORS["warning"],
        "error": COLORS["error"],
        "info": COLORS["info"],
    }
    color = colores.get(tipo, COLORS["info"])

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    width=6,
                    height=6,
                    border_radius=3,
                    bgcolor=color,
                ),
                ft.Text(texto, size=11, weight=ft.FontWeight.W_500, color=color),
            ],
            spacing=6,
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_radius=BORDER_RADIUS_FULL,
        bgcolor=ft.Colors.with_opacity(0.12, color),
    )
