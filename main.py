from dungeon_generator.explorer import Explorador
from dungeon_generator.core import Mapa
from dungeon_generator.visual import Visualizador
from dungeon_generator.utils import pedir_entero, confirmar_salida, renderizar, guardar_partida, cargar_partida, avanzar_un_paso

def main():
	print("Parámetros del mapa (ENTER para valores por defecto):")
	ancho = pedir_entero("Ancho", 8)
	alto = pedir_entero("Alto", 8)

	while ancho <= 3 or alto <= 3 or ancho >= 15 or alto >= 15:
		print("El ancho y alto deben estar entre 4 y 14.")
		ancho = pedir_entero("Ancho", 8)
		alto = pedir_entero("Alto", 8)

	n_habs = pedir_entero("Cantidad de habitaciones", 35)
	while n_habs > ancho * alto or n_habs <= 4:
		print(f"La cantidad de habitaciones debe estar entre 5 y {ancho * alto}.")
		n_habs = pedir_entero("Cantidad de habitaciones", 35)

	semilla = pedir_entero("Semilla", 6147)

	mapa = Mapa(ancho=ancho, alto=alto)
	mapa.generar_estructura(n_habitaciones=n_habs, seed=semilla)
	mapa.decorar()
	explorador = Explorador(mapa, mapa.habitacion_inicial.posicion)

	visitadas = [explorador.posicion_actual]
	ultimo_pos = None

	vista = "general"
	vis = Visualizador()
	mensajes = ""

	# Bucle principal
	while explorador.esta_vivo:
		renderizar(vista, vis, mapa, explorador, visitadas, mensajes)

		comando = input("> ").strip()
		if comando == "1":
			vista = "habitacion"
			continue
		elif comando == "2":
			vista = "general"
			continue
		elif comando == "3":
			guardar_partida(mapa, explorador)
			continue
		elif comando == "4":
			res = cargar_partida()
			if res is not None:
				mapa_cargado, explorador_cargado = res
				if mapa_cargado is not None and explorador_cargado is not None:
					mapa = mapa_cargado
					explorador = explorador_cargado
			continue
		elif comando == "5":
			if confirmar_salida():
				break
			else:
				continue
		else:
			# Avanzar una sala
			ultimo_pos, mensajes = avanzar_un_paso(mapa, explorador, visitadas, ultimo_pos)
		
		if len(visitadas) == len(mapa.habitaciones):
			print("¡Has explorado todas las habitaciones!")
			break

	# Fin de juego
	print("\nExploración terminada.")
	if explorador.esta_vivo:
			print("¡Has escapado de la mazmorra!")
	else:
		print("Has muerto...")
		vis.mostrar_habitacion_actual(mapa, explorador, visitadas)
		
	inv_txt = []
	for o in explorador.inventario:
		inv_txt.append(f"{o.nombre} ({o.valor})")
	print(f"Inventario final: {inv_txt}")

if __name__ == "__main__":
	main()
