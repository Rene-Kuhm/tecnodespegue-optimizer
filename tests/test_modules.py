"""Tests automatizados para Tecnodespegue Optimizer."""
import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestImports(unittest.TestCase):
    """Tests de importación de módulos."""

    def test_import_theme(self):
        """Verifica que el tema se importe correctamente."""
        from src.ui import theme
        self.assertIsNotNone(theme.COLORS)
        self.assertIn("background", theme.COLORS)
        self.assertIn("primary", theme.COLORS)
        self.assertIn("scan_blue", theme.COLORS)

    def test_import_admin_utils(self):
        """Verifica que las utilidades de admin se importen."""
        from src.utils.admin import es_administrador, ejecutar_powershell, ejecutar_cmd
        self.assertTrue(callable(es_administrador))
        self.assertTrue(callable(ejecutar_powershell))
        self.assertTrue(callable(ejecutar_cmd))

    def test_import_system_info(self):
        """Verifica que system_info se importe correctamente."""
        from src.utils.system_info import obtener_info_sistema, InfoSistema
        self.assertTrue(callable(obtener_info_sistema))

    def test_import_pages(self):
        """Verifica que todas las páginas se importen."""
        from src.ui.pages.inicio import PaginaInicio
        from src.ui.pages.tweaks import PaginaTweaks
        from src.ui.pages.bloatware import PaginaBloatware
        from src.ui.pages.limpieza import PaginaLimpieza
        from src.ui.pages.servicios import PaginaServicios
        from src.ui.pages.drivers import PaginaDrivers
        self.assertTrue(True)

    def test_import_modules(self):
        """Verifica que todos los módulos de funcionalidad se importen."""
        from src.modules.tweaks import TWEAKS_DISPONIBLES
        from src.modules.bloatware import BLOATWARE_APPS
        from src.modules.limpieza import ejecutar_limpieza_completa
        from src.modules.servicios import SERVICIOS_DESHABILITABLES
        from src.modules.drivers import escanear_drivers
        from src.modules.perfiles import PERFILES, NivelPerfil
        self.assertTrue(True)


class TestTheme(unittest.TestCase):
    """Tests del tema de la aplicación."""

    def test_colors_complete(self):
        """Verifica que todos los colores necesarios estén definidos."""
        from src.ui import theme
        required_colors = [
            "background", "sidebar", "surface", "primary",
            "text", "text_secondary", "text_muted",
            "success", "warning", "error", "info",
            "border", "scan_blue", "scan_purple",
            "clean_green", "protect_red", "speed_orange"
        ]
        for color in required_colors:
            self.assertIn(color, theme.COLORS, f"Color '{color}' no encontrado")

    def test_gradients_defined(self):
        """Verifica que los gradientes estén definidos."""
        from src.ui import theme
        required_gradients = [
            "gradient_scan", "gradient_clean", "gradient_protect",
            "gradient_speed", "gradient_primary"
        ]
        for grad in required_gradients:
            self.assertIn(grad, theme.COLORS, f"Gradiente '{grad}' no encontrado")
            self.assertIsInstance(theme.COLORS[grad], list)
            self.assertEqual(len(theme.COLORS[grad]), 2)


class TestSystemInfo(unittest.TestCase):
    """Tests de información del sistema."""

    def test_obtener_info_sistema(self):
        """Verifica que se pueda obtener info del sistema."""
        from src.utils.system_info import obtener_info_sistema
        info = obtener_info_sistema()
        self.assertIsNotNone(info)
        self.assertIsNotNone(info.nombre_pc)
        self.assertIsNotNone(info.build)
        self.assertGreater(info.ram_total_gb, 0)
        self.assertGreater(info.disco_total_gb, 0)
        self.assertGreaterEqual(info.nucleos, 1)


class TestBloatware(unittest.TestCase):
    """Tests del módulo de bloatware."""

    def test_bloatware_list_not_empty(self):
        """Verifica que la lista de bloatware no esté vacía."""
        from src.modules.bloatware import BLOATWARE_APPS
        self.assertGreater(len(BLOATWARE_APPS), 0)

    def test_bloatware_has_required_fields(self):
        """Verifica que cada app tenga los campos requeridos."""
        from src.modules.bloatware import BLOATWARE_APPS
        for app in BLOATWARE_APPS:
            self.assertIsNotNone(app.nombre)
            self.assertIsNotNone(app.paquete)
            self.assertIsNotNone(app.descripcion)
            self.assertIsNotNone(app.categoria)


