# Git · Apuntes

Lo que he aprendido de Git en la ruta OSINT (S01–S04), con mis propias dudas y errores.

---

## 1. El modelo mental

| Concepto | Qué es |
|---|---|
| **Commit** | Una **foto de todo el proyecto** en un momento dado. Guarda: los archivos, el autor y la fecha, el mensaje y un enlace a su commit **padre**. Se identifica con un **hash** (`a04c464`). |
| **Rama** | Solo una **etiqueta** que apunta a un commit. Avanza sola cuando hago un commit estando en ella. |
| **HEAD** | **Dónde estoy yo ahora.** Normalmente apunta a una rama. |
| **`origin/main`** | Lo que mi ordenador **recuerda** de la rama `main` de GitHub la última vez que habló con él. No se actualiza sola. |

> Un commit **no modifica** los archivos: solo guarda una versión. Los archivos los cambio yo al editarlos.

---

## 2. El ciclo básico

```
editar y GUARDAR  →  git add  →  git commit  →  git push
```

| Comando | Qué hace |
|---|---|
| `git init` | Convierte la carpeta actual en un repositorio (crea la carpeta oculta `.git`). |
| `git status` | Qué ha cambiado: en **rojo**, cambios sin preparar; en **verde**, preparados para el commit. |
| `git add archivo` | Prepara ese archivo para el próximo commit. |
| `git add .` | Prepara todos los cambios de la carpeta (revisar antes con `git status`). |
| `git add diario/S01.md` | Para archivos de una subcarpeta, se indica la ruta. |
| `git commit -m "mensaje"` | Guarda la foto con un mensaje. |
| `git commit -am "mensaje"` | `add` + `commit` a la vez, pero **solo** de archivos que Git ya seguía. |

**Un commit es del proyecto entero, no de un archivo.** No hace falta "moverse" a ningún archivo: con `git add` elijo qué cambios entran en la foto.

**Mensajes de commit:** verbo en imperativo y concreto.
- ✔️ `Añadir diario de la S02` · `Corregir enlace del README`
- ✘ `cambios` · `Actualización archivos de la s2`

---

## 3. Ver el historial

```bash
git log --oneline --graph --all
```

- `--oneline` → un commit por línea.
- `--graph` → dibuja las ramas con líneas.
- `--all` → todas las ramas, también las remotas (`origin/main`).

Otros:
- `git show HASH:archivo` → cómo era un archivo en un commit concreto.
- `git log --oneline -- archivo` → solo los commits que tocaron ese archivo.

---

## 4. Ramas y fusiones

| Comando | Qué hace |
|---|---|
| `git branch nombre` | **Crea** una rama, pero **no me mueve** a ella. |
| `git checkout nombre` / `git switch nombre` | Me **mueve** a esa rama. |
| `git checkout -b nombre` | Crea la rama y me mueve a ella. |
| `git branch -m main` | **Renombra** la rama actual (`-m` = *move*). |
| `git merge rama` | Trae los cambios de `rama` a la rama en la que estoy. |
| `git rebase rama` | Copia mis commits **encima** de `rama` (historia en línea recta). |

> Fijarme siempre en el prompt: `(main)` o `(feature)` me dice en qué rama estoy.

### Tres situaciones al unir ramas

| Situación | Qué hace Git |
|---|---|
| `main` está detrás, en el mismo camino | **Fast-forward**: solo mueve la etiqueta. Sin commit nuevo. |
| Las ramas se han separado + `merge` | Crea un **commit de fusión** con dos padres. |
| Las ramas se han separado + `rebase` | **Copia** mis commits encima → hashes nuevos, historia lineal. |

**¿Por qué cambian los hashes al copiar un commit (rebase, cherry-pick)?** Porque el hash se calcula con todo lo que guarda el commit. Al copiarlo cambia el padre y/o la fecha del *committer*, así que es un commit nuevo aunque parezca idéntico.

---

## 5. Conflictos

Pasan cuando dos ramas cambian la **misma zona** de un archivo. Ojo: dos líneas **seguidas** cuentan como la misma zona, aunque sean distintas.

```
<<<<<<< HEAD
lo que hay en mi rama
=======
lo que viene de la otra rama
>>>>>>> otra-rama
```

