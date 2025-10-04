class Explorador:
	def __init__(self, mapa, posicion_inicial):
		self.vida = 150
		self.inventario = [] # lista de Objetos
		self.posicion_actual = posicion_inicial
		self.mapa = mapa
 
	# Moverse a una dirección
	def mover(self, direccion):
		habitacion = self.mapa.habitaciones[self.posicion_actual]
		if direccion in habitacion.conexiones:
			self.posicion_actual = habitacion.conexiones[direccion]
			return True
		return False

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
