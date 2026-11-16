# batuta

Marketplace de Claude Code con el plugin **orquesta**: reparte el trabajo entre subagentes con distintos modelos para gastar menos tokens sin perder calidad.

| Agente | Modelo | Para qué |
|---|---|---|
| `explorador` | Haiku | Buscar, listar, extraer, contar |
| `ejecutor` | Sonnet | Implementar con alcance claro (SQL, Python, DAX, M, Excel, correos) |
| `revisor` | Sonnet | Control de calidad de solo lectura antes de entregar |
| `analista-senior` | Opus | Diagnósticos, cuadraturas, diseño y decisiones con impacto |

Incluye además:

- **Reglas de ruteo** que se inyectan al iniciar cada sesión.
- **Log de subagentes** con tokens reales en `~/.claude/orquesta-log.jsonl` (personal, no se comparte).
- **Aviso de contexto** al 50% y 70%, y `/orquesta:consolidar` para resumir antes de compactar.
- **`/orquesta:ahorro [días]`**: costo real vs. haberlo hecho todo con Opus.
- **`/orquesta:precisar <pedido>`**: convierte un pedido en un prompt estructurado.
- **`/orquesta:revisar-orquesta`**: propone hasta 3 ajustes a partir del log.

## Instalación

Requisitos: Claude Code y Python 3 disponible como `python`.

Dentro de Claude Code:

```
/plugin marketplace add MatiOsses07/batuta
/plugin install orquesta@batuta
```

Reinicia Claude Code. Para recibir actualizaciones: `/plugin marketplace update batuta`.

Opcional (recomendado), en tu `~/.claude/settings.json`:

```json
{ "env": { "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70" } }
```

Más detalle en [orquesta/README.md](orquesta/README.md).

## Licencia

MIT