**Regla de oro:** después de un `CONFLICT`, el siguiente paso es **abrir el archivo**. Nunca `add` directamente.

1. Abrir el archivo y dejar el contenido como debe quedar.
2. **Borrar los marcadores** `<<<<<<<`, `=======` y `>>>>>>>`.
3. Comprobar que no queda ninguno: `grep "<<<<<<<" archivo` no debe mostrar nada.
4. Continuar:

| Si estaba haciendo... | Para seguir |
|---|---|
| `merge` | `git add archivo` + `git commit` |
| `rebase` | `git add archivo` + `git rebase --continue` |
| `revert` | `git add archivo` + `git revert --continue` |

> `git add` **no comprueba** si he quitado los marcadores. Me pasó varias veces en la S01.

Para cancelar: `git merge --abort` · `git rebase --abort`.

---

## 6. Deshacer cambios

| Comando | Qué hace | Cuándo |
|---|---|---|
| `git reset HEAD~1` | Deshace el commit, pero **conserva** los cambios en el archivo. | Me equivoqué en el commit, no en el trabajo. |
| `git reset --hard HASH` | Vuelve a ese commit y **borra** todo lo posterior, también del archivo. | Con mucho cuidado: no se recupera. |
| `git revert HASH` | Crea un commit **nuevo** que anula otro. | Si el commit ya está subido a GitHub. |
| `git restore archivo` | Descarta los cambios no guardados en un commit. | Volver a la última versión guardada. |

**Ojo con el argumento:**
- En `reset`, el argumento es **a dónde vuelvo**: `git reset HEAD~1`.
- En `revert`, es **qué commit deshago**: `git revert HEAD`.

> **Nunca reescribir (reset, rebase) commits que ya están en GitHub** y que otras personas pueden tener. Para lo ya publicado: `revert`.

---

## 7. Moverse por la historia

| Referencia | Significa |
|---|---|
| `HEAD` | El commit donde estoy |
| `main^` | El padre de `main` (uno atrás) |
| `main~3` | Tres commits atrás (`~` va seguido de un **número**, no de un hash) |
| `git checkout HASH` | Ir a un commit concreto → *detached HEAD* |

**Detached HEAD:** HEAD apunta a un commit, no a una rama. El prompt muestra un hash, como `((524486d...))`. Los commits que haga aquí no pertenecen a ninguna rama: si quiero conservarlos, `git switch -c nombre-rama`.

---

## 8. Cherry-pick

```bash
git cherry-pick HASH
```

Copia **un solo commit concreto** de otra rama a la rama actual, sin traerse el resto.

---

## 9. Limpiar commits antes de subir: rebase interactivo

```bash
git rebase -i HEAD~4
```

Abre la lista de los 4 últimos commits, **del más antiguo (arriba) al más reciente (abajo)**. Delante de cada uno, una acción:

| Acción | Qué hace |
|---|---|
| `pick` | Dejarlo como está (hace de **base**) |
| `squash` / `s` | Juntarlo con el de **arriba** y elegir el mensaje |
| `fixup` | Juntarlo con el de arriba, descartando su mensaje |
| `reword` | Cambiar solo su mensaje |
| `drop` | Eliminarlo |

Para juntar 4 en 1: el primero `pick` y los otros tres `s`.

> Solo con commits que **todavía no he subido**.

---

## 10. Trabajar con GitHub (remoto)

### Conectar un repositorio nuevo (solo la primera vez)

1. En GitHub, crear un repositorio **vacío** (sin README).
2. En la terminal, dentro de la carpeta:

```bash
git remote add origin https://github.com/wekalme/REPO.git
git push -u origin main
```

| Parte | Significa |
|---|---|
| `remote add` | Añadir un remoto |
| `origin` | El apodo estándar del remoto |
| `-u` | *Upstream*: conecta mi `main` con la de GitHub y lo recuerda. Después basta con `git push` y `git pull`. |
| `origin main` | **A dónde** (remoto) + **qué** (rama). Siempre en ese orden. |

Comprobar la conexión: `git remote -v`.

### Comandos

