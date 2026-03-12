#!/usr/bin/env bash
# Run two programs in the language and check their results.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"

last() { "$PY" "$1" < "$2" | grep -E '.' | tail -1 | tr -d '\r'; }

rc=0
r1=$(last 04-functions/stmt3.py 04-functions/fac.st3)
if [ "$r1" = "120" ]; then echo "ok    fac.st3 -> 120"; else echo "FAIL  fac.st3 -> $r1 (expected 120)"; rc=1; fi
r2=$(last 04-functions/funex.py 04-functions/twice.fn)
if [ "$r2" = "5" ]; then echo "ok    twice.fn -> 5"; else echo "FAIL  twice.fn -> $r2 (expected 5)"; rc=1; fi

[ "$rc" -eq 0 ] && echo "PASS"
exit $rc
