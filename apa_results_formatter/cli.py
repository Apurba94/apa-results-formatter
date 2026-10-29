"""Command-line interface for apa-results-formatter."""
import argparse
import csv
import json

from .core import format_result


def _num(v):
    try:
        f = float(v)
        return int(f) if f.is_integer() and "." not in str(v) else f
    except (TypeError, ValueError):
        return v


def main(argv=None):
    ap = argparse.ArgumentParser(prog="apa-results-formatter", description="Format results in APA style.")
    ap.add_argument("input", help="JSON list or CSV with a 'test' column and statistic columns")
    ap.add_argument("--plain", action="store_true", help="no Markdown italics")
    ap.add_argument("--label", default="label", help="column/key used as a row label")
    args = ap.parse_args(argv)
    if args.input.lower().endswith(".json"):
        with open(args.input, encoding="utf-8") as fh:
            recs = json.load(fh)
    else:
        with open(args.input, encoding="utf-8-sig", newline="") as fh:
            recs = [{k: _num(v) for k, v in r.items() if v not in ("", None)} for r in csv.DictReader(fh)]
    bad = 0
    for r in recs:
        try:
            text = format_result(r, md=not args.plain)
        except (KeyError, ValueError) as exc:
            text = "ERROR: %s" % exc
            bad += 1
        label = r.get(args.label)
        print(("%s: %s" % (label, text)) if label else text)
    return 1 if bad else 0
