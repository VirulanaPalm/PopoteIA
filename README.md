# POPOTE'S

Cerebro de un futuro robot con IA conversacional, personalidad propia y,
a futuro, cuerpo físico (sensores, motores, cámara). Este repo es el
cerebro corriendo en modo **simulación/desktop** (Windows).

## Estructura

```
main.py              → loop principal: hilo de IA + interfaz gráfica (tkinter)
pantallita.py         → cara de Popote (ojos, boca, brillo por estado)
brain/core.py         → conversación general vía Groq
voice/listener.py     → escucha (STT, Google, es-AR)
voice/speaker.py      → habla (TTS, PowerShell/System.Speech)
voice/music.py        → DJ local (yt-dlp + ffplay)
capabilities/         → Capability Registry (inventario de qué puede hacer Popote)
config/               → configuración y capabilities.json
tests/                → scripts de prueba manual (no son tests automatizados)
actions, sensors, vision, personality, hardware, utils, memory/
                      → carpetas reservadas para capacidades futuras
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Además necesitás, instalados en el sistema y en el PATH (no son paquetes de pip):
- **ffmpeg** y **ffplay** (para `voice/music.py`)
- Un micrófono reconocido por Windows (para `voice/listener.py`)

Creá un archivo `.env` en la raíz con:

```
GROQ_API_KEY=tu_api_key_de_groq
```

## Correr Popote

```bash
python main.py
```

Decile "apagar sistema" o "andate a dormir" para cerrarlo prolijo.

## Nota sobre el TTS

Hay dos sistemas de síntesis de voz en el repo:

- **`voice/speaker.py`** → el que realmente usa `main.py` (PowerShell / System.Speech de Windows). Es el oficial.
- **`edge_tts` + `playsound`** (en `tests/test_edge.py` y `tests/test_speaker.py`) → una alternativa que se probó pero **no está integrada** a `main.py`. Queda como prueba, por si en algún momento se decide migrar a esa voz.

## Capability Registry

`capabilities/registry.py` guarda en `config/capabilities.json` el
inventario de las capacidades del sistema (nombre, estado, riesgo,
dependencias, archivos). Por ahora es solo informativo: no cambia cómo
corre `main.py`. Para (re)generarlo con las capacidades base:

```bash
python capabilities/registry.py
```

Es la base de la Fase 1 del *Self Development Engine* descripto en el
documento maestro del proyecto.
