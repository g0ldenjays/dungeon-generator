from dungeon_generator.explorer import Explorador
from dungeon_generator.core import Mapa
from dungeon_generator.visual import Visualizador
from dungeon_generator.utils import pedir_entero, confirmar_salida, renderizar, mostrar_mensaje_guardar, mostrar_mensaje_cargar, avanzar_un_paso

def main():
	print("Parámetros del mapa (ENTER para valores por defecto):")
	ancho = pedir_entero("Ancho", 8)
	alto = pedir_entero("Alto", 8)
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
			mostrar_mensaje_guardar()
			continue
		elif comando == "4":
			mostrar_mensaje_cargar()
			continue
		elif comando == "5":
			if confirmar_salida():
				break
			else:
				continue
		else:
			# Avanzar una sala
			ultimo_pos, mensajes = avanzar_un_paso(mapa, explorador, visitadas, ultimo_pos)

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
