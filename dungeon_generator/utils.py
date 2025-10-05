from dungeon_generator.visual import Visualizador
import random
import os

# Utilidades para el main.py
def limpiar_pantalla():
	try:
		if os.name == "nt":
			os.system("cls")
		else:
			os.system("clear")
	except Exception:
		pass

def pedir_entero(mensaje, por_defecto):
	s = input(f"{mensaje} [{por_defecto}]: ").strip()
	if s == "":
		return por_defecto
	try:
		return int(s)
	except Exception:
		print("Valor inválido. Usando por defecto.")
		return por_defecto

def obtener_tipo_contenido(hab):
	if hab is None or hab.contenido is None:
		return "nada"
	t = getattr(hab.contenido, "tipo", None)
	if t == "tesoro":
		try:
			return getattr(hab.contenido.objeto, "nombre", "tesoro")
		except Exception:
			return "tesoro"
	if t == "monstruo":
		return f"Monstruo {getattr(hab.contenido, 'nombre', '')}".strip()
	if t == "jefe":
		return f"Jefe {getattr(hab.contenido, 'nombre', '')}".strip()
	if t == "evento":
		return getattr(hab.contenido, "nombre", "evento")
	return str(t) if t else "contenido"

# Acciones del menú
def mostrar_mensaje_guardar():
	# Aquí estará guardar_partida()
	print("\n[ GUARDAR ] Esta función aún no está implementada.")
	input("Presiona ENTER para continuar...")

def mostrar_mensaje_cargar():
	# Aquí estará cargar_partida()
	print("\n[ CARGAR ] Esta función aún no está implementada.")
	input("Presiona ENTER para continuar...")

def confirmar_salida() -> bool:
	resp = input("¿Seguro que deseas salir? (y/n): ").strip().lower()
	return resp == "y"

# Lógica de exploración
def avanzar_un_paso(mapa, explorador, visitadas, ultimo_pos):
	"""Realiza un movimiento y exploración de UNA habitación usando tu lógica."""
	actual = explorador.posicion_actual
	conexiones = mapa.habitaciones[actual].conexiones

	if not conexiones:
		print("No hay conexiones desde aquí.")
		return ultimo_pos # no cambia

	dir_elegida = None

	# Buscar una no visitada
	for d, pos in conexiones.items():
		if pos not in visitadas:
			dir_elegida = d
			break

	# Si no hay, elegir cualquiera que no sea la última
	if dir_elegida is None:
		candidatas = [d for d, p in conexiones.items() if p != ultimo_pos]
		if not candidatas:
			candidatas = list(conexiones.keys())
		dir_elegida = random.choice(candidatas)

	# Mover y explorar
	prev = actual
	if explorador.mover(dir_elegida):
		pos = explorador.posicion_actual
		hab = mapa.habitaciones[pos]
		encabezado = f"Te mueves a {pos}. Hay: {obtener_tipo_contenido(hab)}"
		resultado = explorador.explorar_habitacion()  # texto

		# Registrar visita si es nueva
		if (not visitadas) or (visitadas[-1] != pos):
			if pos not in visitadas:
				visitadas.append(pos)

		# ¿Hubo portal? (la posición cambió durante explorar_habitacion)
		if explorador.posicion_actual != pos:
			# olvida la última pos (no penalizamos vuelta inmediata)
			return None, f"{encabezado}\n(Portal) {resultado}"
		else:
			# seguimos recordando la anterior
			return prev, f"{encabezado}\n{resultado}"
	else:
		return ultimo_pos, "No pudiste moverte."

# Render según vista
def renderizar(vista, vis: Visualizador, mapa, explorador, visitadas, mensajes):
	"""
	Vista: "general" | "habitacion"
	
	Dibuja la interfaz: limpia pantalla, muestra mapa + guía/minimapa o maximapa,
	y el estado del explorador.
	"""
	limpiar_pantalla()

	# Mostrar mapa según vista
	if vista == "habitacion":
		# Maximapa con panel de info
		vis.mostrar_habitacion_actual(mapa, explorador, visitadas)
	else:
		# Mapa general + minimapa
		vis.mostrar_mapa_completo(mapa, explorador.posicion_actual, explorador)
		
	# Ambos mapas incluyen la guía de información

	if mensajes:
		print("\n--- Turno ---")
		print(mensajes)     # es un string simple
		print("-" * 30)

	vis.mostrar_estado_explorador(explorador)

	# Menú
	print("\nAcciones: [ENTER] avanzar | [1] maximapa | [2] mapa | [3] guardar | [4] cargar | [5] salir")
