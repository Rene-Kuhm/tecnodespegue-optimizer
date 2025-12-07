"""Tema y estilos de la aplicación - Diseño Profesional Premium."""
import flet as ft

# Paleta de colores premium - Estilo moderno y profesional
COLORS = {
    # Colores primarios con gradiente mental
    "primary": "#7c3aed",         # Violeta vibrante
    "primary_light": "#a78bfa",   # Violeta claro
    "primary_dark": "#5b21b6",    # Violeta oscuro

    # Acentos
    "secondary": "#06b6d4",       # Cyan
    "accent": "#f472b6",          # Rosa

    # Fondos con profundidad
    "background": "#09090b",      # Negro profundo
    "surface": "#18181b",         # Zinc 900
    "surface_light": "#27272a",   # Zinc 800
    "surface_elevated": "#3f3f46", # Zinc 700

    # Textos
    "text": "#fafafa",            # Zinc 50
    "text_secondary": "#a1a1aa",  # Zinc 400
    "text_muted": "#71717a",      # Zinc 500

    # Estados
    "success": "#10b981",         # Emerald
    "success_light": "#34d399",
    "warning": "#f59e0b",         # Amber
    "warning_light": "#fbbf24",
    "error": "#ef4444",           # Red
    "error_light": "#f87171",
    "info": "#3b82f6",            # Blue
    "info_light": "#60a5fa",

    # Bordes y divisores
    "border": "#3f3f46",
    "divider": "#27272a",
}

# Bordes redondeados
BORDER_RADIUS = 16
BORDER_RADIUS_SM = 10
BORDER_RADIUS_LG = 20
BORDER_RADIUS_XL = 24

# Sombras con más profundidad
SHADOW = ft.BoxShadow(
    spread_radius=0,
    blur_radius=20,
    color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
    offset=ft.Offset(0, 8)
)

SHADOW_SM = ft.BoxShadow(
    spread_radius=0,
    blur_radius=10,
    color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
    offset=ft.Offset(0, 4)
)

SHADOW_GLOW = ft.BoxShadow(
    spread_radius=2,
    blur_radius=15,
    color=ft.Colors.with_opacity(0.3, COLORS["primary"]),
    offset=ft.Offset(0, 0)
)


def crear_card(content: ft.Control, padding: int = 24, elevated: bool = False) -> ft.Container:
    """Crea una tarjeta con estilo premium."""
    return ft.Container(
        content=content,
        padding=padding,
        border_radius=BORDER_RADIUS,
        bgcolor=COLORS["surface"],
        border=ft.border.all(1, COLORS["border"]) if not elevated else None,
        shadow=SHADOW if elevated else SHADOW_SM,
    )


def crear_card_gradient(content: ft.Control, padding: int = 24) -> ft.Container:
    """Crea una tarjeta con borde gradiente."""
    return ft.Container(
        content=ft.Container(
            content=content,
            padding=padding,
            border_radius=BORDER_RADIUS - 2,
            bgcolor=COLORS["surface"],
        ),
        padding=2,
        border_radius=BORDER_RADIUS,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[COLORS["primary"], COLORS["secondary"]],
        ),
    )


def crear_boton_primario(texto: str, on_click=None, icono: str = None, disabled: bool = False) -> ft.Container:
    """Crea un botón primario con efecto premium."""
    btn = ft.ElevatedButton(
        text=texto,
        icon=icono,
        on_click=on_click,
        disabled=disabled,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor={
                ft.ControlState.DEFAULT: COLORS["primary"],
                ft.ControlState.HOVERED: COLORS["primary_dark"],
                ft.ControlState.DISABLED: COLORS["surface_elevated"],
            },
            padding=ft.padding.symmetric(horizontal=28, vertical=14),
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS_SM),
            elevation={"pressed": 0, "": 4},
        ),
    )
    return btn


def crear_boton_secundario(texto: str, on_click=None, icono: str = None) -> ft.OutlinedButton:
    """Crea un botón secundario."""
    return ft.OutlinedButton(
        text=texto,
        icon=icono,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=COLORS["primary_light"],
            padding=ft.padding.symmetric(horizontal=28, vertical=14),
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS_SM),
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(color=COLORS["primary"], width=2),
                ft.ControlState.HOVERED: ft.BorderSide(color=COLORS["primary_light"], width=2),
            },
        ),
    )


