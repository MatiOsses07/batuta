---
description: Revisa el log de la orquesta de agentes y propone máximo 3 ajustes (sin aplicar nada sin aprobación)
---

Revisa la orquesta de agentes. Trabaja solo en `~\.claude\` (log y revisiones) y en los agentes del plugin (`${CLAUDE_PLUGIN_ROOT}\agents\`).

1. Lee `orquesta-log.jsonl`, `${CLAUDE_PLUGIN_ROOT}\agents\{explorador,ejecutor,analista-senior,revisor}.md` y `${CLAUDE_PLUGIN_ROOT}\hooks\reglas.md` (en lugar de CLAUDE.md).
   - El log mezcla dos tipos de línea: `"origen":"hook"` (automática: fecha, proyecto, session_id, agente, salida) y líneas manuales del orquestador (tarea, agentes, retrabajo, escalamiento, resultado). Cruza ambas por fecha/session_id. Ignora líneas con `error` salvo para reportarlas.
2. Si hay menos de 10 entradas: dilo, muestra el conteo y termina sin proponer cambios (datos insuficientes).
3. Calcula por agente: nº de usos, % con retrabajo, % con escalamiento, % resultado ok (tabla corta).
4. Detecta patrones: retrabajo repetido en un agente; tareas del mismo tipo que siempre escalan; tareas que el orquestador hizo solo y salieron mal; revisor que aprueba y luego falla.
5. Propón MÁXIMO 3 cambios, uno por variable, cada uno como diff exacto (archivo, antes → después) con la evidencia del log. Si `reglas.md` supera 60 líneas, propón qué regla eliminar o condensar.
6. NO apliques nada sin mi aprobación explícita. Al aprobar: respaldo `.bak` del archivo y luego aplicar.
7. Al terminar (haya o no cambios aprobados): agrega una línea a `orquesta-revisiones.md` con `AAAA-MM-DD | hallazgos | cambios aplicados`, y mueve las entradas revisadas de `orquesta-log.jsonl` a `orquesta-log.archivo.jsonl` (el log activo debe quedar vacío o solo con entradas posteriores).

Respuestas breves, en español.
