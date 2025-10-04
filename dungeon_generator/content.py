from abc import ABC, abstractmethod
import random


# Clase Objeto
class Objeto:
	def __init__(self, nombre, valor, descripcion):
		self.nombre = nombre
		self.valor = valor
		self.descripcion = descripcion

	def __str__(self):
		return f"{self.nombre} (valor: {self.valor})"


# Clase base abstracta
class ContenidoHabitacion(ABC):
	@property
	@abstractmethod
	def descripcion(self):
		"""Descripción textual del contenido"""
		pass

	@property
	@abstractmethod
	def tipo(self):
		"""Tipo de contenido (tesoro, monstruo, jefe, evento)"""
		pass

	@abstractmethod
	def interactuar(self, explorador):
		"""Acción al interactuar con el contenido"""
		pass


# Tesoro
class Tesoro(ContenidoHabitacion):
	def __init__(self, objeto):
		self.objeto = objeto

	@property
	def descripcion(self):
		return f"Un cofre que contiene {self.objeto.nombre}"

	@property
	def tipo(self):
		return "tesoro"

	def interactuar(self, explorador):
		explorador.inventario.append(self.objeto)
		return f"Encontraste un tesoro: {self.objeto}"


# Monstruo
class Monstruo(ContenidoHabitacion):
	def __init__(self, nombre, vida, ataque):
		self.nombre = nombre
		self.vida = vida
		self.ataque = ataque

	@property
	def descripcion(self):
		return f"Monstruo {self.nombre} (vida {self.vida}, ataque {self.ataque})"

	@property
	def tipo(self):
		return "monstruo"

	def interactuar(self, explorador):
		texto = [f"¡Un {self.nombre} aparece! Vida: {self.vida}, Ataque: {self.ataque}"]

		while self.vida > 0 and explorador.vida > 0:
			if random.random() < 0.5:
				# Explorador ataca
				self.vida -= 1
				texto.append(f"Golpeas al {self.nombre}. Le queda {self.vida} de vida.")
			else:
				# Monstruo ataca
				explorador.recibir_dano(self.ataque)
				texto.append(f"El {self.nombre} te golpea. Te queda {explorador.vida} de vida.")

		if self.vida <= 0:
			texto.append(f"¡Derrotaste al {self.nombre}!")
		else:
			texto.append("Has sido derrotado...")

		return "\n".join(texto)


# Jefe (hereda de Monstruo)
class Jefe(Monstruo):
	def __init__(self, nombre, vida, ataque, recompensa_especial):
		super().__init__(nombre, vida, ataque)
		self.recompensa_especial = recompensa_especial

	@property
	def descripcion(self):
		return f"Un jefe temible: {self.nombre} (vida {self.vida}, ataque {self.ataque})"

	@property
	def tipo(self):
		return "jefe"

	def interactuar(self, explorador):
		texto = [f"¡Un jefe {self.nombre} aparece! Vida: {self.vida}, Ataque: {self.ataque}"]

		while self.vida > 0 and explorador.vida > 0:
			if random.random() < 0.35:  # Explorador acierta menos
				self.vida -= 1
				texto.append(f"Golpeas al {self.nombre}. Le queda {self.vida} de vida.")
			else:
				explorador.recibir_dano(self.ataque)
				texto.append(f"El {self.nombre} te golpea. Te queda {explorador.vida} de vida.")

		if self.vida <= 0:
			texto.append(f"¡Derrotaste al jefe {self.nombre}!")
			explorador.inventario.append(self.recompensa_especial)
			texto.append(f"Obtienes una recompensa especial: {self.recompensa_especial}")
		else:
			texto.append("Has sido derrotado por el jefe...")

		return "\n".join(texto)




# Eventos
class Evento(ContenidoHabitacion):
	def __init__(self, nombre, descripcion, efecto):
		self.nombre = nombre
		self._descripcion = descripcion
		self.efecto = efecto

	@property
	def descripcion(self):
		return f"Evento: {self._descripcion}"

	@property
	def tipo(self):
		return "evento"

	def interactuar(self, explorador):
		texto = [f"Ocurre un evento: {self.nombre} - {self._descripcion}"]

		if self.efecto == "trampa":
			explorador.recibir_dano(1)
			texto.append("¡Caíste en una trampa! Pierdes 1 de vida.")
		elif self.efecto == "fuente":
			explorador.vida += 1
			texto.append("Encuentras una fuente mágica. Ganas 1 de vida.")
		elif self.efecto == "bonificacion":
			explorador.bonus += 1 # Aun no se ha implementado la duracion por X celdas ni efecto en combate
			texto.append("Recibes una bendición temporal (+ Ataque).")
		elif self.efecto == "portal":
			posibles = [h for h in explorador.mapa.habitaciones.values() if h.posicion != explorador.posicion_actual]
			if posibles:
				destino = random.choice(posibles)
				explorador.posicion_actual = destino.posicion
				destino.visitada = True
				texto.append(f"Un portal se abre... ¡eres transportado a {destino.posicion}!")
			else:
				texto.append("El portal intentó activarse, pero no encontró destino.")
		else:
			texto.append("El evento no tuvo efecto concreto.")

		return "\n".join(texto)
