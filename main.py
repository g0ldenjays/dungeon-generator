from dungeon_generator.core import Mapa
from dungeon_generator.explorer import Explorador
from dungeon_generator.visual import Visualizador
import random
import os

def obtener_tipo_contenido(hab):
	if hab is None or hab.contenido is None:
		return "nada"
	return hab.contenido.descripcion

def main():
	os.system('cls' if os.name == 'nt' else 'clear')
	
	vis = Visualizador()
	n = 35 # número de habitaciones a explorar
	mapa = Mapa(ancho=8, alto=8)
	mapa.generar_estructura(n_habitaciones=n, seed=6147)
	mapa.decorar()

	explorador = Explorador(mapa, mapa.habitacion_inicial.posicion)

	visitadas = [explorador.posicion_actual]
	objetivo = n
	ultimo_pos = None

	# CON LA SEMILLA 6147, MAPA 8X8 CON 35 HABS:
		# 31 es el número de pasos para explorar un poco y caer en un portal y bendición, además de varios monstruos y tesoros
		# Pase de 20 a 5 para ver que la barra de vida se actualiza correctamente
		# Escriba 20 para ver que la parte de "¿Es nueva?" funciona
	pasos_max = 34

	# Explora inicial
	hab = mapa.habitaciones[explorador.posicion_actual]
	print(f"({pasos_max}) Explorador en {explorador.posicion_actual}, hay: {obtener_tipo_contenido(hab)}")
	explorador.explorar_habitacion()


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
			print(f"({pasos_max}) Explorador en {explorador.posicion_actual}, hay: {obtener_tipo_contenido(hab)}")
			explorador.explorar_habitacion()
			
			if not visitadas or visitadas[-1] != pos:
				if pos not in visitadas:
					visitadas.append(pos)

			# Si hubo portal olvida la ultima pos
			if explorador.posicion_actual != pos:
				ultimo_pos = None
			else:
				ultimo_pos = prev

			
		vis.mostrar_mapa_completo(mapa, explorador.posicion_actual, explorador)
		vis.mostrar_estado_explorador(explorador)

	#vis.mostrar_habitacion_actual(mapa, explorador, visitadas)
	
	stats = mapa.obtener_estadisticas_mapa()
	print(f"Estadísticas del mapa: {stats}")

if __name__ == "__main__":
	main()
