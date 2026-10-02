#!/usr/bin/env bash
# Regenerate TeX catalogs from generators/ JSON via Maven.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/generators"
mvn -q -DskipTests package exec:java
