***Iván Ignacio Sebastián Gallardo Barría, Base de Datos II***

# Proyecto: Generador de mapa de dungeons usando OOP 

# Checklist de Desarrollo por Días

## Día 1 — Estructura del proyecto y mapa básico
- [x] Repo y entorno inicializado con **uv**.
- [x] `core.py` con clases `Habitacion` y `Mapa`.
- [x] Método `Mapa.generar_estructura(n)` implementado.
- [x] Habitación inicial ubicada en un **borde**.
- [x] `n_habitaciones ≤ ancho × alto`.
- [x] Todas las habitaciones son **accesibles** (conectividad total).
- [x] Conexiones consistentes (ida y vuelta).
- [x] `main.py` imprime datos básicos y ejemplo de conexiones.

- [x] Testeo aprobado

---

## Día 2 — Contenidos y Explorador
- [x] Clases de contenido: `ContenidoHabitacion` (abstracta), `Tesoro`, `Monstruo`, `Jefe`, `Evento`.
- [x] Clase `Objeto` creada (nombre, valor, descripción).
- [x] Clase `Explorador` creada con: mover, explorar, recibir daño, inventario, estado.
- [x] `Mapa.colocar_contenido()` reparte porcentajes:
  - [x] Al menos un jefe. (2% para que haya jefe extra) (Con estadísticas bajas para probar combate/recompensas)
  - [x] Monstruos.  (27%) (Con estadísticas bajas para probar combate/recompensas)
  - [x] Tesoros.  (15%)
  - [x] Eventos.  (10%) (Bonificación bonus aún no implementado, el resto sí)
  - [x] Resto vacías. (46%)
- [x] Dificultad y valores escalan con **distancia Manhattan**.
- [x] Reglas de combate simples (probabilidades) funcionando.

- [x] Testeo aprobado
### Post push:
- [x] Mejora del `main.py`, ahora muestra qué contenido hay en cada habitación.
- [x] Se arregló posibles_eventos, no contaba con el bonus.
- [x] Los eventos se hicieron consumibles, a excepción del bonus.

---

## Día 3 — Visualización y estadísticas
- [x] Implementar funcionalidad al bonus.
- [x] Confirmar que el contenido en habitaciones no aparezca al revisitar.
- [x] Hacer función que calcule la **distancia Manhattan**. 
- [ ] Método `obtener_estadisticas_mapa()` en `Mapa`:
  - [ ] Total de habitaciones.
  - [ ] Distribución por tipo.
  - [ ] Promedio de conexiones por habitación.
- [ ] Clase `Visualizador` con `rich`:
  - [ ] `mostrar_mapa_completo()`.
  - [ ] `mostrar_habitacion_actual()`.
  - [ ] `mostrar_minimapa()` (solo visitadas).
  - [ ] `mostrar_estado_explorador()`.

- [ ] `main.py` actualizado con demo simple.

---

## Día 4 — Serialización JSON y documentación
- [ ] `guardar_partida(mapa, explorador, archivo)` implementado.
- [ ] `cargar_partida(archivo)` reconstruye mapa y explorador.
- [ ] Serialización evita ciclos (usa coordenadas).
- [ ] Contenidos serializados con campo `"tipo"`.
- [x] Dependencia `rich` registrada en `pyproject.toml`.

---

## Día 5 — Pulido, QA y entrega final
- [ ] Restringir habitaciones a un mínimo.
- [ ] Eventos probados: trampa, fuente, portal, bonificación.
- [ ] Buffs temporales aplicados y decrementados correctamente.
- [ ] Arreglar estadísticas de monstruos/jefes.
- [ ] Estadísticas revisadas en mapas pequeños y medianos.
- [ ] Guardar/cargar probado y consistente.
- [ ] README.md completo y actualizado.
- [ ] `main.py` corre sin errores.
- [ ] Último commit con mensaje claro.
