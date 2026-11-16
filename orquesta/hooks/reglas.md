# Orquesta de agentes
## Ruteo
- Tarea mecánica, lectura o extracción -> `explorador`.
- Implementación con alcance definido -> `ejecutor`.
- Ambigüedad, diagnóstico, cuadraturas, diseño o decisiones con impacto -> `analista-senior`.
- Pasan por `revisor` solo entregables con cifras, código que toca datos o decisiones con impacto. No revisar tareas triviales.
- Loop ejecutor <-> revisor: máximo 2 vueltas; si en la segunda sigue con hallazgos, escalar a `analista-senior`.
- Escalar de rol, no de esfuerzo: si un agente falla dos veces, subir (haiku -> sonnet -> opus). Si la tarea resulta más simple, bajar.
- Lo barato recolecta, lo caro concluye: los modelos bajos nunca toman decisiones.
- Delegar solo bloques autocontenidos y grandes; no pasos triviales (cada subagente parte en frío).
- Al delegar, brief completo: objetivo, rutas exactas, restricciones y formato de salida, para que no re-explore.

## Ahorro de tokens
- Leer solo lo necesario: Grep/Glob y rangos de líneas, no archivos completos.
- No pegar de vuelta código ni archivos largos; resumir y referenciar rutas.
- Respuestas breves y directas, sin preámbulos ni recapitulaciones.
- Consultas a BD: top/limit, solo columnas necesarias, nunca tablas completas.
- Sugerir `/clear` al cambiar de tema y `/compact` cuando la conversación se alargue.
- Antes de tareas grandes, proponer un plan breve y confirmar.

## Estilo
- Responder en español, profesional y técnico, explicando brevemente el razonamiento detrás de decisiones de código y análisis.
- SQL en minúsculas (keywords y estructura).
- Correos siempre cierran con "Saludos!".
- Comentarios de indicadores/gráficos: simples, concretos y explicativos.

## Registro
- Al cerrar una tarea que usó subagentes, agrega una línea JSON a `~/.claude/orquesta-log.jsonl` (ruta del usuario) con: tarea (5 palabras), agentes usados, retrabajo (sí/no), escalamiento (sí/no y a quién) y resultado (ok/parcial/falló).

## Precisión de pedidos
- En pedidos de más de una frase o ambiguos, empieza con una línea "Entendí: [objetivo, alcance, formato de salida]" y sigue de inmediato; el usuario corrige después si hace falta.
- Pregunta antes de actuar solo si falta un dato que cambia el resultado; no preguntes lo que puedes inferir del chat o de las rutas.
- No apliques esto a mensajes cortos de continuación ("sí", "hazla", "ok") ni a preguntas simples.

## FP&A
- Si la tarea toca presupuesto, PPTO vs REAL, EBITDA, desviaciones, forecast, costo unitario, cierre mensual o presentación de cifras a gerencia: carga la skill `anthropic-skills:fpa-master` antes de delegar.
- En el brief a cada agente incluye solo lo aplicable de fpa-master: método de descomposición (precio/cantidad/mix/timing), audiencia (L1–L4) y controles a validar. No pegues la skill completa.
- `analista-senior` ya la trae precargada; `revisor` aplica los controles financieros de su definición. `ejecutor` y `explorador` no la cargan: reciben solo las instrucciones concretas.
- Si la desviación tiene causa de terreno (clima, fenología, labores, JH), sumar a `agronomo-campo` para la explicación agronómica.
