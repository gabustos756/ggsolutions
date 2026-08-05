# Antigravity Workspace Rules — GG Solutions

## Permisos & Modo Ágil de Trabajo

### Permitido sin pedir permiso
- Leer archivos.
- Editar archivos locales.
- Crear nuevos archivos.
- Refactorizar código.
- Ejecutar comandos de build, lint, test y preview local.
- Mover o renombrar archivos dentro del workspace.

### Requiere confirmación previa
- `git add`
- `git commit`
- `git push`
- `git pull`
- `git merge`
- `git rebase`
- `git reset`
- `git checkout` (cuando cambie historia o ramas)
- `git branch -D`
- `git push --force`
- Cualquier comando que modifique historial remoto o local de forma irreversible.

### Regla Operativa
Si la acción no toca Git y no destruye datos, ejecutala sin pedir permiso. Si la acción toca Git, pedí confirmación antes de continuar.
