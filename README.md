# Tecnodespegue Optimizer

**Optimizador de Windows 11 25H2 en Español**

Una herramienta completa y profesional para optimizar tu sistema Windows 11, eliminar bloatware, aplicar tweaks de rendimiento y gestionar servicios innecesarios.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-0.21+-green.svg)
![Windows](https://img.shields.io/badge/Windows-11%2025H2-0078D6.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Características

### Dashboard Principal
- Información del sistema en tiempo real (CPU, RAM, Disco)
- Monitoreo de procesos con mayor consumo de recursos
- Perfiles de optimización rápida con un solo clic

### Tweaks del Sistema (22+)
- **Rendimiento**: Deshabilitar animaciones, Superfetch, indexación
- **Privacidad**: Bloquear telemetría, Cortana, historial de actividad
- **Interfaz**: Limpiar menú contextual, deshabilitar transparencias
- **Energía**: Optimizar plan de energía para máximo rendimiento
- **Red**: Optimizar configuración de red y DNS
- **Almacenamiento**: Deshabilitar hibernación, compresión NTFS

### Eliminación de Bloatware (40+ apps)
- Aplicaciones preinstaladas de Microsoft
- Juegos innecesarios (Candy Crush, Solitaire, etc.)
- Apps de terceros que vienen con Windows
- Eliminación segura con PowerShell

### Limpieza del Sistema
- Archivos temporales de usuario y sistema
- Caché de Windows Update
- Prefetch y miniaturas
- Logs de Windows
- Papelera de reciclaje

### Gestión de Servicios
- Lista de servicios que se pueden deshabilitar de forma segura
- Acciones rápidas para telemetría, Xbox, Hyper-V
- Información detallada de cada servicio

### 5 Perfiles de Optimización
| Perfil | Descripción |
|--------|-------------|
| **Mínimo** | Cambios seguros, sin riesgo |
| **Recomendado** | Balance entre rendimiento y funcionalidad |
| **Máximo** | Optimización agresiva para máximo rendimiento |
| **Gaming** | Optimizado para juegos y baja latencia |
| **Productividad** | Ideal para trabajo y multitarea |

## Requisitos

- Windows 11 (25H2 recomendado)
- Python 3.10 o superior
- Permisos de administrador (recomendado)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Rene-Kuhm/tecnodespegue-optimizer.git
cd tecnodespegue-optimizer
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
python main.py
```

## Uso

1. **Ejecutar como Administrador**: Para aplicar la mayoría de las optimizaciones, la aplicación necesita permisos de administrador.

2. **Seleccionar un perfil**: En el Dashboard, elige uno de los 5 perfiles según tus necesidades.

3. **Personalizar**: Usa las secciones de Tweaks, Bloatware y Servicios para ajustar configuraciones específicas.

4. **Limpiar**: Ejecuta una limpieza del sistema para liberar espacio en disco.

## Capturas de Pantalla

La aplicación cuenta con una interfaz moderna y oscura, diseñada para ser intuitiva y fácil de usar.

## Advertencias

- Siempre crea un punto de restauración antes de aplicar optimizaciones agresivas
- Algunos tweaks pueden requerir reinicio del sistema
- La eliminación de bloatware es permanente (aunque se pueden reinstalar desde la Microsoft Store)

## Tecnologías

- **Python 3.10+**: Lenguaje de programación
- **Flet**: Framework de UI moderno
- **PowerShell**: Para comandos del sistema
- **psutil**: Monitoreo de recursos del sistema

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor

Desarrollado por **Tecnodespegue**

---

**Nota**: Este software modifica configuraciones del sistema. Úsalo bajo tu propia responsabilidad. Se recomienda crear un punto de restauración del sistema antes de aplicar cualquier optimización.
