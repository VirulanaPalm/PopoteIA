"""
Interfaz visual de POPOTE: la "cara".

Dibuja ojos y boca sobre un Canvas de tkinter y los anima a 60 FPS.
El color (rosa) se ilumina o se atenúa según el estado (escuchando /
pensando / normal), y la boca se abre y cierra en sincronía con el TTS.
"""

import math
import random
import tkinter as tk

ANCHO_VENTANA = 600
ALTO_VENTANA = 450

RGB_ROSA_BASE = (255, 85, 204)

# Multiplicadores de brillo por estado
BRILLO_ESCUCHANDO = 1.35
BRILLO_PENSANDO = 0.55
BRILLO_NORMAL = 1.0

VELOCIDAD_LERP_BRILLO = 0.1
VELOCIDAD_LERP_BOCA = 0.3
VELOCIDAD_LERP_OJOS = 0.4
VELOCIDAD_ANIMACION_BOCA = 0.4

RADIO_MAXIMO_OJO = 60
ALTURA_MAXIMA_OJO = 80
ALTURA_MINIMA_OJO = 3

FPS_MS = 16  # ~60 FPS

# Coordenadas base de ojos y boca
X1_OJO_IZQ, X2_OJO_IZQ = 100, 260
X1_OJO_DER, X2_OJO_DER = 340, 500
Y_CENTRO_OJOS = 160

X1_BOCA_BASE, X2_BOCA_BASE, Y_BOCA = 260, 340, 330
ANCHO_BOCA_BASE = 30
ANCHO_BOCA_EXTRA = 15
DESPLAZAMIENTO_BOCA_MAX = 40

PARPADEO_MS_MIN = 2000
PARPADEO_MS_MAX = 5000
DURACION_PARPADEO_MS = 120


class CaraPopote:
    def __init__(self, root):
        self.root = root
        self.root.title("POPOTE - Interfaz Visual")
        self.root.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.root.configure(bg="white")

        self.canvas = tk.Canvas(
            root, width=ANCHO_VENTANA, height=ALTO_VENTANA, bg="white", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.rgb_rosa = RGB_ROSA_BASE

        # Sistema de brillo suave (multiplicador)
        self.brillo_actual = BRILLO_NORMAL
        self.brillo_objetivo = BRILLO_NORMAL

        hex_inicial = self._calcular_color_con_brillo()

        # Ojos y boca
        self.ojo_izq = self.canvas.create_polygon([0, 0, 0, 0], fill=hex_inicial, outline="", smooth=True)
        self.ojo_der = self.canvas.create_polygon([0, 0, 0, 0], fill=hex_inicial, outline="", smooth=True)
        self.boca = self.canvas.create_line(
            X1_BOCA_BASE, Y_BOCA, X2_BOCA_BASE, Y_BOCA,
            fill=hex_inicial, width=ANCHO_BOCA_BASE, capstyle=tk.ROUND,
        )

        # Variables de animación
        self.hablando = False
        self.fase_boca = 0.0
        self.apertura_boca = 0.0
        self.apertura_ojos = 1.0
        self.objetivo_ojos = 1.0

        self._iniciar_parpadeo_aleatorio()
        self._loop_animacion()

    def _calcular_color_con_brillo(self) -> str:
        """Multiplica el rosa base por el brillo actual y lo pasa a HEX."""
        rgb_calculado = [min(255, max(0, c * self.brillo_actual)) for c in self.rgb_rosa]
        return f"#{int(rgb_calculado[0]):02x}{int(rgb_calculado[1]):02x}{int(rgb_calculado[2]):02x}"

    def _actualizar_cuadrado_redondeado(self, id_figura, x1, y1, x2, y2, radio_maximo=RADIO_MAXIMO_OJO):
        radio = min(radio_maximo, (y2 - y1) / 2, (x2 - x1) / 2)
        if radio < 0:
            radio = 0

        puntos = [
            x1 + radio, y1, x2 - radio, y1, x2, y1, x2, y1 + radio,
            x2, y2 - radio, x2, y2, x2 - radio, y2, x1 + radio, y2,
            x1, y2, x1, y2 - radio, x1, y1 + radio, x1, y1,
        ]
        self.canvas.coords(id_figura, *puntos)

    def _iniciar_parpadeo_aleatorio(self):
        self.objetivo_ojos = 0.0
        self.root.after(DURACION_PARPADEO_MS, self._abrir_ojos)

        tiempo_random = random.randint(PARPADEO_MS_MIN, PARPADEO_MS_MAX)
        self.root.after(tiempo_random, self._iniciar_parpadeo_aleatorio)

    def _abrir_ojos(self):
        self.objetivo_ojos = 1.0

    def iniciar_habla(self):
        self.hablando = True

    def detener_habla(self):
        self.hablando = False

    # --- CONTROL DE BRILLO POR ESTADO ---
    def estado_escuchando(self):
        """Se ilumina suavemente hacia arriba."""
        self.brillo_objetivo = BRILLO_ESCUCHANDO

    def estado_pensando(self):
        """Se atenúa suavemente hacia abajo."""
        self.brillo_objetivo = BRILLO_PENSANDO

    def estado_normal(self):
        """Vuelve al brillo original."""
        self.brillo_objetivo = BRILLO_NORMAL

    # --- MOTOR MAESTRO DE ANIMACIÓN (~60 FPS) ---
    def _loop_animacion(self):
        # 0. Transición suave de brillo (LERP)
        self.brillo_actual += (self.brillo_objetivo - self.brillo_actual) * VELOCIDAD_LERP_BRILLO
        color_hex = self._calcular_color_con_brillo()

        self.canvas.itemconfig(self.ojo_izq, fill=color_hex)
        self.canvas.itemconfig(self.ojo_der, fill=color_hex)
        self.canvas.itemconfig(self.boca, fill=color_hex)

        # 1. Animación de la boca
        if self.hablando:
            self.fase_boca += VELOCIDAD_ANIMACION_BOCA
            objetivo_boca = (math.sin(self.fase_boca) + 1) / 2
        else:
            self.fase_boca = 0.0
            objetivo_boca = 0.0

        self.apertura_boca += (objetivo_boca - self.apertura_boca) * VELOCIDAD_LERP_BOCA

        dx = DESPLAZAMIENTO_BOCA_MAX * self.apertura_boca
        x1_boca = X1_BOCA_BASE + dx
        x2_boca = X2_BOCA_BASE - dx
        ancho_boca = ANCHO_BOCA_BASE + (ANCHO_BOCA_EXTRA * self.apertura_boca)

        self.canvas.coords(self.boca, x1_boca, Y_BOCA, x2_boca, Y_BOCA)
        self.canvas.itemconfig(self.boca, width=ancho_boca)

        # 2. Animación de los ojos
        self.apertura_ojos += (self.objetivo_ojos - self.apertura_ojos) * VELOCIDAD_LERP_OJOS
        altura_actual = ALTURA_MAXIMA_OJO * self.apertura_ojos
        if altura_actual < ALTURA_MINIMA_OJO:
            altura_actual = ALTURA_MINIMA_OJO

        y1_ojo = Y_CENTRO_OJOS - altura_actual
        y2_ojo = Y_CENTRO_OJOS + altura_actual

        self._actualizar_cuadrado_redondeado(self.ojo_izq, X1_OJO_IZQ, y1_ojo, X2_OJO_IZQ, y2_ojo)
        self._actualizar_cuadrado_redondeado(self.ojo_der, X1_OJO_DER, y1_ojo, X2_OJO_DER, y2_ojo)

        self.root.after(FPS_MS, self._loop_animacion)