def crear_boton_icon(icono: str, on_click=None, tooltip: str = None, color: str = "primary") -> ft.IconButton:
    """Crea un botón de icono."""
    return ft.IconButton(
        icon=icono,
        icon_color=COLORS[color],
        icon_size=22,
        tooltip=tooltip,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, COLORS[color]),
            },
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS_SM),
        ),
    )


def crear_titulo(texto: str, size: int = 24) -> ft.Text:
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


def crear_chip(texto: str, color: str = "primary", outlined: bool = False) -> ft.Container:
    """Crea un chip/badge premium."""
    bg_color = COLORS.get(color, COLORS["primary"])
    if outlined:
        return ft.Container(
            content=ft.Text(texto, size=11, weight=ft.FontWeight.W_500, color=bg_color),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=20,
            border=ft.border.all(1.5, bg_color),
            bgcolor=ft.Colors.with_opacity(0.1, bg_color),
        )
    return ft.Container(
        content=ft.Text(texto, size=11, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
        bgcolor=bg_color,
    )


def crear_stat_card(titulo: str, valor: str, icono, color: str = "primary", subtitulo: str = None) -> ft.Container:
    """Crea una tarjeta de estadística premium."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icono, size=22, color=COLORS[color]),
                            padding=10,
                            border_radius=BORDER_RADIUS_SM,
                            bgcolor=ft.Colors.with_opacity(0.15, COLORS[color]),
                        ),
                        ft.Container(expand=True),
                    ],
                ),
                ft.Container(height=12),
                ft.Text(valor, size=28, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                ft.Text(titulo, size=13, color=COLORS["text_secondary"]),
                ft.Text(subtitulo, size=11, color=COLORS["text_muted"]) if subtitulo else ft.Container(),
            ],
            spacing=2,
        ),
        padding=20,
        border_radius=BORDER_RADIUS,
        bgcolor=COLORS["surface"],
        border=ft.border.all(1, COLORS["border"]),
        width=180,
    )


def crear_switch_item(titulo: str, descripcion: str, valor: bool = False, on_change=None, data=None) -> ft.Container:
    """Crea un item con switch premium."""
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
                        ft.Text(descripcion, size=12, color=COLORS["text_secondary"]),
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
        margin=ft.margin.only(bottom=10),
    )


def crear_progreso_item(titulo: str, valor: float, color: str = "primary") -> ft.Container:
    """Crea un item con barra de progreso premium."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(titulo, size=14, color=COLORS["text"]),
                        ft.Text(f"{valor:.1f}%", size=14, weight=ft.FontWeight.BOLD, color=COLORS[color]),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.Container(
                        width=f"{valor}%",
                        height=10,
                        border_radius=5,
                        bgcolor=COLORS[color],
                    ),
                    width=float("inf"),
                    height=10,
                    border_radius=5,
                    bgcolor=COLORS["surface_elevated"],
                ),
            ],
            spacing=10,
        ),
        margin=ft.margin.only(bottom=16),
    )


def crear_list_tile(titulo: str, subtitulo: str = None, icono=None, trailing=None, on_click=None) -> ft.Container:
    """Crea un ListTile premium."""
    leading = None
    if icono:
        leading = ft.Container(
            content=ft.Icon(icono, size=22, color=COLORS["primary"]),
            padding=10,
            border_radius=BORDER_RADIUS_SM,
            bgcolor=ft.Colors.with_opacity(0.1, COLORS["primary"]),
        )

    return ft.Container(
        content=ft.Row(
            controls=[
                leading if leading else ft.Container(),
                ft.Column(
                    controls=[
                        ft.Text(titulo, size=14, weight=ft.FontWeight.W_500, color=COLORS["text"]),
                        ft.Text(subtitulo, size=12, color=COLORS["text_secondary"]) if subtitulo else ft.Container(),
                    ],
                    spacing=2,
                    expand=True,
                ),
                trailing if trailing else ft.Container(),
            ],
            spacing=16,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
        border_radius=BORDER_RADIUS_SM,
        bgcolor=COLORS["surface_light"],
        border=ft.border.all(1, COLORS["border"]),
        on_click=on_click,
        ink=True if on_click else False,
    )


def crear_seccion_header(titulo: str, subtitulo: str = None, accion=None) -> ft.Container:
    """Crea un header de sección."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
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
