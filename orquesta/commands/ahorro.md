---
description: Muestra tokens consumidos por la orquesta y el ahorro estimado frente a Opus 5.5
argument-hint: "[días, por defecto 30]"
---

Ejecuta `python "${CLAUDE_PLUGIN_ROOT}/scripts/ahorro.py" $ARGUMENTS` y muestra la tabla tal cual, sin recalcular.

Luego agrega máximo 3 líneas: qué agente aporta más ahorro, si el revisor o el retrabajo se comen parte del ahorro, y la advertencia de que el ahorro es una estimación (supone los mismos tokens con Opus 5.5). Si hay entradas excluidas por no tener tokens, dilo.

Respuesta breve, en español.
