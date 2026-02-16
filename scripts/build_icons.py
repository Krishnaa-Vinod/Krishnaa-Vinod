#!/usr/bin/env python3
"""
build_icons.py — Generate uniform skill (42×42) and social (18px) SVGs
from downloaded raw Simple Icons / Octicons SVGs.

Palette
  Background : #21342E
  Border     : #2C4A42
  Icon fill  : #DCE7E2
"""

import re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────
REPO   = Path(__file__).resolve().parent.parent
RAW_SI = REPO / "assets" / "raw" / "simpleicons"
RAW_OC = REPO / "assets" / "raw" / "octicons"
OUT_SOCIAL = REPO / "assets" / "generated" / "social"
OUT_SKILLS = REPO / "assets" / "generated" / "skills"

# ── Palette ────────────────────────────────────────────────────
BG     = "#21342E"
BORDER = "#2C4A42"
FILL   = "#DCE7E2"

# ── Dimensions ─────────────────────────────────────────────────
SKILL_SIZE    = 42
SKILL_PADDING = 9        # (42 − 24) / 2
SKILL_RX      = 8
SOCIAL_SIZE   = 18

# ── What to build ──────────────────────────────────────────────
SKILL_SLUGS = [
    "python", "cplusplus", "pytorch", "opencv", "ros",
    "docker", "linux", "git", "numpy",
]

SOCIAL_SPECS = {
    "linkedin":      ("simpleicons", "linkedin"),
    "googlescholar": ("simpleicons", "googlescholar"),
    "mail":          ("octicons",    "mail-16"),
}


# ── Helpers ────────────────────────────────────────────────────
def extract_paths(svg: str) -> list[str]:
    """Return every d-attribute from <path .../> elements."""
    return re.findall(r'<path[^>]*?\bd="([^"]+)"[^>]*/?>',  svg, re.DOTALL)


def extract_viewbox(svg: str) -> tuple[float, float, float, float]:
    m = re.search(r'viewBox="([^"]+)"', svg)
    parts = (m.group(1) if m else "0 0 24 24").split()
    return tuple(float(p) for p in parts)          # type: ignore[return-value]


# ── Generators ─────────────────────────────────────────────────
def social_svg(paths: list[str], vb: tuple) -> str:
    vb_str = " ".join(str(v) for v in vb)
    inner  = "\n".join(f'  <path d="{d}" fill="{FILL}"/>' for d in paths)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SOCIAL_SIZE}" height="{SOCIAL_SIZE}" '
        f'viewBox="{vb_str}">\n{inner}\n</svg>\n'
    )


def skill_svg(paths: list[str], vb: tuple) -> str:
    _, _, vw, vh = vb
    inner = SKILL_SIZE - 2 * SKILL_PADDING
    scale  = min(inner / vw, inner / vh)
    ox = SKILL_PADDING + (inner - vw * scale) / 2
    oy = SKILL_PADDING + (inner - vh * scale) / 2

    path_els = "\n".join(f'    <path d="{d}" fill="{FILL}"/>' for d in paths)

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SKILL_SIZE}" height="{SKILL_SIZE}" '
        f'viewBox="0 0 {SKILL_SIZE} {SKILL_SIZE}">\n'
        f'  <rect x="0.5" y="0.5" width="{SKILL_SIZE-1}" height="{SKILL_SIZE-1}" '
        f'rx="{SKILL_RX}" fill="{BG}" stroke="{BORDER}" stroke-width="1"/>\n'
        f'  <g transform="translate({ox:.2f},{oy:.2f}) scale({scale:.4f})">\n'
        f'{path_els}\n'
        f'  </g>\n'
        f'</svg>\n'
    )


# ── Main ───────────────────────────────────────────────────────
def main() -> None:
    OUT_SOCIAL.mkdir(parents=True, exist_ok=True)
    OUT_SKILLS.mkdir(parents=True, exist_ok=True)

    print("Building social icons...")
    for name, (source, slug) in SOCIAL_SPECS.items():
        src = (RAW_SI if source == "simpleicons" else RAW_OC) / f"{slug}.svg"
        if not src.exists():
            print(f"  [SKIP] {src.name} not found")
            continue
        svg   = src.read_text()
        paths = extract_paths(svg)
        vb    = extract_viewbox(svg)
        out   = OUT_SOCIAL / f"{name}.svg"
        out.write_text(social_svg(paths, vb))
        print(f"  [OK]   {out.relative_to(REPO)}")

    print("\nBuilding skill icons...")
    for slug in SKILL_SLUGS:
        src = RAW_SI / f"{slug}.svg"
        if not src.exists():
            print(f"  [SKIP] {src.name} not found")
            continue
        svg   = src.read_text()
        paths = extract_paths(svg)
        vb    = extract_viewbox(svg)
        out   = OUT_SKILLS / f"{slug}.svg"
        out.write_text(skill_svg(paths, vb))
        print(f"  [OK]   {out.relative_to(REPO)}")

    print("\nDone. Generated icons in assets/generated/")


if __name__ == "__main__":
    main()
