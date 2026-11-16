---
description: Consolida el contexto del chat en un resumen estructurado para continuar tras /clear o /compact
---

Consolida este chat para liberar contexto sin perder el hilo.

1. Redacta un resumen de máximo 40 líneas con estas secciones: **Objetivo**, **Decisiones tomadas** (con el porqué), **Estado actual**, **Archivos y rutas tocados** (rutas exactas), **Hallazgos y cifras clave**, **Pendientes / próximo paso**, **Restricciones y preferencias del usuario**.
2. Incluye solo lo necesario para retomar: sin código largo ni logs, referencia rutas en vez de pegar contenido.
3. Guárdalo en `~\.claude\consolidados\AAAA-MM-DD_HHMM.md` (crea la carpeta si no existe).
4. Termina indicando: "Ejecuta `/clear` y pega el contenido de ese archivo (o dime su ruta) para continuar" o, si prefieres, `/compact`.

Respuesta breve, en español. No ejecutes `/clear` ni `/compact` tú mismo.
