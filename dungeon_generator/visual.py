from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.columns import Columns

class Visualizador:
	def __init__(self):
		self.console = Console()

	def estilo(self, ch: str) -> str:
		if ch == "@": return "[bright_green]@[/]"
		if ch == "$": return "[gold1]$[/]"
		if ch == "E": return "[red]E[/]"
		if ch == "J": return "[dark_violet]J[/]"
		if ch == "!": return "[cyan]![/]"
		if ch == "I": return "[pale_turquoise1]I[/]"
		if ch == ".": return "[grey70].[/]"
		return ch

	def simbolo_contenido(self, hab):
		if hab.contenido is None:
			return None
		t = getattr(hab.contenido, "tipo", None)
		if t == "tesoro": return "$"
		if t == "monstruo": return "E"
		if t == "jefe": return "J"
		if t == "evento": return "!"
		return None

	# Guía
	def panel_guia(self):

		def blk(style):  # bloque 1x1 (espacio con fondo)
			return f"[{style}] [/]"

		bg = {
			"jugador": "on bright_green",
			"tesoro":  "on gold1",
			"enemigo": "on red",
			"jefe":    "on dark_violet",
			"evento":  "on cyan",
			"inicio":  "on pale_turquoise1",
			"piso":    "on grey23",
		}

		texto = (
			f"{blk(bg['jugador'])}  Jugador\n"
			f"{blk(bg['tesoro'])}  Tesoro\n"
			f"{blk(bg['enemigo'])}  Enemigo\n"
			f"{blk(bg['jefe'])}  Jefe\n"
			f"{blk(bg['evento'])}  Evento\n"
			f"{blk(bg['inicio'])}  Inicio\n"
			f"{blk(bg['piso'])}  Piso / Conexión"
		)
		return Panel(texto, title="Guía", box=box.ROUNDED)

	# Vista general del mapa
	def mostrar_mapa_completo(self, mapa, pos_explorador):
		"""Muestra el mapa completo con contenido en habitaciones usando bloques de color."""
		bh, bw = 3, 3
		gap = 1

		H = mapa.alto * bh + (mapa.alto - 1) * gap
		W = mapa.ancho * bw + (mapa.ancho - 1) * gap

		canvas = [[" " for _ in range(W)] for _ in range(H)]

		def put(r, c, ch):
			if 0 <= r < H and 0 <= c < W:
				canvas[r][c] = ch

		for y in range(mapa.alto):
			for x in range(mapa.ancho):
				pos = (x, y)
				if pos not in mapa.habitaciones:
					continue
				hab = mapa.habitaciones[pos]

				r0 = y * (bh + gap)
				c0 = x * (bw + gap)

				# Sala de 3x3
				for rr in range(bh):
					for cc in range(bw):
						put(r0 + rr, c0 + cc, ".")

				# Conexiones
				if "norte" in hab.conexiones and r0 - 1 >= 0:
					put(r0 - 1, c0 + 1, ".")

				if "sur" in hab.conexiones and r0 + bh < H: 
					put(r0 + bh, c0 + 1, ".")

				if "oeste" in hab.conexiones and c0 - 1 >= 0: 
					put(r0 + 1, c0 - 1, ".")

				if "este" in hab.conexiones and c0 + bw < W: 
					put(r0 + 1, c0 + bw, ".")

				# Contenido (centro derecho de la sala)
				sym = self.simbolo_contenido(hab)
				if sym:
					put(r0 + 1, c0 + 2, sym)

				# Jugador (centro izquierdo de la sala)
				if pos == pos_explorador:
					put(r0 + 1, c0 + 0, "@")

				# Marcar inicio
				if mapa.habitacion_inicial and pos == mapa.habitacion_inicial.posicion:
					put(r0 + 1, c0 + 1, "I")

		# Render con bloques 2x1 por carácter
		SCALE_X = 2  # ancho del bloque

		bg = {
			" ": "on grey11", # vacío
			".": "on grey23", # piso / conexión
			"@": "on bright_green", # jugador
			"$": "on gold1", # tesoro
			"E": "on red", # enemigo
			"J": "on dark_violet", # jefe
			"!": "on cyan", # evento
			"I": "on pale_turquoise1", # inicio
		}

		def cell_block(ch: str) -> str:
			style = bg.get(ch, "on grey11")  # por defecto vacío
			return f"[{style}]" + " " * SCALE_X + "[/]"

		filas = []
		for r in range(H):
			frag = []
			for ch in canvas[r]:
				frag.append(cell_block(ch))
			filas.append("".join(frag))

		mapa_panel = Panel("\n".join(filas), title="Mapa General", box=box.ROUNDED, padding=(0, 1))

		guia = self.panel_guia()

		# Mostrar mapa y guia lado a lado
		self.console.print(Columns([mapa_panel, guia], equal=True, expand=True))

	# Vista detallada de la habitación actual
	def mostrar_habitacion_actual(self, mapa, explorador, visitadas):
		"""
		Dibuja la habitación actual usando bloques de color.
		
		- @ en centro-izq
		- contenido en centro-der (si existe)
		- I en el centro si es la inicial

		Debajo muestra un panel con datos de la habitación.
		"""

		# Base 3x3 de símbolos
		base = [
			["." , "." , "."],
			["." , "." , "."],
			["." , "." , "."],
		]

		pos = explorador.posicion_actual
		hab = mapa.habitaciones[pos]

		# Jugador @ en (1,0)
		base[1][0] = "@"

		# Contenido si lo hay en (1,2)
		sym = self.simbolo_contenido(hab)
		if sym:
			base[1][2] = sym

		# Marca de inicio 'I' en el centro (1,1), siempre
		if mapa.habitacion_inicial and pos == mapa.habitacion_inicial.posicion:
			base[1][1] = "I"

		# ----- Render de bloques 4x4 por celda -----
		# Mapeo de fondo por símbolo
		bg = {
			".": "on grey23",
			"@": "on bright_green",
			"$": "on gold1",
			"E": "on red",
			"J": "on dark_violet",
			"!": "on cyan",
			"I": "on pale_turquoise1",
		}
		# ----- Render de bloques 4x2 por celda -----
		SCALE_X = 8  # ancho del bloque
		SCALE_Y = 4  # alto del bloque

		lineas = []
		for r in range(3):
			# cada fila de la base genera SCALE_Y líneas visuales
			for _ in range(SCALE_Y):
				frag = []
				for c in range(3):
					ch = base[r][c]
					style = bg.get(ch, "on grey23")
					frag.append(f"[{style}]" + " " * SCALE_X + "[/]")
				lineas.append("".join(frag))

		panel_hab = Panel(
			"\n".join(lineas),
			title=f"Maximapa ({pos})",
			box=box.ROUNDED,
			padding=(0, 1),
		)

		# Guía
		guia = self.panel_guia()

		# Panel de información sobre la habitación
		es_nueva = False
		if visitadas:
			try:
				es_nueva = bool(visitadas) and visitadas[-1] == pos

			except Exception:
				es_nueva = (pos in visitadas)

		cont_nombre = "Ninguno"
		cont_desc = "[No hay descripción]"
		if hab.contenido is not None:
			try:
				if hasattr(hab.contenido, "tipo") and hab.contenido.tipo == "tesoro" and hasattr(hab.contenido, "objeto"):
					cont_nombre = getattr(hab.contenido.objeto, "nombre", "Tesoro")
					cont_desc = getattr(hab.contenido.objeto, "descripcion", "Un objeto valioso.")
				else:
					cont_nombre = getattr(hab.contenido, "nombre", type(hab.contenido).__name__)
					cont_desc = getattr(hab.contenido, "descripcion", f"Tipo: {getattr(hab.contenido, 'tipo', 'desconocido')}")
			except Exception:
				cont_nombre = type(hab.contenido).__name__
				cont_desc = f"Tipo: {getattr(hab.contenido, 'tipo', 'desconocido')}"

		dirs = []
		for d in ("norte", "sur", "oeste", "este"):
			if d in hab.conexiones:
				dirs.append(d)
		conexiones_txt = ", ".join(dirs) if dirs else "sin salidas"

		info_txt = (
			f"Habitación: {pos}\n"
			f"¿Es nueva?: {es_nueva}\n"
			f"Contenido: {cont_nombre}: {cont_desc}\n"
			f"Conexiones: {conexiones_txt}"
		)
		panel_info = Panel(info_txt, title="Información", box=box.ROUNDED)

		# Mostrar todo
		self.console.print(Columns([panel_hab, guia], equal=True, expand=True))
		self.console.print(panel_info)
