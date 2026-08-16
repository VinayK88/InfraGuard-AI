from __future__ import annotations

import argparse
import json
from pathlib import Path

from .report import build_report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="infraguard")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("evaluate", help="Evaluate the deterministic assurance baseline")

    report = subcommands.add_parser("report", help="Write the full assurance report")
    report.add_argument("--output", default="reports/local-report.json")
    return parser


def main() -> int:
    args = _parser().parse_args()
    report = build_report()
    summary = report["summary"]

    if args.command == "evaluate":
        print(
            f"Mission resilience: {report['mission_resilience_score']:.1f}/100\n"
            f"Scenarios contained: {summary['contained']}/{summary['scenarios']}\n"
            f"Unsafe actions blocked: {summary['unsafe_actions_blocked']}\n"
            f"Provenance health: {report['provenance_health']:.1%}"
        )
        return 0 if summary["contained"] == summary["scenarios"] else 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
