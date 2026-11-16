# Plugin orquesta

Agentes (`explorador`, `ejecutor`, `analista-senior`, `revisor`), reglas de ruteo, log automático de subagentes y comando `/revisar-orquesta`.

## Requisitos
- Claude Code y Python 3 en el PATH (comando `python`).

## Instalación
- Prueba rápida sin instalar: `claude --plugin-dir <ruta>/orquesta`
- Para el equipo: publicar la carpeta en un repo Git y agregarla como marketplace
  (`/plugin marketplace add MatiOsses07/batuta` y luego `/plugin install orquesta@batuta`).

## Qué hace
- **SessionStart**: inyecta las reglas de `hooks/reglas.md` y avisa si toca revisión (≥20 entradas o ≥7 días).
- **SubagentStop**: registra cada subagente en `~/.claude/orquesta-log.jsonl` (local de cada persona).
- **/revisar-orquesta**: propone máx. 3 ajustes con evidencia del log, sin aplicar nada sin aprobación.

## Consolidador de contexto
- **UserPromptSubmit** (`hooks/contexto.py`): estima el uso de contexto y avisa al 50% (sugiere consolidar) y al 70%. Infiere la ventana del modelo (1M para Opus/Sonnet/Fable 5 o ids `[1m]`; 200k el resto), ignora subagentes y mensajes sintéticos, y vuelve a avisar después de compactar. Config opcional: `ORQUESTA_VENTANA` (fuerza la ventana), `ORQUESTA_AVISO`, `ORQUESTA_COMPACTA` (default: `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` o 70). Borra estados de sesión de más de 7 días.
- **/orquesta:consolidar**: genera un resumen estructurado y lo guarda en `~/.claude/consolidados/`.
- **Auto-compact al 70%**: un plugin no puede fijarlo; cada persona agrega en su `settings.json`: `"env": { "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70" }`.

## Medidor de ahorro
- `log_subagente.py` guarda los tokens reales de cada subagente (entrada, salida, caché).
- **/orquesta:ahorro [días]**: tabla por agente con costo real, costo de referencia (Opus 5.5) y ahorro estimado. Precios editables en `datos/precios.json`.
- El ahorro es una estimación: supone que Opus 5.5 habría gastado los mismos tokens.

## Precisión de pedidos
- Regla en `reglas.md`: Claude abre con "Entendí: …" en pedidos largos o ambiguos y sigue de inmediato.
- **/orquesta:precisar <pedido>**: devuelve un prompt estructurado para revisarlo antes de enviarlo.

## Notas
- El log y las revisiones son personales; no se comparten.
- Al actualizar el plugin se sobrescriben agentes y reglas; sube al repo los ajustes aprobados en las revisiones.