class TestTweaks(unittest.TestCase):
    """Tests del módulo de tweaks."""

    def test_tweaks_list_not_empty(self):
        """Verifica que la lista de tweaks no esté vacía."""
        from src.modules.tweaks import TWEAKS_DISPONIBLES
        self.assertGreater(len(TWEAKS_DISPONIBLES), 0)

    def test_tweaks_have_required_fields(self):
        """Verifica que cada tweak tenga los campos requeridos."""
        from src.modules.tweaks import TWEAKS_DISPONIBLES
        for tweak in TWEAKS_DISPONIBLES:
            self.assertIsNotNone(tweak.nombre)
            self.assertIsNotNone(tweak.descripcion)
            self.assertIsNotNone(tweak.categoria)
            self.assertIsNotNone(tweak.riesgo)


class TestServicios(unittest.TestCase):
    """Tests del módulo de servicios."""

    def test_servicios_list_not_empty(self):
        """Verifica que la lista de servicios no esté vacía."""
        from src.modules.servicios import SERVICIOS_DESHABILITABLES
        self.assertGreater(len(SERVICIOS_DESHABILITABLES), 0)

    def test_servicios_have_required_fields(self):
        """Verifica que cada servicio tenga los campos requeridos."""
        from src.modules.servicios import SERVICIOS_DESHABILITABLES
        for nombre, datos in SERVICIOS_DESHABILITABLES.items():
            self.assertIsNotNone(nombre)
            self.assertIsInstance(nombre, str)
            self.assertIsInstance(datos, tuple)
            self.assertEqual(len(datos), 2)  # (descripcion, recomendacion)


class TestLimpieza(unittest.TestCase):
    """Tests del módulo de limpieza."""

    def test_funciones_limpieza_exist(self):
        """Verifica que las funciones de limpieza existan."""
        from src.modules.limpieza import (
            limpiar_temp_usuario, limpiar_temp_windows, limpiar_prefetch,
            limpiar_cache_windows_update, limpiar_thumbnails,
            limpiar_logs_windows, limpiar_papelera, ejecutar_limpieza_completa
        )
        self.assertTrue(callable(limpiar_temp_usuario))
        self.assertTrue(callable(ejecutar_limpieza_completa))


class TestPerfiles(unittest.TestCase):
    """Tests del módulo de perfiles."""

    def test_perfiles_exist(self):
        """Verifica que los perfiles existan."""
        from src.modules.perfiles import PERFILES, NivelPerfil
        self.assertIn(NivelPerfil.MINIMO, PERFILES)
        self.assertIn(NivelPerfil.RECOMENDADO, PERFILES)
        self.assertIn(NivelPerfil.MAXIMO, PERFILES)
        self.assertIn(NivelPerfil.GAMING, PERFILES)

    def test_perfiles_have_required_fields(self):
        """Verifica que cada perfil tenga los campos requeridos."""
        from src.modules.perfiles import PERFILES
        for nivel, perfil in PERFILES.items():
            self.assertIsNotNone(perfil.nombre)
            self.assertIsNotNone(perfil.descripcion)


class TestDrivers(unittest.TestCase):
    """Tests del módulo de drivers."""

    def test_funciones_drivers_exist(self):
        """Verifica que las funciones de drivers existan."""
        from src.modules.drivers import escanear_drivers, actualizar_todos_drivers
        self.assertTrue(callable(escanear_drivers))
        self.assertTrue(callable(actualizar_todos_drivers))


class TestAdminUtils(unittest.TestCase):
    """Tests de utilidades de administrador."""

    def test_es_administrador_returns_bool(self):
        """Verifica que es_administrador retorne un booleano."""
        from src.utils.admin import es_administrador
        result = es_administrador()
        self.assertIsInstance(result, bool)

    def test_ejecutar_powershell_returns_tuple(self):
        """Verifica que ejecutar_powershell retorne una tupla."""
        from src.utils.admin import ejecutar_powershell
        exito, salida = ejecutar_powershell("Write-Output 'test'")
        self.assertIsInstance(exito, bool)
        self.assertIsInstance(salida, str)

    def test_ejecutar_cmd_returns_tuple(self):
        """Verifica que ejecutar_cmd retorne una tupla."""
        from src.utils.admin import ejecutar_cmd
        exito, salida = ejecutar_cmd("echo test")
        self.assertIsInstance(exito, bool)
        self.assertIsInstance(salida, str)


if __name__ == "__main__":
    # Ejecutar tests con verbosidad
    unittest.main(verbosity=2)
