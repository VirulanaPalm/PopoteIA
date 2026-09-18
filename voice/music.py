import os
import sys
import subprocess
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pythoncom

RUTA_AUDIO = os.path.abspath("audio_temp.mp3")
BUSQUEDA_POR_DEFECTO = "Skrillex Bangarang"
TIMEOUT_DESCARGA_SEGUNDOS = 60

# Palabras que se sacan del pedido de Agus para quedarnos solo con el nombre del tema.
PALABRAS_A_SACAR = (
    "reproducir", "reproducirla", "ponete", "poné", "música",
    "un tema de", "tema de", "el tema", "por favor",
    "quiero escuchar", "escuchar",
    "hola popote", "hola", "popote",
)

_proceso_musica = None

def _limpiar_busqueda(comando_usuario: str) -> str:
    busqueda = comando_usuario.lower()
    for palabra in PALABRAS_A_SACAR:
        busqueda = busqueda.replace(palabra, "")
    busqueda = " ".join(busqueda.split())
    return busqueda.strip()

def reproducir_musica(comando_usuario: str) -> str:
    """Busca el tema en YouTube, descarga el audio y lo reproduce localmente."""
    global _proceso_musica

    busqueda = _limpiar_busqueda(comando_usuario)
    if not busqueda or len(busqueda) < 2:
        busqueda = BUSQUEDA_POR_DEFECTO

    print(f"[DJ POPOTE] Descargando '{busqueda}' para reproducir localmente...")

    detener_musica()

    if os.path.exists(RUTA_AUDIO):
        try:
            os.remove(RUTA_AUDIO)
        except Exception:
            pass

    try:
        salida_sin_ext = RUTA_AUDIO.replace(".mp3", "")
        
        # EL TRUCO MAGICO: Llamar a yt-dlp como módulo de Python (sys.executable -m yt_dlp)
        comando = [
            sys.executable, "-m", "yt_dlp",
            f"ytsearch1:{busqueda} official audio",
            "-x", "--audio-format", "mp3",
            "-o", f"{salida_sin_ext}.%(ext)s",
            "--no-warnings",
        ]

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_DESCARGA_SEGUNDOS,
        )

        # Si falla, imprimimos TODO el error real en la consola
        if resultado.returncode != 0:
            error_real = resultado.stderr if resultado.stderr else resultado.stdout
            print(f"\n[YT-DLP ERROR DETALLADO]:\n{error_real}\n")

        if os.path.exists(RUTA_AUDIO) and os.path.getsize(RUTA_AUDIO) > 0:
            _proceso_musica = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", RUTA_AUDIO],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return f"Reproduciendo {busqueda}, hermano. ¡A disfrutar!"

        return (
            f"No pude descargar '{busqueda}'. Revisá la consola para ver el error exacto."
        )

    except subprocess.TimeoutExpired:
        return "La descarga tardó demasiado, probemos con otro tema."
    except Exception as e:
        return f"Se me cruzaron los cables con la música: {e}"


def detener_musica() -> None:
    """Corta la reproducción actual, si hay algo sonando."""
    global _proceso_musica
    if _proceso_musica is not None and _proceso_musica.poll() is None:
        _proceso_musica.terminate()
        _proceso_musica.wait(timeout=2)
    _proceso_musica = None


def atenuar_musica():
    """Baja el volumen de la música (ffplay.exe) al 15%."""
    try:
        pythoncom.CoInitialize()
        sesiones = AudioUtilities.GetAllSessions()
        for sesion in sesiones:
            if sesion.Process and sesion.Process.name() == "ffplay.exe":
                volumen = sesion._ctl.QueryInterface(ISimpleAudioVolume)
                volumen.SetMasterVolume(0.15, None)
    except:
        pass


def normalizar_musica():
    """Sube el volumen de la música (ffplay.exe) de vuelta al 100%."""
    try:
        pythoncom.CoInitialize()
        sesiones = AudioUtilities.GetAllSessions()
        for sesion in sesiones:
            if sesion.Process and sesion.Process.name() == "ffplay.exe":
                volumen = sesion._ctl.QueryInterface(ISimpleAudioVolume)
                volumen.SetMasterVolume(1.0, None)
    except:
        pass


def cambiar_volumen(nivel: float) -> str:
    """Cambia el volumen fijo de la música de forma manual (0.0 a 1.0)."""
    try:
        pythoncom.CoInitialize()
        sesiones = AudioUtilities.GetAllSessions()
        cambiado = False
        for sesion in sesiones:
            if sesion.Process and sesion.Process.name() == "ffplay.exe":
                volumen = sesion._ctl.QueryInterface(ISimpleAudioVolume)
                volumen.SetMasterVolume(nivel, None)
                cambiado = True
        
        if cambiado:
            porcentaje = int(nivel * 100)
            return f"Listo el pollo, volumen al {porcentaje} por ciento."
        else:
            return "No hay música sonando para cambiarle el volumen."
    except Exception as e:
        return f"Me falló la perilla del volumen: {e}"