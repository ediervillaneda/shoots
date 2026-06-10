# Git Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Inicializar repositorio git con Git Flow lite (main + develop + ramas v0.x/tema).

**Architecture:** Repo local con dos ramas permanentes (main, develop). main recibe solo merges taggeados al cerrar versiones. develop es base para ramas de trabajo temporales nombradas v0.x/descripcion.

**Tech Stack:** Git

---

## Archivos a crear

- `.gitignore` — excluir artefactos Python, Pygame, OS y editor

---

### Task 1: Crear .gitignore

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Crear .gitignore**

```
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg
*.egg-info/
dist/
build/
.eggs/
*.whl
pip-wheel-metadata/
.venv/
venv/
env/
.env

# Pygame / game
saves/
*.log

# OS
.DS_Store
Thumbs.db
desktop.ini

# Editors
.vscode/
.idea/
*.swp
*.swo
*~
```

- [ ] **Step 2: Verificar que .gitignore existe**

```powershell
Test-Path .gitignore
```
Expected: `True`

---

### Task 2: Inicializar repositorio y commit inicial en main

**Files:**
- Modify: repo root (git init)

- [ ] **Step 1: Inicializar git**

```powershell
git init
```
Expected: `Initialized empty Git repository in F:/apps/python/shoots/.git/`

- [ ] **Step 2: Staging del commit inicial**

```powershell
git add .gitignore CLAUDE.md agent.md docs/
```

- [ ] **Step 3: Verificar staged files**

```powershell
git status
```
Expected: Los 4 ítems en "Changes to be committed". Sin archivos inesperados.

- [ ] **Step 4: Commit inicial**

```powershell
git commit -m "chore: initial project setup

Add CLAUDE.md, agent.md, .gitignore and git workflow spec/plan.
"
```

- [ ] **Step 5: Verificar commit**

```powershell
git log --oneline
```
Expected: Una línea con `chore: initial project setup`

---

### Task 3: Crear rama develop

- [ ] **Step 1: Crear y cambiar a develop**

```powershell
git checkout -b develop
```
Expected: `Switched to a new branch 'develop'`

- [ ] **Step 2: Verificar estado de ramas**

```powershell
git branch
```
Expected:
```
* develop
  main
```

---

### Task 4: Actualizar CLAUDE.md con sección de git workflow

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Agregar sección al final de CLAUDE.md**

Agregar al final del archivo:

```markdown
## Git Workflow

- `main` — releases estables, solo merges desde `develop`, taggeado (v0.1, v0.2...)
- `develop` — integración, base para crear ramas de trabajo

**Ramas de trabajo:** `v0.x/descripcion-corta` (ej: `v0.1/player-movement`)

**Flujo:**
1. `git checkout develop && git checkout -b v0.x/tema`
2. Trabajar y commitear en la rama
3. `git checkout develop && git merge v0.x/tema`
4. Al cerrar versión: `git checkout main && git merge develop && git tag v0.x`
```

- [ ] **Step 2: Commit**

```powershell
git add CLAUDE.md
git commit -m "docs: add git workflow section to CLAUDE.md"
```

---

### Task 5: Crear primera rama de trabajo

- [ ] **Step 1: Crear rama para v0.1**

```powershell
git checkout -b v0.1/window-setup
```
Expected: `Switched to a new branch 'v0.1/window-setup'`

- [ ] **Step 2: Verificar estado final**

```powershell
git branch
```
Expected:
```
* v0.1/window-setup
  develop
  main
```

- [ ] **Step 3: Verificar log desde origen**

```powershell
git log --oneline --all
```
Expected: commit inicial visible en todas las ramas.
