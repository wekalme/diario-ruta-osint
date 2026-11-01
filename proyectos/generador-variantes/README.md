# Generador de variantes de usuario

**Ruta OSINT · Semana 2 · Python (CS50P, lecciones 0–3)**

Genera los nombres de usuario más probables de una persona a partir de su nombre, apellido y año de nacimiento: `ana.garcia`, `agarcia`, `anagarcia90`…

En una investigación OSINT, es el primer paso para buscar los perfiles de alguien en distintas plataformas.

## Uso

```bash
python generador_variantes.py
```

### Ejemplo con un año válido

```
Nombre: Ana
Apellido: García
Año de nacimiento: 1990
ana.garcia
agarcia
anagarcia
anagarcia90
1990garcia
ana.garcia90
```

### Ejemplo con un año no válido

```
Nombre: Íñigo
Apellido: Muñoz
Año de nacimiento: noventa
El año no es un número; genero las variantes sin año
inigo.munoz
imunoz
inigomunoz
```

## Qué hace

- Pasa nombre y apellido a minúsculas y quita tildes, `ü` y `ñ` (`Muñoz` → `munoz`).
- Genera siempre 3 variantes sin año.
- Si el año es válido (un número de 4 cifras, no posterior a 2026), añade 3 variantes con año.
- Si el año no es válido, avisa y continúa sin él (no vuelve a preguntar).

## Cómo lo planteé

Antes de programar, analicé el enunciado por pasos:

1. **Entrada, salida y condiciones**: qué recibe, qué devuelve y qué pasa si el año está mal.
2. **Casos límite**: año en letras (`noventa`), con 5 cifras (`19901`), futuro (`2028`), nombres con tilde y `ñ`.
3. **Resolverlo a mano**: cada variante como suma de piezas (`nombre + "." + apellido`).
4. **De palabras a herramientas**:
   - «quitar tildes» → `str.maketrans()` + `translate()`
   - «dos últimas cifras» → slicing `anio[-2:]`
   - «si el año está mal escrito» → `try` / `except ValueError` / `else`
   - «tengo que acordarme de si el año es válido» → variable interruptor (`anio_valido`)
   - «ir guardando variantes» → lista vacía + `append()`
5. **Plan en comentarios**, en cuatro fases: conseguir → comprobar → transformar → mostrar.

## Mejoras pendientes

- Controlar el nombre vacío (ahora `nombre[0]` da `IndexError`).
- Rechazar años negativos o demasiado antiguos (por ejemplo, anteriores a 1900).
- Quitar espacios en nombres compuestos (`María José` → `mariajose`).
- Más patrones: guion bajo, apellido primero, segundo apellido…
- Comprobar automáticamente si cada usuario existe en distintas plataformas.

## Uso ético

Probado solo con datos propios o de personas ficticias. Esta herramienta genera hipótesis de búsqueda a partir de información que se aporta voluntariamente; no accede a ninguna cuenta ni sistema.