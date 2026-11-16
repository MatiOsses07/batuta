"""Hook UserPromptSubmit: avisa cuando el contexto del chat supera el 50% (consolidar) o el 70% (auto-compact).
Estima el uso con el 'usage' del último mensaje del asistente (hilo principal) en el transcript. Nunca bloquea (siempre exit 0).
Config opcional por variables de entorno: ORQUESTA_VENTANA (tokens; si no se fija, se infiere del modelo),
ORQUESTA_AVISO (default 50), ORQUESTA_COMPACTA (default: CLAUDE_AUTOCOMPACT_PCT_OVERRIDE o 70)."""
import json
import os
import sys
import time

PREFIJO = chr(92) * 2 + "?" + chr(92)  # prefijo de ruta larga de Windows: \\?\
HOME = os.path.join(os.path.expanduser("~"), ".claude")
ESTADO = os.path.join(HOME, "orquesta-estado")
VENTANA_ENV = int(os.environ.get("ORQUESTA_VENTANA", "0") or 0)
AVISO = int(os.environ.get("ORQUESTA_AVISO", "50"))
AUTOCOMPACT = os.environ.get("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE")
COMPACTA = int(os.environ.get("ORQUESTA_COMPACTA") or AUTOCOMPACT or "70")
MODELOS_1M = ("claude-opus-5", "claude-sonnet-5", "claude-fable-5")  # familias con ventana de 1M
DIAS_ESTADO = 7  # se borran archivos de estado más antiguos que esto


def abrir(p):
    """Abre en binario; en Windows reintenta con prefijo largo solo si la ruta normal falla (rutas >260)."""
    p = os.path.abspath(p)
    try:
        return open(p, "rb")
    except OSError:
        if os.name == "nt" and not p.startswith(PREFIJO):
            return open(PREFIJO + p, "rb")
        raise


def leer_uso(texto):
    """(tokens, modelo) del último mensaje del asistente del hilo principal; (None, None) si no hay."""
    uso, modelo = None, None
    for line in texto.splitlines():
        if '"usage"' not in line:
            continue
        try:
            j = json.loads(line)
        except ValueError:
            continue
        m = j.get("message") or {}
        u = m.get("usage")
        if j.get("type") != "assistant" or not u or j.get("isSidechain") or m.get("model") == "<synthetic>":
            continue
        # input + cache = contexto enviado; output pasa a ser contexto del siguiente turno
        uso = sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens", "output_tokens"))
        modelo = m.get("model") or modelo
    return uso, modelo


def tokens_en_uso(path):
    """Lee la cola del transcript; si ahí no hay usage (p. ej. un tool result enorme), lee el archivo completo."""
    with abrir(path) as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(max(0, size - 400_000))
        uso, modelo = leer_uso(f.read().decode("utf-8", errors="ignore"))
        if uso is None and size > 400_000:
            f.seek(0)
            uso, modelo = leer_uso(f.read().decode("utf-8", errors="ignore"))
    return uso, modelo


def ventana(modelo, uso):
    if VENTANA_ENV:
        return VENTANA_ENV
    m = (modelo or "").lower()
    if "[1m]" in m or m.startswith(MODELOS_1M) or uso > 200_000:
        return 1_000_000
    return 200_000


def limpiar_estado():
    limite = time.time() - DIAS_ESTADO * 86400
    for n in os.listdir(ESTADO):
        p = os.path.join(ESTADO, n)
        try:
            if n.endswith(".txt") and os.path.getmtime(p) < limite:
                os.remove(p)
        except OSError:
            pass


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
        path, sid = data.get("transcript_path"), data.get("session_id") or "sin-sesion"
        if not path:
            return
        uso, modelo = tokens_en_uso(path)
        if not uso:
            return
        pct = int(uso * 100 / ventana(modelo, uso))
        banda = (pct // 5) * 5  # avisa una vez por tramo de 5 puntos
        os.makedirs(ESTADO, exist_ok=True)
        f_estado = os.path.join(ESTADO, f"{sid}.txt")
        previo = 0
        if os.path.exists(f_estado):
            previo = int(open(f_estado, encoding="utf-8").read().strip() or 0)
        else:
            limpiar_estado()
        if banda < previo:
            # bajó el contexto (compact/consolidar): rearmar para volver a avisar cuando suba
            open(f_estado, "w", encoding="utf-8").write(str(banda))
            return
        if banda < AVISO or banda == previo:
            return
        open(f_estado, "w", encoding="utf-8").write(str(banda))
        if pct >= COMPACTA:
            if AUTOCOMPACT:
                print(f"Orquesta: contexto al {pct}% (~{uso//1000}k tokens). Se compactará solo; si hay tareas largas, ejecuta /orquesta:consolidar antes.")
            else:
                print(f"Orquesta: contexto al {pct}% (~{uso//1000}k tokens). Sugiere al usuario ejecutar /orquesta:consolidar y luego /compact ya (auto-compact al {COMPACTA}% no está configurado).")
        else:
            print(f"Orquesta: contexto al {pct}% (~{uso//1000}k tokens). Sugiere al usuario ejecutar /orquesta:consolidar (o /compact) en el próximo corte natural.")
    except Exception:
        pass


main()
sys.exit(0)
