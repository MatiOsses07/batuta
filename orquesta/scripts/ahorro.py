"""Informe de tokens y ahorro estimado de la orquesta. Uso: python ahorro.py [dias=30]
Lee ~/.claude/orquesta-log.jsonl y orquesta-log.archivo.jsonl. Costo real = tokens medidos al precio de cada modelo;
costo de referencia = esos mismos tokens al precio del modelo de referencia (datos/precios.json)."""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.join(os.path.expanduser("~"), ".claude")
CAMPOS = ("entrada", "salida", "cache_lectura", "cache_escritura")


def precio_de(modelo, tabla):
    """claude-haiku-4-5-20251001 -> precios de claude-haiku-4-5 (coincidencia por prefijo)."""
    if not modelo:
        return None
    for clave, p in tabla.items():
        if modelo.startswith(clave):
            return p
    return None


def costo(tokens, p):
    return sum(tokens.get(c, 0) * p[c] for c in CAMPOS) / 1_000_000


def main():
    dias = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    desde = datetime.now().astimezone() - timedelta(days=dias)
    with open(os.path.join(RAIZ, "datos", "precios.json"), encoding="utf-8") as f:
        precios = json.load(f)
    tabla, ref = precios["modelos"], precios["referencia"]
    p_ref = tabla[ref]

    vistos, filas, sin_dato = set(), defaultdict(lambda: defaultdict(float)), 0
    for nombre in ("orquesta-log.jsonl", "orquesta-log.archivo.jsonl"):
        ruta = os.path.join(HOME, nombre)
        if not os.path.exists(ruta):
            continue
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                try:
                    e = json.loads(linea)
                except ValueError:
                    continue
                if e.get("origen") != "hook" or e.get("error") or not e.get("agente"):
                    continue
                clave = e.get("agent_id") or (e.get("fecha"), e.get("agente"))
                if clave in vistos:
                    continue
                vistos.add(clave)
                try:
                    if datetime.fromisoformat(e["fecha"]) < desde:
                        continue
                except Exception:
                    continue
                t, p = e.get("tokens"), precio_de(e.get("modelo"), tabla)
                if not t or not p:
                    sin_dato += 1
                    continue
                fila = filas[e["agente"].split(":")[-1]]
                fila["usos"] += 1
                for c in CAMPOS:
                    fila[c] += t.get(c, 0)
                fila["real"] += costo(t, p)
                fila["ref"] += costo(t, p_ref)

    if not filas:
        print(f"Sin datos medidos en los últimos {dias} días ({sin_dato} entradas sin tokens o con modelo desconocido).")
        return
    print(f"Ahorro de la orquesta, últimos {dias} días (referencia: {ref})\n")
    print(f"{'agente':<16}{'usos':>5}{'tokens (K)':>12}{'real USD':>10}{'ref USD':>9}{'ahorro USD':>12}{'%':>6}")
    tot = defaultdict(float)
    for ag, fila in sorted(filas.items()):
        tk = sum(fila[c] for c in CAMPOS)
        ah = fila["ref"] - fila["real"]
        pct = ah / fila["ref"] * 100 if fila["ref"] else 0
        print(f"{ag:<16}{int(fila['usos']):>5}{tk/1000:>12,.0f}{fila['real']:>10.2f}{fila['ref']:>9.2f}{ah:>12.2f}{pct:>6.0f}")
        tot["usos"] += fila["usos"]
        tot["real"] += fila["real"]
        tot["ref"] += fila["ref"]
        tot["tok"] += tk
    ah = tot["ref"] - tot["real"]
    pct = ah / tot["ref"] * 100 if tot["ref"] else 0
    print(f"{'TOTAL':<16}{int(tot['usos']):>5}{tot['tok']/1000:>12,.0f}{tot['real']:>10.2f}{tot['ref']:>9.2f}{ah:>12.2f}{pct:>6.0f}")
    print(f"\nTokens procesados fuera de tu chat principal: {tot['tok']/1000:,.0f}K (estimación del contexto que no lo llenó).")
    if sin_dato:
        print(f"Excluidas {sin_dato} entradas sin tokens medidos (registradas antes de v1.2.0 o modelo sin precio).")
    print("Nota: el ahorro es una estimación; supone que el modelo de referencia habría gastado los mismos tokens.")


main()
