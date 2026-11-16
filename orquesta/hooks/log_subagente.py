"""Hook SubagentStop: agrega una línea JSON a orquesta-log.jsonl. Nunca bloquea (siempre exit 0)."""
import json
import os
import sys
import time
from datetime import datetime

HOME = os.path.join(os.path.expanduser("~"), ".claude")
LOG = os.path.join(HOME, "orquesta-log.jsonl")


def append(entry):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def long_path(p):
    # Windows: rutas >260 caracteres requieren el prefijo \\?\
    p = os.path.abspath(p)
    return p if p.startswith("\\\\?\\") or os.name != "nt" else "\\\\?\\" + p


def leer_transcript(path):
    """Devuelve (modelo, tokens) del transcript del subagente. tokens suma input/output/cache por mensaje
    del asistente (una vez por id de mensaje). (None, None) si no hay ruta."""
    if not path:
        return None, None
    modelo = None
    por_id = {}
    with open(long_path(path), encoding="utf-8") as f:
        for n, line in enumerate(f):
            if '"assistant"' not in line:
                continue
            try:
                j = json.loads(line)
            except ValueError:
                continue
            if j.get("type") != "assistant":
                continue
            m = j.get("message") or {}
            modelo = m.get("model") or modelo
            u = m.get("usage")
            if u:
                por_id[m.get("id") or f"linea{n}"] = u  # el último registro del mensaje es el completo
    tokens = {"entrada": 0, "salida": 0, "cache_lectura": 0, "cache_escritura": 0}
    for u in por_id.values():
        tokens["entrada"] += u.get("input_tokens") or 0
        tokens["salida"] += u.get("output_tokens") or 0
        tokens["cache_lectura"] += u.get("cache_read_input_tokens") or 0
        tokens["cache_escritura"] += u.get("cache_creation_input_tokens") or 0
    return modelo, (tokens if por_id else None)


def main():
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
        # Subagentes internos de la app llegan sin nombre y sin transcript: no son de la orquesta.
        if not data.get("agent_type"):
            sys.exit(0)
        entry = {
            "origen": "hook",
            "fecha": now,
            "proyecto": data.get("cwd"),
            "session_id": data.get("session_id"),
            "agente": data.get("agent_type"),
            "agent_id": data.get("agent_id"),
            "modelo": None,
            "tokens": None,
        }
        # El transcript puede no existir aún al disparar el hook: reintentar solo si falta el archivo.
        for intento in range(3):
            try:
                entry["modelo"], entry["tokens"] = leer_transcript(data.get("agent_transcript_path"))
                entry.pop("modelo_error", None)
                break
            except FileNotFoundError as e:
                entry["modelo_error"] = f"{type(e).__name__}: {e}"
                if intento < 2:
                    time.sleep(0.5)
            except Exception as e:
                entry["modelo_error"] = f"{type(e).__name__}: {e}"
                break
        append(entry)
    except Exception as e:
        try:
            append({"origen": "hook", "fecha": now, "error": f"{type(e).__name__}: {e}"})
        except Exception:
            pass
    sys.exit(0)


main()
