# Git Workflow Design — Starfall

**Fecha:** 2026-06-09
**Proyecto:** Starfall (Shoot 'em up 2D)
**Estado:** Aprobado

---

## Estrategia

Git Flow lite. Dos ramas permanentes más ramas de trabajo temporales por versión/tema.

---

## Ramas permanentes

| Rama | Propósito |
|------|-----------|
| `main` | Releases estables únicamente. Nunca recibe commits directos. |
| `develop` | Integración continua. Base para crear ramas de trabajo. |

---

## Ramas de trabajo (temporales)

Convención de nombre:

```
v<versión>/<descripcion-corta-en-kebab-case>
```

Ejemplos según roadmap:

```
v0.1/window-setup
v0.1/player-movement
v0.1/shooting
v0.2/enemies
v0.2/collisions
v0.3/scoring
v0.3/lives
v0.4/powerups
v0.5/boss
v1.0/menus
v1.0/audio
v1.0/highscores
```

---

## Flujo de trabajo

```
1. Crear rama desde develop:
   git checkout develop
   git checkout -b v0.x/tema

2. Trabajar y hacer commits en la rama

3. Merge a develop al completar el tema:
   git checkout develop
   git merge v0.x/tema

4. Eliminar rama de trabajo (opcional):
   git branch -d v0.x/tema

5. Al completar TODOS los temas de una versión:
   git checkout main
   git merge develop
   git tag v0.x
```

---

## Tags de release

Solo en `main`. Un tag por versión del roadmap:

```
v0.1, v0.2, v0.3, v0.4, v0.5, v1.0
```

---

## Reglas

- Nunca commit directo a `main`
- `develop` solo recibe merges de ramas `v0.x/`
- `main` solo recibe merges de `develop` al cerrar versión completa
- Una rama por grupo de cambios coherente (no mezclar temas en la misma rama)

---

## Estado inicial

```
main     ← commit inicial (CLAUDE.md, agent.md, .gitignore, spec docs)
develop  ← branched from main
```

Primera rama de trabajo se crea al iniciar v0.1.