| Comando | Qué hace |
|---|---|
| `git push` | Sube mis commits |
| `git fetch` | **Solo descarga** los cambios y actualiza `origin/main`. No toca mi `main`. |
| `git pull` | `fetch` + `merge` (crea commit de fusión si hace falta) |
| `git pull --rebase` | `fetch` + `rebase` (historia lineal) |
| `git merge origin/main` | Unir la rama remota después de un `fetch` (se escribe con barra, como una sola palabra) |
| `git clone URL` | Copiar un repositorio de GitHub a mi ordenador |

### ¿Por qué GitHub rechaza un `push`?

```
! [rejected]  main -> main (fetch first)
```

Porque GitHub tiene commits que yo no tengo. `push` le pide a GitHub que **mueva su etiqueta `main`** hasta mi commit, y GitHub solo lo acepta si es un **fast-forward** (mi commit está justo delante del suyo, sin perder nada). Si las ramas se han separado, primero tengo que traer sus cambios y unirlos.

**Solución:**
1. `git fetch` → miro el gráfico para ver la bifurcación.
2. `git merge` (o `git rebase origin/main`).
3. Resolver conflictos si los hay.
4. `git push`.

> Truco: `git status` puede decir *"up to date with origin/main"* aunque GitHub tenga cambios nuevos, porque `origin/main` es solo lo que mi ordenador **recuerda**. Para saberlo de verdad: `git fetch`.

---

## 11. Configuración (una sola vez por ordenador)

```bash
git config --global user.name "Mi Nombre"
git config --global user.email "mi@email.com"
git config --global init.defaultBranch main   # repos nuevos empiezan en main
git config --global pull.rebase true          # opcional: pull hace rebase por defecto
git config --global --list                    # ver la configuración
```

`user.name` es el nombre que aparece como autora; GitHub me reconoce por el **email**.

---

## 12. Salir de sitios donde me he quedado "atrapada"

| Situación | Cómo se reconoce | Cómo salir |
|---|---|---|
| **Paginador** (log largo) | `:` en la última línea | `q` |
| **Vim** (commit sin `-m`, merge, rebase) | Pantalla con `~` a la izquierda | `Esc` → `:wq` → `Intro` (guardar y salir) |
| Vim: escribir | — | `i` para escribir, `Esc` para dejar de escribir |
| Vim: salir sin guardar | — | `Esc` → `:q!` → `Intro` |
| Vim en rebase interactivo: **cancelar** | — | `Esc` → `:cq` → `Intro` |

---

## 13. Errores que me han pasado

| Error / situación | Causa | Solución |
|---|---|---|
| `fatal: not a git repository` | No estoy dentro de la carpeta del repositorio, o no he hecho `git init`. | `cd carpeta` (mirar el prompt) o `git init`. |
| `nothing to commit, working tree clean` | No he cambiado nada, o no he **guardado** el archivo. | Editar, Ctrl + S, y volver a `add`. |
| `pathspec 'archivo' did not match any files` | El archivo no existe (o está en otra carpeta). | Crearlo, o indicar la ruta (`diario/S01.md`). |
| `fatal: 'main' does not appear to be a git repository` | Escribí `git push main`: Git tomó `main` como remoto. | `git push` o `git push origin main`. |
| Commit hecho en la rama equivocada | `git branch` crea la rama, pero no me mueve a ella. | Moverme antes con `git switch`. |
| Marcadores `<<<<<<<` subidos | `add` justo después del conflicto, sin editar. | Abrir el archivo, quitar marcadores, commit nuevo. |
| `revert` del commit equivocado | Confundí el argumento de `revert` con el de `reset`. | En `revert`: el commit a deshacer (`HEAD` si es el último). |
| Conflicto aunque cambié líneas distintas | Eran líneas **seguidas**: Git las trata como la misma zona. | Resolverlo como cualquier conflicto. |

---

## 14. Seguridad

- **Antes de `git add .`, siempre `git status`**, para ver qué entra.
- **Nunca subir contraseñas, claves de API ni tokens.** Para que Git ignore archivos, se listan en un archivo **`.gitignore`**.
- En repositorios públicos: nada de soluciones de los *problem sets* de CS50 ni contraseñas de Bandit.