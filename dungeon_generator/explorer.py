class Explorador:
	def __init__(self, mapa, posicion_inicial):
		self.vida = 20
		self.inventario = []
		self.posicion_actual = posicion_inicial
		self.mapa = mapa

		self.bonus_ataque = 0 # Daño extra
		self.bonus_prob = 0.0 # Probabilidad extra
		self.bonus_duracion = 0 # Habitaciones restantes antes de acabarse
		self.aux = 0
 
	# Moverse a una dirección
	def mover(self, direccion):
		habitacion = self.mapa.habitaciones[self.posicion_actual]
		if direccion in habitacion.conexiones:
			self.posicion_actual = habitacion.conexiones[direccion]

	    # Lógica bonus
		if self.bonus_duracion > 0:
			self.bonus_duracion -= 1
			if self.bonus_duracion == 0:
				self.bonus_ataque = 0
				self.bonus_prob = 0.0
				self.bonus_total = 0

		return True

	# Explorar la habitación actual
	def explorar_habitacion(self):
		habitacion = self.mapa.habitaciones[self.posicion_actual]
		habitacion.visitada = True

		if habitacion.contenido is None:
			return "La habitación está vacía."

		# Ejecutar la interacción con el contenido
		resultado = habitacion.contenido.interactuar(self)
		return resultado

	# Habitaciones adyacentes
	def obtener_habitaciones_adyacentes(self):
		habitacion = self.mapa.habitaciones[self.posicion_actual]
		return list(habitacion.conexiones.keys())

	# Recibir daño
	def recibir_dano(self, cantidad):
		self.vida -= cantidad
		if self.vida < 0:
			self.vida = 0

	# Verificar si está vivo
	@property
	def esta_vivo(self):
		return self.vida > 0
	
	def aplicar_bonificacion(self, potencia, atk, prob):

		self.aux = potencia
		self.bonus_duracion = max(2, int(potencia)) # Al menos 2 habitaciones de duración
		self.bonus_total = self.bonus_duracion
		self.bonus_ataque = max(0, int(atk))
		p = float(prob)
		self.bonus_prob = p
