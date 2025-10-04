from dungeon_generator.core import Mapa
from dungeon_generator.explorer import Explorador
import random

def obtener_tipo_contenido(hab):
	if hab is None or hab.contenido is None:
		return "nada"
	return hab.contenido.descripcion

def main():
	n = 20 # número de habitaciones a explorar
	mapa = Mapa(ancho=8, alto=8)
	mapa.generar_estructura(n_habitaciones=n, seed=61742)
	mapa.decorar()

	explorador = Explorador(mapa, mapa.habitacion_inicial.posicion)

	visitadas = set([explorador.posicion_actual])
	objetivo = n
	ultimo_pos = None

	# Explora inicial
	hab = mapa.habitaciones[explorador.posicion_actual]
	print(f"Explorador en {explorador.posicion_actual}, hay: {obtener_tipo_contenido(hab)}")
	explorador.explorar_habitacion()

	# Límite de seguridad por si el explorador se atrapa, evitar flood en consola
	pasos_max = 30
	# En un futuro se dará la opción de solo habitaciones nuevas

	# Ciclo con lógica de exploración
	while len(visitadas) < objetivo and explorador.esta_vivo and pasos_max > 0:
		pasos_max -= 1
		actual = explorador.posicion_actual
		conexiones = mapa.habitaciones[actual].conexiones

		if not conexiones:
			break

		# Buscamos una habitacion no visitada que no sea la ultima
		dir_elegida = None
		for d, pos in conexiones.items(): # IMPORTANTE faltaría aleatorizar el orden de las conexiones
			if pos not in visitadas and pos != ultimo_pos:
				dir_elegida = d
				break

		# Falta validar la necesidad de este plan de movimiento:
		# Si no hay esta vez recalcula considerando la ultima
		if dir_elegida is None:
			for d, pos in conexiones.items(): # acá también faltaría aleatorizar el orden
				if pos not in visitadas:
					dir_elegida = d
					break

		# Si sigue sin haber, elige cualquiera que no sea la ultima
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
			print(f"Explorador en {pos}, hay: {obtener_tipo_contenido(hab)}")
			explorador.explorar_habitacion()
			visitadas.add(explorador.posicion_actual)

			# Si hubo portal olvida la ultima pos
			if explorador.posicion_actual != pos:
				ultimo_pos = None
			else:
				ultimo_pos = prev

	print(f"Exploración terminada. Inventario: {[str(obj) for obj in explorador.inventario]}")

if __name__ == "__main__":
	main()
