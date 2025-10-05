***Iván Ignacio Sebastián Gallardo Barría, Base de Datos II***

# Proyecto: Generador de mapa de dungeons usando OOP 

## Instrucciones de ejecución
Se descargan los archivos del repositorio con su(s) dependencia(s) correspondiente(s). Dejar el `main.py` fuera de la carpeta `dungeon_generator/` y ejecutar el mismo `main.py`.

## Diseño e Implementación
Mi generador de dungeons trata de ser sencillo y modular. El mapa se expande de forma aleatoria y con conexiones que hacen verlo "ramificado". Se decora el mapa con contenidos `(Tesoros, Monstruos, Jefes, Eventos)` con porcentajes `15%, 27%, 2% y 10%` respectivamente, el resto son salas vacías. El valor de los tesoros como la dificultad escala según distancia Manhattan entre sala actual y sala inicio. El `Explorador` posee vida, inventario y posición, además de un sistema de bonificación de daño. Para la visualización se usa la librería `rich`. 

## Cumplimiento de los requerimientos de la tarea

|  # | Requerimiento                                              | Estado          | Observación                                                                                                                                           |
| -: | ---------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
|  1 | Clase `Habitacion` y sus atributos                         | **Cumplido**    | [No hay observación]                                                                                                                                  |
|  2 | Clase `Mapa` con lo solicitado                             | **Parcial**     | La cantidad de habitaciones / tamaño del mapa siguen siendo datos que el usuario no puede cambiar. Se trabajará en ello.                              |
|  3 | Clase `Objeto` con atributos                               | **Cumplido**    | [No hay observación]                                                                                                                                  |
|  4 | Clase `Explorador` con sus atributos                       | **Cumplido**    | [No hay observación]                                                                                                                                  |
|  5 | Clase abstracta `ContenidoHabitacion` y sus hijas          | **Cumplido**    | Se agregaron 3 jefes (con sus recompensas) y 3 monstruos. Para los tesoros se agregaron 5 objetos distintos.                                          |
|  6 | Reglas de distribución                                     | **Cumplido**    | [No hay observación]                                                                                                                                  |
|  7 | `obtener_estadisticas_mapa()`                              | **Cumplido**    | [No hay observación]                                                                                                                                  |
|  8 | Guardado/Cargado de partidas con JSON                      | **No cumplido** | Se trabajará en ello.                                                                                                                                 |
|  9 | Clase `Visualizador`                                       | **Parcial**     | Para un mejor manejo de la librería `rich` se requirió apoyo de compañeros y herramientas de IA.                                                      |
| 10 | Eventos aleatorios                                         | **Cumplido**    | No era parte del requerimiento pero ahora portales, trampas y fuentes son consumibles. La bonificación dura distancia Manhattan entre sala del evento e inicio. |
| 11 | Sistema de dificultad escalable                            | **Cumplido**    | El bonus de ataque enemigo es `distancia // 3`; la vida aumenta `distancia // 2`. Los tesoros suben su valor en `distancia`.                          |


## Checklist de Desarrollo por días

### Día 1 — Estructura del proyecto y mapa básico
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

### Día 2 — Contenidos y Explorador
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
#### Post push:
- [x] Mejora del `main.py`, ahora muestra qué contenido hay en cada habitación.
- [x] Se arregló posibles_eventos, no contaba con el bonus.
- [x] Los eventos se hicieron consumibles, a excepción del bonus.

---

### Día 3 — Visualización y estadísticas
- [x] Implementar funcionalidad al bonus.
- [x] Confirmar que el contenido en habitaciones no aparezca al revisitar.
- [x] Hacer función que calcule la **distancia Manhattan**. 
- [x] Método `obtener_estadisticas_mapa()` en `Mapa`:
  - [x] Total de habitaciones.
  - [x] Distribución por tipo.
  - [X] Promedio de conexiones por habitación.
- [x] Clase `Visualizador` con `rich`:
  - [x] `mostrar_mapa_completo()`.
  - [x] `mostrar_habitacion_actual()`.
  - [ ] `mostrar_minimapa()` (solo visitadas con color).
  - [ ] `mostrar_estado_explorador()`.
- [ ] Arreglar lógica de movimiento, hacerla más intuitiva.

- [ ] `main.py` actualizado con demo simple.

---

### Día 4 — Serialización JSON y documentación
- [ ] `guardar_partida(mapa, explorador, archivo)` implementado.
- [ ] `cargar_partida(archivo)` reconstruye mapa y explorador.
- [ ] Contenidos serializados con campo `"tipo"`.
- [x] Dependencia `rich` registrada en `pyproject.toml`.

---

### Día 5 — Pulido, QA y entrega final
- [ ] Restringir habitaciones/tamaño de mapa a un mínimo.
- [x] Eventos probados: trampa, fuente, portal, bonificación.
- [ ] Arreglar estadísticas de monstruos/jefes.
- [x] Estadísticas revisadas en mapas pequeños y medianos.
- [ ] Guardar/cargar probado y consistente.
- [ ] README.md completo y actualizado.
- [ ] `main.py` corre sin errores.
- [ ] Último commit.
