"""Tema y estilos de la aplicación."""
import flet as ft

# Colores principales
COLORS = {
    "primary": "#6366f1",      # Indigo
    "primary_dark": "#4f46e5",
    "secondary": "#10b981",    # Emerald
    "background": "#0f0f0f",   # Negro profundo
    "surface": "#1a1a1a",      # Gris oscuro
    "surface_light": "#262626",
    "text": "#ffffff",
    "text_secondary": "#a1a1aa",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
}

# Gradientes
GRADIENT_PRIMARY = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    colors=["#6366f1", "#8b5cf6"]
)

# Bordes redondeados
BORDER_RADIUS = 12
BORDER_RADIUS_SM = 8
BORDER_RADIUS_LG = 16

# Sombras
SHADOW = ft.BoxShadow(
    spread_radius=0,
    blur_radius=10,
    color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
    offset=ft.Offset(0, 4)
)


def crear_card(content: ft.Control, padding: int = 20) -> ft.Container:
    """Crea una tarjeta con estilo."""
    return ft.Container(
        content=content,
        padding=padding,
        border_radius=BORDER_RADIUS,
        bgcolor=COLORS["surface"],
        shadow=SHADOW,
    )


def crear_boton_primario(texto: str, on_click=None, icono: str = None, disabled: bool = False) -> ft.ElevatedButton:
    """Crea un botón primario."""
    return ft.ElevatedButton(
        text=texto,
        icon=icono,
        on_click=on_click,
        disabled=disabled,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor={
                ft.ControlState.DEFAULT: COLORS["primary"],
                ft.ControlState.HOVERED: COLORS["primary_dark"],
                ft.ControlState.DISABLED: ft.Colors.GREY_700,
            },
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS_SM),
        ),
    )


def crear_boton_secundario(texto: str, on_click=None, icono: str = None) -> ft.OutlinedButton:
    """Crea un botón secundario."""
    return ft.OutlinedButton(
        text=texto,
        icon=icono,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=COLORS["text"],
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS_SM),
            side=ft.BorderSide(color=COLORS["primary"], width=1),
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


def crear_chip(texto: str, color: str = "primary") -> ft.Container:
    """Crea un chip/badge."""
    bg_color = COLORS.get(color, COLORS["primary"])
    return ft.Container(
        content=ft.Text(texto, size=12, color=ft.Colors.WHITE),
        padding=ft.padding.symmetric(horizontal=12, vertical=4),
        border_radius=20,
        bgcolor=bg_color,
    )


def crear_switch_item(titulo: str, descripcion: str, valor: bool = False, on_change=None, data=None) -> ft.Container:
    """Crea un item con switch."""
    switch = ft.Switch(
        value=valor,
        on_change=on_change,
        active_color=COLORS["primary"],
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
                    spacing=2,
                    expand=True,
                ),
                switch,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border_radius=BORDER_RADIUS_SM,
        bgcolor=COLORS["surface_light"],
        margin=ft.margin.only(bottom=8),
    )


def crear_progreso_item(titulo: str, valor: float, color: str = "primary") -> ft.Container:
    """Crea un item con barra de progreso."""
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
                ft.ProgressBar(
                    value=valor / 100,
                    color=COLORS[color],
                    bgcolor=COLORS["surface_light"],
                    height=8,
                    border_radius=4,
                ),
            ],
            spacing=8,
        ),
        margin=ft.margin.only(bottom=16),
    )
