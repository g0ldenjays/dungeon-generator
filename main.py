from dungeon_generator.core import Mapa

def main():
	ancho, alto = 8, 8
	total = 20

	mapa = Mapa(ancho, alto)
	mapa.generar_estructura(total, seed=3) # Seed fija

	hab_inicial = mapa.habitacion_inicial
	print("=== DÍA 1: Prueba de generación de mapa ===")
	print(f"Mapa: {ancho}x{alto}")
	print(f"Habitaciones generadas: {len(mapa.habitaciones)} (esperado: {total})")
	print(f"Inicial en borde: {(hab_inicial.posicion[0], hab_inicial.posicion[1])}\n")

	# Mostrar habitaciones con sus conexiones
	print("Ejemplo de habitaciones:")
	for (x, y), hab in list(mapa.habitaciones.items()):
		print(f"- Hab {hab.id} en {x},{y}, conexiones: {hab.conexiones}")

if __name__ == "__main__":
	main()
