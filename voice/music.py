import os
import sys
import subprocess
import random
import glob
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pythoncom

TIMEOUT_DESCARGA_SEGUNDOS = 30

BUSQUEDAS_ALEATORIAS = [
    "Skrillex Bangarang",
    "Chacarera santiagueña mix",
    "Canciones de Boca Juniors La 12",
    "Fallout 4 Diamond City Radio",
    "Música electrónica para programar",
    "Rock nacional argentino clásicos"
]

PALABRAS_A_SACAR = (
    "reproducir", "reproducirla", "reproducí", "reproduci",
    "producir", "producí",
    "ponete", "poné", "pone", "poneme", "pon", 
    "algo de", "algo", "música", "musica", "canción", "cancion",
    "un tema de", "tema de", "el tema", "por favor",
    "quiero escuchar", "escuchar", "buscá", "busca", 
    "dale play a", "dale play", "tocá", "toca", 
    "mandale", "mandá", "arranca con", "arrancá con", "hacé sonar", "hace sonar",
    "hola popote", "hola", "popote", "che",
)

_proceso_musica = None
# CLAVE: Arranca bajito (15%) para que puedas interrumpirlo fácil.
_volumen_actual = 0.15  

def _limpiar_busqueda(comando_usuario: str) -> str:
    busqueda = comando_usuario.lower()
    for palabra in PALABRAS_A_SACAR:
        busqueda = busqueda.replace(palabra, "")
    return " ".join(busqueda.split()).strip()

def reproducir_musica(comando_usuario: str) -> str:
    global _proceso_musica, _volumen_actual

    busqueda = _limpiar_busqueda(comando_usuario)
    if not busqueda or len(busqueda) < 2:
        busqueda = random.choice(BUSQUEDAS_ALEATORIAS)

    print(f"[DJ POPOTE] Buscando '{busqueda}' de forma ultrarrápida...")
    detener_musica()

    for archivo_viejo in glob.glob("audio_temp.*"):
        try:
            os.remove(archivo_viejo)
        except Exception:
            pass

    try:
        comando = [
            sys.executable, "-m", "yt_dlp",
            f"ytsearch1:{busqueda}",
            "-f", "bestaudio",
            "-o", "audio_temp.%(ext)s",
            "--no-warnings",
        ]

        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=TIMEOUT_DESCARGA_SEGUNDOS)
        archivos_descargados = glob.glob("audio_temp.*")

        if archivos_descargados:
            ruta_final = os.path.abspath(archivos_descargados[0])
            _proceso_musica = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "-volume", str(int(_volumen_actual * 100)), ruta_final],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            cambiar_volumen(_volumen_actual)
            return f"Dale, ahí te pongo {busqueda}."
        else:
            return f"No pude encontrar '{busqueda}'. Revisá la consola."

    except subprocess.TimeoutExpired:
        return "Tardó demasiado, probemos con otro tema."
    except Exception as e:
        return f"Se me cruzaron los cables con la música: {e}"

def detener_musica() -> None:
    global _proceso_musica
    if _proceso_musica is not None and _proceso_musica.poll() is None:
        _proceso_musica.terminate()
        _proceso_musica.wait(timeout=2)
    _proceso_musica = None

def atenuar_musica():
    try:
        pythoncom.CoInitialize()
        for sesion in AudioUtilities.GetAllSessions():
            if sesion.Process and sesion.Process.name() == "ffplay.exe":
                volumen = sesion._ctl.QueryInterface(ISimpleAudioVolume)
                volumen.SetMasterVolume(0.05, None) # Atenuación casi muda
    except:
        pass

def normalizar_musica():
    global _volumen_actual
    try:
        pythoncom.CoInitialize()
        for sesion in AudioUtilities.GetAllSessions():
            if sesion.Process and sesion.Process.name() == "ffplay.exe":
                volumen = sesion._ctl.QueryInterface(ISimpleAudioVolume)
                volumen.SetMasterVolume(_volumen_actual, None)
    except:
        pass

def cambiar_volumen(nivel: float) -> str:
    global _volumen_actual
    try:
        pythoncom.CoInitialize()
        cambiado = False
        for sesion in AudioUtilities.GetAllSessions():
            if sesion.Process and sesion.Process.name() == "ffplay.exe":
                volumen = sesion._ctl.QueryInterface(ISimpleAudioVolume)
                volumen.SetMasterVolume(nivel, None)
                cambiado = True
        
        if cambiado:
            _volumen_actual = nivel 
            porcentaje = int(nivel * 100)
            return f"Listo el pollo, volumen al {porcentaje} por ciento."
        else:
            return "No hay música sonando para cambiarle el volumen."
    except Exception as e:
        return f"Me falló la perilla del volumen: {e}"