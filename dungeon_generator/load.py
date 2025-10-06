import json

from dungeon_generator.core import Mapa, Habitacion
from dungeon_generator.explorer import Explorador
from dungeon_generator.content import Tesoro, Monstruo, Jefe, Evento, Objeto


def lista_a_pos(lst):
	"""Convierte listas [x, y] a tuplas (x, y)."""
	try:
		return (int(lst[0]), int(lst[1]))
	except Exception:
		return (0, 0)


def deserializar_objeto(d):
	"""Pasa de dict a Objeto."""
	if not d:
		return None
	nombre = d.get("nombre", "Objeto")
	valor = d.get("valor", 0)
	descripcion = d.get("descripcion", "")
	return Objeto(nombre, valor=valor, descripcion=descripcion)


def deserializar_contenido(d):
	"""
	Pasa de dict a instancia de contenido o None.
	"""
	if d is None:
		return None

	tipo = d.get("tipo")

	if tipo == "tesoro":
		obj = deserializar_objeto(d.get("objeto"))
		usado = d.get("usado", False)
		return Tesoro(obj, usado) if obj is not None else None

	if tipo == "monstruo":
		nombre = d.get("nombre", "Monstruo")
		vida = d.get("vida", 1)
		ataque = d.get("ataque", 1)
		return Monstruo(nombre, vida=vida, ataque=ataque)

	if tipo == "jefe":
		nombre = d.get("nombre", "Jefe")
		vida = d.get("vida", 5)
		ataque = d.get("ataque", 2)
		recompensa = deserializar_objeto(d.get("recompensa_especial"))
		muerto = d.get("muerto", False)
		return Jefe(nombre, vida=vida, ataque=ataque, recompensa_especial=recompensa, muerto=muerto)

	if tipo == "evento":
		nombre = d.get("nombre", "Evento")
		efecto = d.get("efecto", "")
		descripcion = d.get("descripcion", "")
		usado = d.get("usado", False)
		return Evento(nombre=nombre, efecto=efecto, descripcion=descripcion, usado=usado)

	return None


def reconstruir_habitacion(hd):
	"""
	Pasa de dict de habitación a Habitacion con todos sus campos sin insertarla en el mapa.
	"""
	hid = hd.get("id", 0)
	pos = lista_a_pos(hd.get("posicion", [0, 0]))
	init = bool(hd.get("inicial", False))
	hab = Habitacion(hid, pos, inicial=init)

	# Visitada
	hab.visitada = bool(hd.get("visitada", False))

	# Conexiones: dir -> [x, y]
	conns = hd.get("conexiones", {}) or {}
	hab.conexiones = {}
	try:
		for d, lst in conns.items():
			hab.conexiones[d] = lista_a_pos(lst)
	except Exception:
		pass

	# Contenido
	hab.contenido = deserializar_contenido(hd.get("contenido"))

	return hab


def reconstruir_mapa(mdata):
	"""
	Pasa de dict de mapa a Mapa reconstruido (habitaciones, inicial).
	"""
	ancho = int(mdata.get("ancho", 0))
	alto = int(mdata.get("alto", 0))

	mapa = Mapa(ancho=ancho, alto=alto)

	# Habitaciones
	mapa.habitaciones = {}
	habitaciones_json = mdata.get("habitaciones", []) or []
	for hd in habitaciones_json:
		hab = reconstruir_habitacion(hd)
		mapa.habitaciones[hab.posicion] = hab

	# Habitación inicial
	pos_ini = mdata.get("habitacion_inicial")
	if pos_ini is not None:
		pos_t = lista_a_pos(pos_ini)
		mapa.habitacion_inicial = mapa.habitaciones.get(pos_t)
	else:
		# Busca la que tenga inicial=True
		mapa.habitacion_inicial = None
		for hab in mapa.habitaciones.values():
			if getattr(hab, "inicial", False):
				mapa.habitacion_inicial = hab
				break

	return mapa


def reconstruir_explorador(edata, mapa):
	"""
	Pasa de dict de explorador + mapa a Explorador listo.
	"""
	pos = lista_a_pos(edata.get("posicion_actual", [0, 0]))
	exp = Explorador(mapa, pos)

	# Vida
	exp.vida = int(edata.get("vida", getattr(exp, "vida", 5)))

	# Inventario
	exp.inventario = []
	for od in edata.get("inventario", []) or []:
		obj = deserializar_objeto(od)
		if obj is not None:
			exp.inventario.append(obj)

	# Bonus
	exp.bonus_ataque = int(edata.get("bonus_ataque", 0))
	exp.bonus_prob = float(edata.get("bonus_prob", 0.0))
	exp.bonus_duracion = int(edata.get("bonus_duracion", 0))
	exp.bonus_total = int(edata.get("bonus_total", 0))

	return exp


def cargar_datos(archivo):
	"""
	Lee un archivo de save JSON y devuelve (mapa, explorador).

	Lanza excepción si el archivo no existe o está corrupto.
	"""
	with open(archivo, "r", encoding="utf-8") as archivo:
		data = json.load(archivo)

	mdata = data.get("mapa", {})
	edata = data.get("explorador", {})

	mapa = reconstruir_mapa(mdata)
	explorador = reconstruir_explorador(edata, mapa)

	return mapa, explorador
