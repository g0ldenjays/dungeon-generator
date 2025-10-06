import json

def pos_a_lista(pos):
	"""
	Convierte una posición (tupla o lista) a una lista de dos enteros [x, y].
	"""

	try:
		return [int(pos[0]), int(pos[1])]
	except Exception:
		return [0, 0]

def serializar_objeto(obj):
	"""
	Serializa un objeto (tesoro, recompensa especial, etc.) a un diccionario.
	"""
	return {
		"nombre": getattr(obj, "nombre", str(obj)),
		"valor": getattr(obj, "valor", 0),
		"descripcion": getattr(obj, "descripcion", ""),
	}

def serializar_contenido(contenido):
	"""
	Serializa el contenido de una habitación a un diccionario.
	"""
	if contenido is None:
		return None

	tipo = getattr(contenido, "tipo", None)

	if tipo == "tesoro":
		obj = getattr(contenido, "objeto", None)
		return {
			"tipo": "tesoro",
			"objeto": serializar_objeto(obj) if obj is not None else None,
			"usado": getattr(contenido, "usado", False)
		}

	if tipo in ("monstruo", "jefe"):
		data = {
			"tipo": tipo,
			"nombre": getattr(contenido, "nombre", ""),
			"vida": getattr(contenido, "vida", 0),
			"ataque": getattr(contenido, "ataque", 0),
		}
		recompensa = getattr(contenido, "recompensa_especial", None)
		if recompensa is not None:
			data["recompensa_especial"] = serializar_objeto(recompensa)
		
		if tipo == "jefe":
			data["muerto"] = getattr(contenido, "muerto", False) 
		
		return data

	if tipo == "evento":
		return {
			"tipo": "evento",
			"nombre": getattr(contenido, "nombre", ""),
			"efecto": getattr(contenido, "efecto", ""),
			"descripcion": getattr(contenido, "descripcion", ""),
			"usado": getattr(contenido, "usado", False),
		}

	return {"tipo": str(tipo) if tipo is not None else "desconocido"}

def serializar_habitacion(hab):
	"""
	Serializa una habitación a un diccionario.
	"""
	conexiones = {}
	try:
		for d, pos in hab.conexiones.items():
			conexiones[d] = pos_a_lista(pos)
	except Exception:
		conexiones = {}

	return {
		"id": getattr(hab, "id", 0),
		"posicion": pos_a_lista(getattr(hab, "posicion", (0, 0))),
		"inicial": bool(getattr(hab, "inicial", False)),
		"visitada": bool(getattr(hab, "visitada", False)),
		"conexiones": conexiones,
		"contenido": serializar_contenido(getattr(hab, "contenido", None)),
	}

def serializar_mapa(mapa):
	"""
	Serializa el mapa completo a un diccionario.
	"""
	try:
		inicial = mapa.habitacion_inicial
		hab_inicial_pos = pos_a_lista(inicial.posicion) if inicial is not None else None
	except Exception:
		hab_inicial_pos = None

	habitaciones = []
	try:
		for _, hab in mapa.habitaciones.items():
			habitaciones.append(serializar_habitacion(hab))
	except Exception:
		habitaciones = []

	return {
		"ancho": int(getattr(mapa, "ancho", 0)),
		"alto": int(getattr(mapa, "alto", 0)),
		"habitacion_inicial": hab_inicial_pos,
		"habitaciones": habitaciones,
	}

def serializar_explorador(explorador):
	"""
	Serializa el explorador completo a un diccionario.
	"""

	inventario = []
	try:
		for obj in getattr(explorador, "inventario", []) or []:
			inventario.append(serializar_objeto(obj))
	except Exception:
		inventario = []

	return {
		"vida": int(getattr(explorador, "vida", 0)),
		"posicion_actual": pos_a_lista(getattr(explorador, "posicion_actual", (0, 0))),
		"inventario": inventario,
		"bonus_ataque": int(getattr(explorador, "bonus_ataque", 0)),
		"bonus_prob": float(getattr(explorador, "bonus_prob", 0.0)),
		"bonus_duracion": int(getattr(explorador, "bonus_duracion", 0)),
		"bonus_total": int(getattr(explorador, "bonus_total", 0)),
	}

def guardar_datos(mapa, explorador, archivo):   
	"""
	Guarda en JSON el estado completo del mapa y del explorador.
	
	- Ruta de salida (ej. 'save_2025-10-05_20.03.24.json')
	"""
	data = {
		"mapa": serializar_mapa(mapa),
		"explorador": serializar_explorador(explorador),
	}

	with open(archivo, "w", encoding="utf-8") as archivo:
		json.dump(data, archivo, ensure_ascii=False, indent=4) # Formateado para aceptar caracteres especiales y legible
