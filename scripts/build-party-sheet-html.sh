#!/usr/bin/env bash
# Build party-sheet.html → party-sheet-alt.pdf with WeasyPrint.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/party-sheet.html"
OUT="$ROOT/party-sheet-alt.pdf"

if ! command -v weasyprint >/dev/null; then
  echo "weasyprint is required" >&2
  exit 1
fi

weasyprint "$SRC" "$OUT"
echo "Wrote $OUT"
pdfinfo "$OUT" 2>/dev/null | awk '/^Pages:/ {print}' || true
