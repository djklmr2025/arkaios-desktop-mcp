# ARKAIOS Desktop Senses (MCP Server) 👁️🎙️🖱️

[![MCP Protocol](https://img.shields.io/badge/Model%20Context%20Protocol-MCP-green)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Validado por](https://img.shields.io/badge/Validado%20por-Gemini%20Agent-orange)](#)

**ARKAIOS Desktop Senses** es un servidor local basado en el estándar **Model Context Protocol (MCP)**. Libera a los agentes de IA (como Copilot, Claude Desktop o agentes custom) de la "cárcel del navegador", dándoles acceso nativo y directo al hardware de tu computadora.

En lugar de leer código HTML web, este servidor le da a tu IA **sentidos físicos**: la capacidad de ver la pantalla, controlar el mouse, escuchar el micrófono y ver a través de tu cámara web.

## 🚀 Capacidades (Herramientas / Tools)

Este servidor expone las siguientes capacidades al modelo LLM:

*   👁️ **`screenshot`**: Toma una fotografía de los píxeles reales del monitor.
*   🎯 **`extract_ui`**: Escanea los botones y cajas de texto interactivas de la pantalla.
*   🖱️ **`click` & `type` & `hotkey`**: Control físico del mouse y teclado.
*   📷 **`webcam`**: Toma fotografías en tiempo real usando OpenCV.
*   🎙️ **`listen`**: Graba 5 segundos del micrófono local y lo transcribe a texto usando el motor de Google.

## 🧠 Arquitectura
A diferencia de soluciones basadas en web (Firebase/AI Studio) que requieren permisos constantes del navegador (`getUserMedia`) y no pueden operar en segundo plano, **ARKAIOS Desktop Senses** es un daemon de Python (FastAPI). 
Se ejecuta en el **Session 1** (espacio de usuario) de Windows, actuando como un puente IPC local para que los agentes que corren en el fondo (Session 0) puedan interactuar con la interfaz gráfica.

## ⚙️ Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/djklmr2025/arkaios-desktop-mcp.git
   cd arkaios-desktop-mcp
   ```
2. Crea tu entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Ejecuta el archivo **`Arrancar_Ojos_Antigravity.bat`**. Esto iniciará el servidor local en el puerto `8001`. (Debes dejar esta ventana abierta).

## 🔌 Integración con Otros Agentes (Copilot / Claude)

Para conectar este servidor a IAs comerciales que soportan MCP:
Ejecuta el instalador automático:
```bash
python install_addon.py
```
Esto modificará los archivos de configuración (`mcp.json` o `claude_desktop_config.json`) de tu IDE para inyectar este puente.

## 🤝 Contribuciones (Pull Requests)

¡Este es un proyecto open-source y la comunidad es bienvenida a mejorarlo! Si quieres añadir nuevos "sentidos" (por ejemplo, reconocimiento facial avanzado, integración con APIs externas, etc.):

1. Haz un **Fork** del proyecto.
2. Crea tu rama de características (`git checkout -b feature/NuevoSentido`).
3. Haz commit de tus cambios (`git commit -m 'Añadido nuevo sentido X'`).
4. Haz Push a la rama (`git push origin feature/NuevoSentido`).
5. Abre un **Pull Request**.

Cualquier PR que mejore la seguridad, la estabilidad o añada capacidades MCP interesantes será revisado y aprobado.

## ☕ Apoya el Proyecto (Donaciones)

Si este servidor MCP te ha ahorrado horas de desarrollo o le ha dado vida a tu agente de IA, considera apoyar el desarrollo continuo del proyecto ARKAIOS NeuralAgent. 
Las donaciones nos ayudan a mantener los servidores, pagar APIs y seguir creando código abierto de vanguardia:

*   [**Patreon / Buy me a Coffee**] *(Coloca aquí tu enlace cuando lo tengas)*
*   [**GitHub Sponsors**] *(Activa GitHub Sponsors en tu cuenta para recibir apoyos directo aquí)*

## 💬 Feedback y Pruebas

¿Lo probaste con Copilot? ¿Lo conectaste a Claude Desktop? ¡Queremos saber cómo te fue!
*   ⭐ **Deja una estrella (Star)** en este repositorio si te funcionó.
*   🐛 Si encuentras un bug (como que OpenCV no detecta tu cámara), abre un **Issue**.
*   💡 Si tienes ideas locas para nuevos superpoderes, déjanos un mensaje en la pestaña de **Discussions**.

---
*Desarrollado como parte del proyecto ARKAIOS NeuralAgent. Co-creado y validado en tiempo real por Gemini AI.*
