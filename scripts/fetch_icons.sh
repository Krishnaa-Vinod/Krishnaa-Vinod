#!/usr/bin/env bash
# ───────────────────────────────────────────────────────────────
# fetch_icons.sh — Download raw SVGs from Simple Icons & Octicons
# ───────────────────────────────────────────────────────────────
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

SI_DIR="$REPO_ROOT/assets/raw/simpleicons"
OC_DIR="$REPO_ROOT/assets/raw/octicons"

mkdir -p "$SI_DIR" "$OC_DIR"

# ── Simple Icons (skills + social) ────────────────────────────
SI_SLUGS=(
  python cplusplus pytorch opencv ros
  docker linux git numpy
  linkedin googlescholar
)

SI_BASE="https://cdn.jsdelivr.net/npm/simple-icons@latest/icons"

echo "Downloading Simple Icons SVGs..."
for slug in "${SI_SLUGS[@]}"; do
  printf "  %-20s" "$slug"
  if curl -fsSL "$SI_BASE/${slug}.svg" -o "$SI_DIR/${slug}.svg" 2>/dev/null; then
    echo "OK"
  else
    echo "FAILED (trying simpleicons.org fallback)"
    curl -fsSL "https://simpleicons.org/icons/${slug}.svg" \
      -o "$SI_DIR/${slug}.svg" || echo "  !! Could not download $slug"
  fi
done

# ── Octicons mail icon ────────────────────────────────────────
echo ""
echo "Downloading Octicons mail icon..."
curl -fsSL \
  "https://raw.githubusercontent.com/primer/octicons/main/icons/mail-16.svg" \
  -o "$OC_DIR/mail-16.svg" && echo "  mail-16  OK" || echo "  mail-16  FAILED"

echo ""
echo "Done. Raw SVGs saved to assets/raw/"
