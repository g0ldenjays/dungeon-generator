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
		if ch == "I": return "[yellow2]I[/]"
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

	# Leyenda
	def panel_leyenda(self) -> Panel:
		texto = (
			"[bright_green]@[/] = Jugador\n"
			"[gold1]$[/] = Tesoro\n"
			"[red]E[/] = Enemigo\n"
			"[dark_violet]J[/] = Jefe\n"
			"[cyan]![/] = Evento\n"
			"[yellow2]I[/] = Inicio\n"
			"[grey70].[/] = Piso / conexión"
		)
		return Panel(texto, title="Guía", box=box.ROUNDED)

	def mostrar_mapa_completo(self, mapa, pos_explorador):
		"""Salas 3x3 de '.', un '.' extra por conexión y contenido visible en todas las salas."""
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

		filas = ["".join(self.estilo(ch) for ch in row) for row in canvas]
		mapa_panel = Panel("\n".join(filas), title="Mapa", box=box.SIMPLE)
		leyenda = self.panel_leyenda()

		# Mostrar mapa y leyenda lado a lado
		self.console.print(Columns([mapa_panel, leyenda], equal=True, expand=True))
