#!/usr/bin/env python3
"""Generate tables/spells.tex — Mage Grimoire catalog."""

from pathlib import Path

OUT = Path("/home/msachau/shardbound/tables/spells.tex")

# (name, circle, diff_tex, defensive_bool, effect, overcast)
# diff_tex already includes energy/stress macros as needed
CIRCLE_I = [
    ("Spark Needle", r"\easy", False, r"Deal 1 hit to a foe in your zone or an adjacent zone.", r"$+1$ hit"),
    ("Glass Veil", r"\easy", True, r"One ally in your zone gains Guard.", r"That ally also restores 1 Armor box"),
    ("Dust Bind", r"\medium{} \energy{1}", False, r"Bind one foe in your zone.", r"Also deal 1 hit"),
    ("Shard Mend", r"\medium{} \energy{1}", True, r"Heal 1 Hit on one ally in your zone.", r"Heal 2 Hits instead"),
    ("Static Kiss", r"\easy", False, r"A foe in your zone loses Guard.", r"That foe is also Marked"),
    ("Echo Step", r"\medium{} \energy{1}", False, r"Move one ally one zone.", r"Also grant them Guard"),
    ("Vein Sense", r"\easy", False, r"Mark one foe in any zone.", r"Deal 1 hit to that foe"),
    ("Ash Whisper", r"\medium{} \energy{1}", False, r"Deal 1 hit to a foe in any zone.", r"$+1$ hit"),
    ("Null Soften", r"\medium{} \energy{1}", True, r"Until your next round, foes in your zone deal 1 less hit (minimum 1).", r"Also gain Guard"),
    ("Cinder Seal", r"\easy", False, r"Set one foe in your zone Burning.", r"Also deal 1 hit"),
    ("Pattern Brace", r"\medium{} \energy{1}", True, r"Restore 1 Armor box on yourself or an ally in your zone.", r"Restore 2 boxes, split as you like"),
    ("Borrowed Face", r"\medium{} \energy{1}", False, r"Raise one unassigned party die by $+1$ (max 6).", r"Raise two dice instead"),
]

CIRCLE_II = [
    ("Lance Lattice", r"\grand{} \energy{1}", False, r"Deal 3 hits to one foe in any zone.", r"Ignore Armor"),
    ("Bastion Glass", r"\grand{} \energy{1}", True, r"Allies in your zone gain Guard and restore 1 Armor box each.", r"Also heal 1 Hit each"),
    ("Rift Pull", r"\grand{} \energy{1}", False, r"Pull one foe from any zone into yours; deal 2 hits.", r"Also Bind them"),
    ("Choir Bolt", r"\grand{} \energy{1}", False, r"Deal 1 hit to every foe in one zone.", r"$+1$ hit to each"),
    ("Horizon Lock", r"\grand{} \energy{1}", False, r"Until your next round, foes cannot leave your zone; each takes 1 hit.", r"Also Bind one of them"),
    ("Aether Battery", r"\grand{} \energy{1} \stress{1}", False, r"Reclaim 3 Energy.", r"Reclaim 4 Energy"),
    ("Mirror Cage", r"\grand{} \energy{1}", True, r"Until your next round, the first hit against an ally in your zone is dealt to its attacker instead.", r"First two hits"),
    ("Shatter Note", r"\grand{} \energy{1}", False, r"Deal 2 hits to one foe; it loses Guard and is Marked.", r"$+1$ hit"),
    ("Flesh Dust", r"\grand{} \energy{1} \stress{1}", True, r"Heal 2 Hits on each ally in your zone.", r"Heal 3 Hits each"),
    ("False Door", r"\grand{} \energy{1}", True, r"Until your next round, one ally in your zone cannot be targeted.", r"Two allies"),
]

CIRCLE_III = [
    ("Breaking Light", r"\dire{} \energy{1}", False, r"Deal 4 hits to one foe in any zone, ignoring Armor.", r"Also Bind them"),
    ("Lattice Absolute", r"\dire{} \energy{1} \stress{1}", True, r"Until your next round, allies in your zone ignore all hits; you take 1 hit.", r"You take no hit"),
    ("Oblivion Pinch", r"\dire{} \energy{1} \stress{1}", False, r"Remove one Minion from the fight, or deal 5 hits to a Brute.", r"Deal 5 hits to an Elite instead of removing a Minion"),
    ("Thunder Choir", r"\dire{} \energy{1}", False, r"Deal 2 hits to every foe on the battle field.", r"$+1$ hit to Marked foes"),
    ("Starless Veil", r"\dire{} \energy{1}", True, r"Until your next round, no ally can be targeted by foes outside your zone.", r"Also grant Guard to all allies in your zone"),
    ("Unmaking", r"\fell{} \energy{2} \stress{1}", False, r"Deal 5 hits to one foe and 2 hits to each other foe in its zone.", r"Ignore Guard on all those hits"),
    ("The Cage Holds", r"\fell{} \energy{2}", False, r"Every foe on the battle field is Bound and skips its next phase.", r"Also deal 1 hit to each"),
    ("Last Hymn", r"\fell{} \energy{2} \stress{2}", True, r"Until your next round every ally ignores all hits and heals 1 Hit.", r"Heal 2 Hits each"),
]


def esc(s: str) -> str:
    return s.replace("&", r"\&").replace("%", r"\%")


def emit_circle(title, intro, spells):
    lines = [rf"\subsubsection{{{title}}}", "", intro, ""]
    lines.append(r"\noindent")
    lines.append(r"{\normalsize")
    lines.append(r"\renewcommand{\arraystretch}{1.35}")
    lines.append(
        r"\begin{tabularx}{\linewidth}{@{\hspace{2pt}} >{\raggedright\arraybackslash}p{4.0cm} >{\centering\arraybackslash}p{3.2cm} >{\raggedright\arraybackslash}X @{}}"
    )
    lines.append(
        r"  \shardheadercell{Spell} & \shardheadercell{Diff.} & \shardheadercell{Effect / Overcast} \\"
    )
    for i, (name, diff, defensive, effect, over) in enumerate(spells):
        color = r"\rowcolor{bone}" if i % 2 == 0 else r"\rowcolor{ash!15}"
        tag = r"\defensive{} " if defensive else ""
        lines.append(
            f"  {color} {tag}\\textbf{{{esc(name)}}} & {diff} & {effect}"
            rf" \textit{{Overcast:}} {over} \\"
        )
    lines.append(r"\end{tabularx}")
    lines.append(r"}")
    lines.append(r"\vspace{0.55em}")
    lines.append("")
    return lines


def main():
    assert len(CIRCLE_I) == 12
    assert len(CIRCLE_II) == 10
    assert len(CIRCLE_III) == 8
    lines = [
        r"% Auto-generated by scripts/generate_spells.py --- do not edit by hand.",
        "",
    ]
    lines.extend(
        emit_circle(
            "Circle I",
            r"First Circle spells need only a starting pool. Towns sell pages for 2 Refined or 1 Cult Favor each.",
            CIRCLE_I,
        )
    )
    lines.extend(
        emit_circle(
            "Circle II",
            r"Grand spells: requires Dice Pool \D{3}{6} (level 3+). Found as mid-ring pages or deep loot.",
            CIRCLE_II,
        )
    )
    lines.extend(
        emit_circle(
            "Circle III",
            r"Dire and Fell spells: pool \D{4}{6} or \D{5}{6} (level 6+ / 9+). Deep Gates and the Star-Grave.",
            CIRCLE_III,
        )
    )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} with {len(CIRCLE_I)+len(CIRCLE_II)+len(CIRCLE_III)} spells")


if __name__ == "__main__":
    main()
