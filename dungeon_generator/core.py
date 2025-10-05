from dataclasses import dataclass
import random
from dungeon_generator.content import Tesoro, Monstruo, Jefe, Evento, Objeto


# Clase Habitacion
@dataclass
class Habitacion:
	"""
	Representa una habitación en el mapa del dungeon.

	- id: identificador único de la habitación.
	- posicion: coordenadas (x, y) en el mapa.
	- inicial: si es la habitación inicial.
	- visitada: si ha sido visitada (para generación o recorrido).
	- conexiones: diccionario de conexiones a otras habitaciones (dirección -> (x,y)).
	- contenido: enemigos, tesoros, etc. (a definir).
	"""
	def __init__(self, id: int, posicion: tuple[int, int], inicial: bool = False):
		self.id: int = id
		self.posicion: tuple[int, int] = posicion
		self.inicial: bool = inicial
		self.visitada: bool = False
		self.conexiones: dict[str, tuple[int, int]] = {}
		self.contenido = None # aquí iría el contenido de la habitación (enemigos, tesoros, etc.)

# ---------------------------------------------------------

# Clase Mapa
class Mapa:
	"""
	Representa un mapa de dungeon con habitaciones conectadas.
	
	- ancho, alto: dimensiones del mapa en número de habitaciones.
	- habitaciones: diccionario con las habitaciones creadas, clave (x,y).
	- habitacion_inicial: referencia a la habitación inicial (en un borde).

	"""
	def __init__(self, ancho: int, alto: int):
		if ancho <= 0 or alto <= 0:
			raise ValueError("El ancho y alto deben ser positivos")

		self.ancho = ancho
		self.alto = alto
		self.habitaciones: dict[tuple[int, int], Habitacion] = {}
		self.habitacion_inicial: Habitacion | None = None

	def generar_estructura(self, n_habitaciones: int, seed: int = 42):
		random.seed(seed)

		max_posibles = self.ancho * self.alto
		if n_habitaciones > max_posibles:
			raise ValueError(f"No caben {n_habitaciones} habitaciones en un mapa de {self.ancho}x{self.alto}")

		# Crear la inicial en el borde
		posicion_inicial = self.posicion_borde()
		h0 = Habitacion(id=0, posicion=posicion_inicial, inicial=True)
		self.habitaciones[posicion_inicial] = h0
		self.habitacion_inicial = h0

		# Expandir hasta llegar al total
		id_counter = 1
		frontera = [posicion_inicial]  # Candidatos a expandir

		while len(self.habitaciones) < n_habitaciones and frontera:
			p_expansion = random.choice(frontera)
			vecinos = self.vecinos_validos(p_expansion)
			random.shuffle(vecinos)

			# Elegir cuántos vecinos generar (1 hasta cantidad de vecinos)
			max_generar = len(vecinos)
			generar = random.randint(1, max_generar)

			generados = 0
			for pos_nuevo, dir_actual, dir_nuevo in vecinos:
				if len(self.habitaciones) >= n_habitaciones:
					break

				if pos_nuevo not in self.habitaciones:
					nueva = Habitacion(id=id_counter, posicion=pos_nuevo)
					self.habitaciones[pos_nuevo] = nueva

					# Conexiones ida/vuelta
					self.habitaciones[p_expansion].conexiones[dir_actual] = pos_nuevo
					nueva.conexiones[dir_nuevo] = p_expansion

					frontera.append(pos_nuevo)
					id_counter += 1
					generados += 1

					if generados >= generar:
						break

			# Si no se generó nada desde este punto, lo quitamos de la frontera
			if generados == 0:
				frontera.remove(p_expansion)

		# Validaciones finales
		if len(self.habitaciones) != n_habitaciones:
			raise RuntimeError("No se alcanzó el número de habitaciones solicitado")

		if not self.es_borde(self.habitacion_inicial.posicion[0], self.habitacion_inicial.posicion[1]):
			raise RuntimeError("La habitación inicial no está en un borde")

		if not self.todas_accesibles():
			raise RuntimeError("Las habitaciones no quedaron todas conectadas")


	# Estadíscas del mapa
	def obtener_estadisticas_mapa(self):
		total = len(self.habitaciones)
		conteos = {"vacia": 0, "tesoro": 0, "monstruo": 0, "jefe": 0, "evento": 0}
		total_conexiones = 0

		for hab in self.habitaciones.values():
			# Conexiones
			total_conexiones += len(hab.conexiones)

			# Contenidos
			if hab.contenido is None:
				conteos["vacia"] += 1
			else:
				try:
					t = hab.contenido.tipo
				except AttributeError:
					t = None

				if t == "tesoro":
					conteos["tesoro"] += 1
				elif t == "monstruo":
					conteos["monstruo"] += 1
				elif t == "jefe":
					conteos["jefe"] += 1
				elif t == "evento":
					conteos["evento"] += 1
				else:
					conteos["vacia"] += 1

		if total > 0:
			promedio = total_conexiones / total
		else:
			promedio = 0.0

		return {
			"total_habitaciones": total,
			"distribucion_por_tipo": conteos,
			"promedio_conexiones": promedio,
		}


	# Métodos de ayuda internos
	def posicion_borde(self) -> tuple[int, int]:
		borde = random.choice(["arriba", "abajo", "izquierda", "derecha"])
		if borde == "arriba":
			return (random.randint(0, self.ancho - 1), 0)
		elif borde == "abajo":
			return (random.randint(0, self.ancho - 1), self.alto - 1)
		elif borde == "izquierda":
			return (0, random.randint(0, self.alto - 1))
		else:  # derecha
			return (self.ancho - 1, random.randint(0, self.alto - 1))

	def es_borde(self, x: int, y: int) -> bool:
		return x == 0 or x == self.ancho - 1 or y == 0 or y == self.alto - 1

	def vecinos_validos(self, posicion: tuple[int, int]) -> list[tuple[tuple[int, int], str, str]]:
		# Devuelve lista de ( (nx, ny), dir_desde_actual, dir_desde_nuevo)
		movimientos = [
			((0, -1), "norte", "sur"),
			((0, 1), "sur", "norte"),
			((-1, 0), "oeste", "este"),
			((1, 0), "este", "oeste"),
		]

		res = []
		for pos_vecino, d1, d2 in movimientos:
			nx, ny = posicion[0] + pos_vecino[0], posicion[1] + pos_vecino[1]
			if 0 <= nx < self.ancho and 0 <= ny < self.alto:
				res.append(((nx, ny), d1, d2))
		return res
	
	def distancia_desde_inicial(self, pos):
		"""Distancia Manhattan desde 'pos' hasta la habitación inicial."""
		x0, y0 = self.habitacion_inicial.posicion
		return abs(pos[0] - x0) + abs(pos[1] - y0)
	
	
	def todas_accesibles(self) -> bool:
		# BFS para verificar que todas las habitaciones se puedan alcanzar
		if self.habitacion_inicial is None:
			return False

		inicio = (self.habitacion_inicial.posicion[0], self.habitacion_inicial.posicion[1])
		visitadas = {inicio}
		cola = [inicio]

		while cola:
			x, y = cola.pop(0)
			hab = self.habitaciones[(x, y)]
			for dir, (nx, ny) in hab.conexiones.items():
				if (nx, ny) not in visitadas:
					visitadas.add((nx, ny))
					cola.append((nx, ny))

		return len(visitadas) == len(self.habitaciones)
	



	# Método más contundente
	def decorar(self):
		"""
		Reparte el contenido de las habitaciones según los porcentajes definidos en el README:

		- Jefes: 2% (al menos 1).
		- Monstruos: 27%.
		- Tesoros: 15%.
		- Eventos: 10%.
		- Resto vacías.

		"""

		# La inicial no lleva contenido
		habitaciones_disponibles = [h for h in self.habitaciones.values() if not h.inicial]
		total = len(habitaciones_disponibles)
		random.shuffle(habitaciones_disponibles)

		# Cálculo de cantidades
		n_jefes = max(1, round(total * 0.02))
		n_monstruos = round(total * 0.27)
		n_tesoros = round(total * 0.15)
		n_eventos = round(total * 0.10)

		# Contenidos
		posibles_jefes = [
			("Gleeok", 1, 3, Objeto("Cuerno de Gleeok", 40, "Poderoso cuerno pesado")),
			("Stalhinox", 1, 2, Objeto("Ojo de Stalhinox", 35, "Gelatinoso... y parpadeante")),
			("Centaleón", 1, 4, Objeto("Corazón de Centaleón", 30, "Aún palpita con fuerza")),
		]

		posibles_monstruos = [
			("Bokoblin", 1, 1),
			("Moblin", 1, 2),
			("Keese", 1, 1),
		]

		posibles_tesoros = [
			("Roca suave", 2, "Roca fina que parece especial"),
			("Chapa metálica", 4, "Tiene algo grabado, aún brilla un poco"),
			("Reloj de oro", 6, "Tic tac... Tic... Y ya se le acabó la pila"),
			("Anillo con diamante", 10, "El brillo te encandila"),
			("Espada de esmeralda", 12, "Se ve pixelada..."),
		]

		posibles_eventos = [
			("Bendicion", "La sala estaba bendecida", "bonificacion", False),
			("Trampa", "Un mecanismo oculto se activa", "trampa", False),
			("Fuente de las hadas", "Fuente con hadas brillantes", "fuente", False),
			("Portal", "Una grieta en el espacio tiempo se abre", "portal", False),
		]

	# Asignación de contenido en habitaciones:

		# Asignar jefes
		for i in range(n_jefes):
			if not habitaciones_disponibles:
				break
			hab = habitaciones_disponibles.pop()
			distancia = self.distancia_desde_inicial(hab.posicion)
			nombre, base_hp, base_atk, recompensa = random.choice(posibles_jefes)
			hab.contenido = Jefe(
				nombre,
				vida=base_hp + distancia,
				ataque=base_atk + distancia// 2,
				recompensa_especial=recompensa
			)

		# Asignar Monstruos
		for i in range(n_monstruos):
			if not habitaciones_disponibles:
				break
			hab = habitaciones_disponibles.pop()
			distancia = self.distancia_desde_inicial(hab.posicion)
			nombre, base_hp, base_atk = random.choice(posibles_monstruos)
			hab.contenido = Monstruo(
				nombre,
				vida=base_hp + distancia// 2,
				ataque=base_atk + distancia// 3
			)

		# Asignar Tesoros
		for i in range(n_tesoros):
			if not habitaciones_disponibles:
				break
			hab = habitaciones_disponibles.pop()
			distancia = self.distancia_desde_inicial(hab.posicion)
			nombre, valor, desc = random.choice(posibles_tesoros)
			objeto = Objeto(nombre, valor=valor + distancia, descripcion=desc)
			hab.contenido = Tesoro(objeto)

		# Asignar Eventos
		for i in range(n_eventos):
			if not habitaciones_disponibles:
				break
			hab = habitaciones_disponibles.pop()
			nombre, desc, efecto, usado = random.choice(posibles_eventos)
			hab.contenido = Evento(nombre, desc, efecto, usado)

		# El resto vacías
		for hab in habitaciones_disponibles:
			hab.contenido = None

