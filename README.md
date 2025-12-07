# Tecnodespegue Optimizer

**Optimizador de Windows 11 25H2 en Español**

Una herramienta completa y profesional para optimizar tu sistema Windows 11, eliminar bloatware, aplicar tweaks de rendimiento y gestionar servicios innecesarios.

![Windows](https://img.shields.io/badge/Windows-11%2025H2-0078D6.svg)
![Release](https://img.shields.io/badge/Release-v1.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Portable](https://img.shields.io/badge/Portable-EXE-orange.svg)

## Descarga

### Aplicacion Portable (Recomendado)

**No requiere instalacion de Python ni dependencias.**

1. Descarga `TecnodespegueOptimizer.exe` desde [Releases](https://github.com/Rene-Kuhm/tecnodespegue-optimizer/releases/latest)
2. Ejecuta como Administrador
3. Listo para optimizar!

## Caracteristicas

### Interfaz Profesional
- Diseno moderno estilo CleanMyMac X
- Splash screen animado
- Tema oscuro elegante
- Navegacion intuitiva con sidebar

### Dashboard Principal
- Informacion del sistema en tiempo real (CPU, RAM, Disco)
- Monitoreo de procesos con mayor consumo de recursos
- Perfiles de optimizacion rapida con un solo clic

### Tweaks del Sistema (22+)
- **Rendimiento**: Deshabilitar animaciones, Superfetch, indexacion
- **Privacidad**: Bloquear telemetria, Cortana, historial de actividad
- **Interfaz**: Menu contextual clasico, deshabilitar Widgets/Copilot
- **Energia**: Plan de energia Ultimate Performance
- **Red**: Optimizar configuracion de red y DNS
- **Almacenamiento**: Deshabilitar hibernacion, compresion NTFS

### Eliminacion de Bloatware (47+ apps detectables)
- Aplicaciones preinstaladas de Microsoft
- Juegos innecesarios (Candy Crush, Solitaire, etc.)
- Apps de terceros (Spotify, TikTok, Instagram, Facebook, etc.)
- Eliminacion segura con PowerShell

### Limpieza del Sistema
- Archivos temporales de usuario y sistema
- Cache de Windows Update
- Prefetch y miniaturas
- Logs de Windows
- Papelera de reciclaje

### Gestion de Servicios
- Lista de servicios que se pueden deshabilitar de forma segura
- Acciones rapidas para telemetria, Xbox, Hyper-V
- Informacion detallada de cada servicio

### Actualizacion de Drivers
- Escaneo de drivers instalados
- Deteccion de drivers desactualizados
- Actualizacion automatica

### 5 Perfiles de Optimizacion
| Perfil | Descripcion |
|--------|-------------|
| **Minimo** | Cambios seguros, sin riesgo |
| **Recomendado** | Balance entre rendimiento y funcionalidad |
| **Maximo** | Optimizacion agresiva para maximo rendimiento |
| **Gaming** | Optimizado para juegos y baja latencia |
| **Productividad** | Ideal para trabajo y multitarea |

## Requisitos

- Windows 11 (25H2 recomendado)
- Permisos de administrador (para todas las funciones)

## Instalacion

### Opcion 1: Aplicacion Portable (Recomendado)

1. Descarga `TecnodespegueOptimizer.exe` desde [Releases](https://github.com/Rene-Kuhm/tecnodespegue-optimizer/releases/latest)
2. Click derecho > "Ejecutar como administrador"
3. Listo!

### Opcion 2: Desde el codigo fuente

Si prefieres ejecutar desde el codigo fuente:

```bash
# Clonar repositorio
git clone https://github.com/Rene-Kuhm/tecnodespegue-optimizer.git
cd tecnodespegue-optimizer

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

## Uso

1. **Ejecutar como Administrador**: Para aplicar la mayoria de las optimizaciones, la aplicacion necesita permisos de administrador.

2. **Escanear**: En el Dashboard, haz clic en el boton de escaneo para analizar tu sistema.

3. **Seleccionar un perfil**: Elige uno de los 5 perfiles segun tus necesidades.

4. **Personalizar**: Usa las secciones de Tweaks, Bloatware y Servicios para ajustar configuraciones especificas.

5. **Limpiar**: Ejecuta una limpieza del sistema para liberar espacio en disco.

## Capturas de Pantalla

La aplicacion cuenta con una interfaz moderna y oscura estilo CleanMyMac X, disenada para ser intuitiva y facil de usar.

## Advertencias

- Siempre crea un punto de restauracion antes de aplicar optimizaciones agresivas
- Algunos tweaks pueden requerir reinicio del sistema
- La eliminacion de bloatware es permanente (aunque se pueden reinstalar desde la Microsoft Store)

## Tecnologias

- **Python 3.10+**: Lenguaje de programacion
- **Flet**: Framework de UI moderno
- **PyInstaller**: Empaquetado portable
- **PowerShell**: Para comandos del sistema
- **psutil**: Monitoreo de recursos del sistema

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaria hacer.

## Licencia

Este proyecto esta bajo la Licencia MIT. Ver el archivo `LICENSE` para mas detalles.

## Autor

Desarrollado por **Tecnodespegue**

---

**Nota**: Este software modifica configuraciones del sistema. Usalo bajo tu propia responsabilidad. Se recomienda crear un punto de restauracion del sistema antes de aplicar cualquier optimizacion.
