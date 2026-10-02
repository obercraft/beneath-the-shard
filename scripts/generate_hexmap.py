#!/usr/bin/env python3
"""Generate chapters/hexmap-grid.tex: a 61-hex ring map of Terramyr (radius 4).

Rings set Gate tier (E/D shallow, C mid, B deep, A Heart). Six wedges set region.
Hex IDs are ring letter + clockwise index starting at the top.
"""

import math
from pathlib import Path

OUT = Path("/home/msachau/shardbound/chapters/hexmap-grid.tex")

SIZE = 0.92  # cm, hex circumradius (pointy-top)
RADIUS = 4

RING_LETTER = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

# Wedge index 0..5 by angle (0-60, 60-120, ...) counter-clockwise from east.
WEDGES = [
    ("Guild Marches", "shardamber!22"),
    ("Crown Scar Road", "shardamber!40!bone"),
    ("Salt Quarantine", "ash!12"),
    ("Ash Frontier", "ash!38"),
    ("Vein Wastes", "blood!14"),
    ("Cult Lacunae", "blood!28!ash!25"),
]
RING_B_FILL = "ash!62"
CENTER_FILL = "shardink!78"


def axial_to_xy(q: int, r: int):
    x = SIZE * math.sqrt(3) * (q + r / 2.0)
    y = SIZE * 1.5 * r
    return x, y


def ring_of(q: int, r: int) -> int:
    s = -q - r
    return max(abs(q), abs(r), abs(s))


def main():
    hexes = []
    for q in range(-RADIUS, RADIUS + 1):
        for r in range(-RADIUS, RADIUS + 1):
            if ring_of(q, r) > RADIUS:
                continue
            x, y = axial_to_xy(q, r)
            ring = ring_of(q, r)
            ang = math.degrees(math.atan2(y, x)) % 360.0 if ring else 0.0
            hexes.append((q, r, x, y, ring, ang))

    # Index within ring: clockwise from the top (90 deg).
    ids = {}
    for ring in range(RADIUS + 1):
        members = [h for h in hexes if h[4] == ring]
        if ring == 0:
            ids[(0, 0)] = "A0"
            continue
        # clockwise angle from top: (90 - ang) mod 360
        members.sort(key=lambda h: (90.0 - h[5]) % 360.0)
        for i, h in enumerate(members, start=1):
            ids[(h[0], h[1])] = f"{RING_LETTER[ring]}{i}"

    # Towns: ring E hex closest to each wedge mid-angle (30, 90, ...).
    towns = set()
    for w in range(6):
        mid = 30.0 + 60.0 * w
        ring_e = [h for h in hexes if h[4] == RADIUS]
        best = min(ring_e, key=lambda h: min(abs(h[5] - mid), 360 - abs(h[5] - mid)))
        towns.add((best[0], best[1]))

    lines = []
    lines.append(r"\begin{center}")
    lines.append(r"\begin{tikzpicture}[x=1cm,y=1cm]")
    for q, r, x, y, ring, ang in hexes:
        if ring == 0:
            fill = CENTER_FILL
            textcol = "bone"
        elif ring == 1:
            fill = RING_B_FILL
            textcol = "shardink"
        else:
            w = int(ang // 60.0) % 6
            fill = WEDGES[w][1]
            textcol = "shardink"
        hid = ids[(q, r)]
        # Pointy-top hexagon: vertices at 30, 90, ... 330 degrees.
        verts = " -- ".join(
            f"({x + SIZE*math.cos(math.radians(30 + 60*k)):.3f},{y + SIZE*math.sin(math.radians(30 + 60*k)):.3f})"
            for k in range(6)
        )
        lines.append(
            f"  \\filldraw[draw=shardink, line width=0.5pt, fill={fill}] {verts} -- cycle;"
        )
        label = hid
        if (q, r) in towns:
            label = hid + r"\,\faHome"
        lines.append(
            f"  \\node[anchor=north, color={textcol}, font=\\GameSans\\scriptsize\\bfseries] "
            f"at ({x:.3f},{y + SIZE*0.78:.3f}) {{{label}}};"
        )
        if ring == 0:
            lines.append(
                f"  \\node[color=bone, font=\\GameSans\\tiny] at ({x:.3f},{y - SIZE*0.25:.3f}) {{Star-Grave}};"
            )
    lines.append(r"\end{tikzpicture}")
    lines.append(r"\end{center}")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for w in range(6):
        mid = 30.0 + 60.0 * w
        ring_e = [h for h in hexes if h[4] == RADIUS]
        best = min(ring_e, key=lambda h: min(abs(h[5] - mid), 360 - abs(h[5] - mid)))
        print(f"{WEDGES[w][0]:16} town {ids[(best[0], best[1])]}")
    print(f"Wrote {OUT} with {len(hexes)} hexes")


if __name__ == "__main__":
    main()
