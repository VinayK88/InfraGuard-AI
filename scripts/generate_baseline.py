import json
from pathlib import Path

from infraguard.report import build_report

OUTPUT = Path("reports/baseline.json")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(build_report(), indent=2), encoding="utf-8")
print(OUTPUT)
