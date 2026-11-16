"""Hook SessionStart: inyecta las reglas de la orquesta y, si toca, avisa de revisión."""
import os
import re
import sys
from datetime import datetime, timedelta

HOME = os.path.join(os.path.expanduser("~"), ".claude")
LOG = os.path.join(HOME, "orquesta-log.jsonl")
REV = os.path.join(HOME, "orquesta-revisiones.md")
REGLAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reglas.md")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        with open(REGLAS, encoding="utf-8") as f:
            print(f.read())
    except Exception:
        pass
    try:
        if not os.path.exists(LOG):
            return
        with open(LOG, encoding="utf-8") as f:
            n = sum(1 for line in f if line.strip())
        if n == 0:
            return
        toca = n >= 20
        last = None
        if os.path.exists(REV):
            with open(REV, encoding="utf-8") as f:
                fechas = re.findall(r"\d{4}-\d{2}-\d{2}", f.read())
            if fechas:
                last = datetime.strptime(fechas[-1], "%Y-%m-%d")
        if last is None:
            last = datetime.fromtimestamp(os.path.getctime(LOG))
        if datetime.now() - last >= timedelta(days=7):
            toca = True
        if toca:
            print("Orquesta: toca revisión, ejecuta /revisar-orquesta")
    except Exception:
        pass


main()
sys.exit(0)
