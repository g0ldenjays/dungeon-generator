from dataclasses import dataclass
import random


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
		self.contenido: str | None = None # aquí iría el contenido de la habitación (enemigos, tesoros, etc.)

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
		# Devuelve lista de (nx, ny, dir_desde_actual, dir_desde_nuevo)
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