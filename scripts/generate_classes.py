#!/usr/bin/env python3
"""Generate chapters/classes/{warrior,rogue,mage}.tex with full class trees."""

from pathlib import Path

OUT = Path("/home/msachau/shardbound/chapters/classes")

DIFF = {
    "E": r"\easy",
    "M": r"\medium{} \energy{1}",
    "H": r"\hard{} \hard{}",
}

# Power curve: which difficulties dominate each level (5 picks, ordered)
LEVEL_DIFFS = {
    1: ["E", "E", "E", "M", "M"],
    2: ["E", "E", "M", "M", "M"],
    3: ["E", "M", "M", "M", "H"],
    4: ["M", "M", "M", "M", "H"],
    5: ["M", "M", "M", "H", "H"],
    6: ["M", "M", "H", "H", "H"],
    7: ["M", "H", "H", "H", "H"],
    8: ["M", "H", "H", "H", "H"],
    9: ["H", "H", "H", "H", "H"],
    10: ["H", "H", "H", "H", "H"],
}


def esc(s: str) -> str:
    return s.replace("&", r"\&").replace("%", r"\%")


def level_table(actions):
    """actions: list of (name, diff_key, effect)"""
    rows = []
    for i, (name, dk, effect) in enumerate(actions):
        color = r"\rowcolor{bone}" if i % 2 == 0 else r"\rowcolor{ash!15}"
        rows.append(
            f"  {color} {esc(name)} & {DIFF[dk]} & {esc(effect)} \\\\"
        )
    body = "\n".join(rows)
    return rf"""
{{\small
\renewcommand{{\arraystretch}}{{1.15}}
\begin{{tabularx}}{{\linewidth}}{{>{{\raggedright\arraybackslash}}p{{2.6cm}} c >{{\raggedright\arraybackslash}}X}}
  \shardheadercell{{Action}} & \shardheadercell{{Diff.}} & \shardheadercell{{Effect}} \\
{body}
\end{{tabularx}}
}}
"""


CLASSES = {
    "warrior": {
        "section": "Warrior Classes",
        "intro": r"Warrior classes forge steel and stubborn will against the Star-Grave.",
        "classes": [
            (
                "Iron Vanguard",
                "A living wall of plate and oath. Holds the gate while others bleed for crystal.",
            ),
            (
                "Ashblade",
                "Burns brighter the closer death leans in. Favors brutal finishing cuts.",
            ),
            (
                "Tunnel Knight",
                "Veteran of collapsing shafts and black chokepoints. Master of cramped zones.",
            ),
            (
                "Crucible Veteran",
                "Tempered in guild smelters and punishment pits. Trades pain for momentum.",
            ),
            (
                "Oathbreaker",
                "Cast out of every banner that mattered. Turns betrayal into ruthless leverage.",
            ),
        ],
    },
    "rogue": {
        "section": "Rogue Classes",
        "intro": r"Rogue classes cut contracts, throats, and escape routes through the underworld.",
        "classes": [
            (
                "Gatecutter",
                "Specialist in Shard-Gate breaches, locks, and killing whoever holds the key.",
            ),
            (
                "Veinstalker",
                "Hunts along crystal veins where light lies and sound dies.",
            ),
            (
                "Debtknife",
                "Collector for Mining Guild ledgers written in blood and interest.",
            ),
            (
                "Glasshand",
                "Fights with shard-slivers and poisoned grit; precision over spectacle.",
            ),
            (
                "Night Broker",
                "Buys silence, sells ambushes, and always keeps a second price ready.",
            ),
        ],
    },
    "mage": {
        "section": "Mage Classes",
        "intro": r"Mage classes bend Aether-Glass until it sings---or screams.",
        "classes": [
            (
                "Aetherwright",
                "Crafts volatile patterns of raw shard-light into bolts and barriers.",
            ),
            (
                "Resonance Cantor",
                "Sings the crystal's frequency until minds crack and stone answers.",
            ),
            (
                "Voidbinder",
                "Pins fragments of the dead world into temporary, hungry cages.",
            ),
            (
                "Dust Alchemist",
                "Grinds relics into powders that heal, burn, or rewrite flesh.",
            ),
            (
                "Prism Seer",
                "Reads fractured futures in glass and steers the party through the worst ones.",
            ),
        ],
    },
}


# Thematic action templates per class: (name_prefix_patterns, effect_builders)
# Each class gets a bank of (name, effect_template) keyed by difficulty mood.

def warrior_bank(cname: str):
    banks = {
        "Iron Vanguard": [
            ("Shield Bash", "E", "Deal 1 hit to a foe in your zone; they cannot Move next round."),
            ("Brace", "E", "Gain Guard. If you already have Guard, an ally in your zone gains Guard."),
            ("Lockstep", "E", "You and one ally in your zone may each Move to the same adjacent zone."),
            ("Iron Wall", "M", "Until your next round, foes entering your zone take 1 hit."),
            ("Taunt", "M", "Choose a foe in your zone: their next action must target you if able."),
            ("Bulwark Strike", "M", "Deal 1 hit and gain Guard."),
            ("Interpose", "M", "Redirect the next hit an ally in your zone would take to yourself; then Guard."),
            ("Phalanx Push", "H", "Deal 1 hit to each foe in your zone; push one into an adjacent zone."),
            ("Unbreakable", "H", "Ignore the next two hits you would take this round."),
            ("Last Stand", "H", "If you have taken a hit this fight, deal 2 hits to one foe in your zone."),
            ("Gate Seal", "E", "No foe may leave your zone until the end of the round."),
            ("Shoulder Check", "E", "Move into an adjacent zone occupied by a foe and deal 1 hit."),
            ("Tower Guard", "M", "All allies in your zone gain Guard."),
            ("Crushing Advance", "M", "Move into an adjacent zone; deal 1 hit to one foe there."),
            ("Aegis Slam", "H", "Deal 2 hits to one foe in your zone; you gain Guard."),
            ("Line Breaker", "H", "Deal 1 hit to a foe; that foe and one adjacent-zone foe each take 1 hit."),
            ("Oath of Iron", "M", "Spend no energy on your next Medium action this round."),
            ("Retaliate", "E", "After you take a hit this round, deal 1 hit to the attacker if in your zone."),
            ("Hold Fast", "M", "You cannot be Moved by foes; gain Guard."),
            ("Siege Presence", "H", "Foes in your zone treat Move as Hard Hard until your next round."),
            ("Anchor", "E", "Prevent one ally in your zone from being Moved this round."),
            ("Rivet Blow", "M", "Deal 1 hit; that foe deals 1 less hit with their next attack."),
            ("Fortify", "M", "Gain Guard and reclaim 1 energy."),
            ("Crushing Guard", "H", "Gain Guard; deal 1 hit to every foe that hits you this round."),
            ("Immovable", "H", "You and one ally ignore Move forced by foes; each gains Guard."),
            ("Vanguard Charge", "H", "Move up to two zones in a straight line; deal 1 hit in the final zone."),
            ("Shield Wall", "H", "Allies in your zone ignore the first hit this round."),
            ("Judgment Blow", "H", "Deal 3 hits to one foe in your zone that injured an ally this fight."),
            ("Enduring Plate", "M", "Ignore the first hit; if it was from a foe in your zone, deal 1 hit back."),
            ("War Banner", "H", "Allies in your zone may treat one Easy action as free of die assignment this round (still need faces)."),
        ],
        "Ashblade": [
            ("Cinder Cut", "E", "Deal 1 hit to a foe in your zone."),
            ("Spark Step", "E", "Move to an adjacent zone after dealing a hit this round."),
            ("Blood Heat", "E", "If you took a hit this round, your next Strike deals +1 hit."),
            ("Searing Edge", "M", "Deal 1 hit; that foe takes 1 hit at the start of the next round."),
            ("Ash Cloud", "M", "Foes in your zone cannot Aid until your next round."),
            ("Executioner's Poise", "M", "Deal 1 hit to a foe that already took a hit this round."),
            ("Flare Parry", "M", "Gain Guard; if you ignore a hit, deal 1 hit to the attacker."),
            ("Cremate", "H", "Deal 2 hits to one foe in your zone; if they fall, reclaim 1 energy."),
            ("Wildfire Slash", "H", "Deal 1 hit to a foe and 1 hit to another foe in the same zone."),
            ("Dying Ember", "H", "If you have 1 hit remaining before you would fall, deal 2 hits instead of falling; then fall."),
            ("Knife of Coals", "E", "Deal 1 hit; ignore Guard on that foe for this hit."),
            ("Smoke Withdraw", "E", "Move to an adjacent zone; gain Guard."),
            ("Brand", "M", "Mark a foe: your next action against them this fight costs no energy."),
            ("Rage Tempo", "M", "Deal 1 hit; take 1 hit yourself to deal +1 hit."),
            ("Incinerate", "H", "Deal 2 hits; that foe cannot Guard this round."),
            ("Ashen Whirl", "H", "Deal 1 hit to up to three foes in your zone."),
            ("Kindling Blow", "M", "Deal 1 hit; if you Strike the same foe later this round, deal +1 hit."),
            ("Char", "E", "A foe in your zone loses Guard if they have it."),
            ("Ember Dance", "M", "Move, then Strike without spending the usual energy (still need Medium die)."),
            ("Hellcut", "H", "Deal 3 hits to one foe that has taken hits this round."),
            ("Scorch Guard", "E", "Gain Guard; attackers that hit you take 1 hit."),
            ("Black Spark", "M", "Deal 1 hit to a foe in an adjacent zone."),
            ("Furnace Heart", "H", "Until your next round, your Strikes deal +1 hit."),
            ("Cinder Storm", "H", "Deal 1 hit to every foe in your zone and an adjacent zone."),
            ("Last Cinder", "H", "Discard all unassigned party dice to deal that many hits (max 3) to one foe."),
            ("Burning Oath", "M", "Deal 1 hit; you may not Guard this round."),
            ("Smolder", "E", "A foe already hit this round takes 1 hit."),
            ("Pyre Drive", "H", "Move into a foe's zone and deal 2 hits."),
            ("Ash Feast", "H", "If a foe falls in your zone, heal 1 hit or reclaim 2 energy."),
            ("White-Hot", "H", "Deal 2 hits; treat your next Hard Hard action this fight as Medium +1 energy instead."),
        ],
        "Tunnel Knight": [
            ("Choke Point", "E", "Choose your zone: only one foe may enter it next round."),
            ("Lantern Guard", "E", "Gain Guard; allies in your zone ignore darkness effects this round."),
            ("Short Step", "E", "Move to an adjacent zone even if it is occupied by foes."),
            ("Cave-In Blow", "M", "Deal 1 hit; that foe cannot leave your zone this round."),
            ("Shaft Rush", "M", "Move up to two adjacent zones along a straight passage; deal 1 hit at the end."),
            ("Ribcracker", "M", "Deal 1 hit; that foe's next Hard Hard action fails automatically."),
            ("Bolt the Hatch", "M", "Prevent all Moves out of your zone until your next round."),
            ("Collapse Threat", "H", "Deal 1 hit to each foe in your zone; they Move to an adjacent zone of your choice."),
            ("Narrow Victory", "H", "If exactly one foe is in your zone, deal 3 hits."),
            ("Deep Watch", "H", "You and allies in your zone gain Guard; foes cannot Aid."),
            ("Pit Spike", "E", "Deal 1 hit to a foe that Moved into your zone this round."),
            ("Echo Step", "E", "Move; leave a decoy: the next foe action targeting your old zone fails."),
            ("Brace Tunnel", "M", "Allies in your zone cannot be Moved."),
            ("Hammer Hook", "M", "Deal 1 hit and Move the foe into an adjacent zone."),
            ("Dead End", "H", "A foe in your zone cannot Move or be Aided this round; deal 1 hit."),
            ("Rockslide Guard", "H", "Gain Guard twice (ignore two hits)."),
            ("Pick Strike", "E", "Deal 1 hit ignoring 1 point of foe armor/Guard."),
            ("Crawlspace", "M", "Move through a foe's zone without stopping; end adjacent."),
            ("Pressure Plate", "M", "The next foe to enter your zone takes 2 hits."),
            ("Crush Corridor", "H", "Deal 2 hits to each foe sharing your zone if no ally is there."),
            ("Support Beam", "E", "An ally in your zone gains Guard."),
            ("Mine Cart Slam", "H", "Move two zones; deal 2 hits in the final zone."),
            ("Blackout Fight", "M", "Foes in your zone treat ranged/adjacent attacks as failing this round."),
            ("Stone Shoulder", "H", "Deal 1 hit; gain Guard; an ally may Move for free (Easy still needed)."),
            ("Catacomb King", "H", "While in a zone with no adjacent empty zone, deal +1 hit on all your hits."),
            ("Seal Crack", "M", "Cancel one foe Move into or out of your zone."),
            ("Grate Kick", "E", "Deal 1 hit; Move yourself to an adjacent zone."),
            ("Spike Nest", "H", "Until your next round, foes ending their turn in your zone take 1 hit."),
            ("Underpass Ambush", "H", "If you Moved this round, deal 2 hits to one foe."),
            ("Final Bulkhead", "H", "You cannot leave your zone; deal 2 hits to every foe that enters."),
        ],
        "Crucible Veteran": [
            ("Pain Tithe", "E", "Take 1 hit to reclaim 1 energy."),
            ("Scar Memory", "E", "Gain Guard if you have already taken a hit this fight."),
            ("Grit Swing", "E", "Deal 1 hit; you may not Move this round."),
            ("Tempered Blow", "M", "Deal 1 hit; ignore the next hit you take."),
            ("Crucible Breath", "M", "Reclaim 1 energy; deal 1 hit to a foe in your zone."),
            ("Break Their Tempo", "M", "Deal 1 hit; that foe skips their next Easy action."),
            ("Blood Tariff", "M", "Take 1 hit; deal 2 hits to one foe."),
            ("Molten Resolve", "H", "While you have taken more hits than any ally, deal +1 hit on strikes."),
            ("Veteran Feint", "H", "Cancel one foe action targeting you; deal 1 hit."),
            ("No Quarter", "H", "Deal 2 hits; you and the foe cannot Guard this round."),
            ("Quench", "E", "Remove a burning/ongoing hit effect from yourself or an ally in your zone."),
            ("Chain Hook", "E", "Pull a foe from an adjacent zone into yours."),
            ("Foundry Stomp", "M", "Deal 1 hit to all foes in your zone."),
            ("Hard Lesson", "M", "An ally in your zone may reroll one assigned die (keep second)."),
            ("Anvil Drop", "H", "Deal 3 hits to one foe; take 1 hit."),
            ("Slag Armor", "H", "Gain Guard; attackers take 1 hit when they hit you this round."),
            ("Scab Over", "M", "Heal 1 hit if you dealt a hit this round."),
            ("Work Gang", "E", "Aid without spending energy (still need Medium die)."),
            ("Cruel Momentum", "H", "After you fell a foe, Move and deal 1 hit."),
            ("Trial by Fire", "H", "Take 2 hits; until your next round your actions need one less die face threshold (6 counts as 4, etc.)."),
            ("Brand of Service", "M", "Mark yourself: reclaim 1 energy whenever you Guard."),
            ("Hammer Echo", "E", "If you dealt a hit last round, deal 1 hit now."),
            ("Forced March", "M", "You and one ally Move to the same adjacent zone."),
            ("Execution Order", "H", "Deal 2 hits to a foe below half hits (GM call) or already hit twice this fight."),
            ("Unmade Fear", "H", "Allies in your zone ignore the first failed action this round and may reassign those dice."),
            ("Pit Fighter", "M", "If alone with foes in your zone, deal +1 hit."),
            ("Iron Lung", "E", "Ignore Static Rain / hazard damage once this round."),
            ("Heavy Toll", "H", "Deal 1 hit; gain 2 energy."),
            ("Crucible Crown", "H", "Deal 2 hits; all allies reclaim 1 energy."),
            ("Endurance Peak", "H", "Ignore all hits this round; you cannot act next round."),
        ],
        "Oathbreaker": [
            ("Broken Word", "E", "Cancel one ally Aid targeting you; deal 1 hit to a foe instead."),
            ("Cut Ties", "E", "Move; you cannot be Aided this round."),
            ("Spite Guard", "E", "Gain Guard; an ally in your zone loses Guard if they have it."),
            ("Betray the Line", "M", "Swap zones with an ally; deal 1 hit in your new zone."),
            ("Blackmail Blow", "M", "Deal 1 hit; that foe must target an ally of yours next if able."),
            ("Stolen Honor", "M", "Use one Basic Action an ally in your zone just resolved, once."),
            ("Cruel Bargain", "M", "An ally takes 1 hit; you deal 2 hits."),
            ("Severance", "H", "Deal 2 hits; that foe cannot benefit from allied actions this round."),
            ("Turncloak Strike", "H", "Deal 1 hit to a foe and 1 hit to an ally in your zone; reclaim 2 energy."),
            ("Forsaken Surge", "H", "If no ally is in your zone, deal 3 hits to one foe."),
            ("Mocking Parry", "E", "Gain Guard; taunt: one foe must attack you."),
            ("Lone Path", "E", "Move twice (two Easy assignments) as one action if you assign two dice."),
            ("Debt of Blood", "M", "Deal 1 hit for each ally that has fallen this fight (max 3)."),
            ("False Banner", "M", "Foes treat you as an ally for targeting until you hit them."),
            ("Exile's Edge", "H", "Deal 2 hits; ignore Guard."),
            ("Ruin Pact", "H", "You and one foe each take 2 hits."),
            ("Whispered Threat", "M", "A foe in an adjacent zone Moves into your zone."),
            ("Backstab Allegiance", "E", "Deal 1 hit to a foe engaged with an ally."),
            ("No Master", "H", "Ignore all forced Moves and taunts; deal 1 hit."),
            ("Shattered Oath", "H", "Discard Guard from all characters in your zone; deal 1 hit to each foe."),
            ("Bitter Aid", "M", "Aid an ally; they take 1 hit and deal +1 hit on their next action."),
            ("Outcast Charge", "E", "Move into a zone with no allies; deal 1 hit."),
            ("Vendetta", "H", "Name a foe: deal 2 hits now and +1 hit whenever you Strike them this fight."),
            ("Cut the Purse", "M", "Deal 1 hit; reclaim 1 energy from the party pool if any was spent this round."),
            ("Last Betrayal", "H", "Sacrifice an ally's Guard to deal 3 hits to one foe."),
            ("Alone Enough", "M", "If you are the only party member in your zone, gain Guard and deal 1 hit."),
            ("Renegade Step", "E", "Move ignoring zones occupied limits."),
            ("Oathknife", "H", "Deal 2 hits; that foe's next action requires Hard Hard."),
            ("Black Standard", "H", "Allies may treat you as not present for zone limits; you deal +1 hit."),
            ("Unbound", "H", "Remove all conditions from yourself; deal 2 hits; take 1 hit."),
        ],
    }
    return banks[cname]


def rogue_bank(cname: str):
    banks = {
        "Gatecutter": [
            ("Pick the Lock", "E", "Ignore one barrier to entering an adjacent zone this round."),
            ("Keystrike", "E", "Deal 1 hit to a foe guarding a zone edge."),
            ("Silent Entry", "E", "Move into an adjacent zone without triggering entry hits."),
            ("Breach Charge", "M", "Move into a foe's zone; that foe loses Guard."),
            ("Cut Hinge", "M", "Deal 1 hit; open a path: allies may Move into your zone as Easy."),
            ("Lockjaw", "M", "A foe in your zone cannot leave through the way they entered."),
            ("Gate Spike", "M", "Deal 1 hit to each foe that enters your zone this round."),
            ("Forced Portal", "H", "Move yourself and one foe to an adjacent zone."),
            ("Kill the Keeper", "H", "Deal 3 hits to a foe that has not Moved this round."),
            ("Seal Behind", "H", "After Moving, foes cannot follow into your new zone this round."),
            ("Wire Snare", "E", "The next foe to leave your zone takes 1 hit."),
            ("Crowbar Blow", "E", "Deal 1 hit; ignore terrain that would block Strike."),
            ("False Key", "M", "A foe Moves into a zone you choose (adjacent)."),
            ("Rapid Breach", "M", "Move twice; deal 1 hit at the end."),
            ("Deadbolt", "H", "No one leaves your zone; deal 1 hit to one foe there."),
            ("Shatter Bar", "H", "Deal 2 hits; destroy one Guard on all foes in zone."),
            ("Scout Latch", "E", "Look into an adjacent zone; Move or Strike with +1 face on one die."),
            ("Trapjack", "M", "Set a trap: first foe to Move adjacent takes 2 hits."),
            ("Skeleton Pass", "H", "All allies may Move into your zone ignoring one hit."),
            ("Execution Entry", "H", "If you entered a zone this round, deal 2 hits."),
            ("Padlock Throat", "M", "Deal 1 hit; foe cannot speak/command allies (no Aid from them)."),
            ("Soft Step In", "E", "Move; gain Guard."),
            ("Iron File", "M", "Reduce a Hard Hard action in your zone to Medium +1 energy for you once."),
            ("Breach Team", "H", "You and one ally Move into the same zone; you deal 1 hit."),
            ("King's Gate", "H", "Control a zone edge: choose who may cross it this round."),
            ("Rattle Chain", "E", "Force a foe in your zone to lose their next Move."),
            ("Bolt Cutter", "H", "Deal 2 hits to a foe in an adjacent zone."),
            ("Open Vein Gate", "H", "Create a one-round path between two adjacent zones; Movers take 1 hit."),
            ("Assassin's Threshold", "M", "Deal 1 hit when a foe crosses into your zone."),
            ("Final Lockpick", "H", "Deal 3 hits; you must Move next round or take 1 hit."),
        ],
        "Veinstalker": [
            ("Vein Step", "E", "Move along a crystal vein to an adjacent zone."),
            ("Glimmer Cut", "E", "Deal 1 hit; ignore darkness."),
            ("Hold Breath", "E", "Gain Guard while in a crystal-lit zone."),
            ("Crystal Ambush", "M", "Deal 1 hit to a foe that Moved this round."),
            ("Resonance Knife", "M", "Deal 1 hit; foe takes 1 hit if they use energy next."),
            ("Stalker's Pause", "M", "Skip Move; your next Strike deals +1 hit."),
            ("Shard Camouflage", "M", "Foes cannot target you until you act or they Aid to reveal."),
            ("Bleed the Vein", "H", "Deal 2 hits; reclaim 1 energy from ambient shard-light."),
            ("Predator Path", "H", "Move up to two zones; deal 1 hit to one foe you pass."),
            ("Quartz Throat", "H", "Deal 3 hits to a lone foe in your zone."),
            ("Soft Glow", "E", "Reveal foes in an adjacent zone; one ally gains +1 die face."),
            ("Needle Fang", "E", "Deal 1 hit ignoring Guard."),
            ("Still Hunt", "M", "If you did not Move last round, deal 2 hits."),
            ("Echo Lure", "M", "Pull a foe from adjacent zone into yours."),
            ("Crystal Snare", "H", "Foe cannot Move; deal 1 hit now and 1 at round end."),
            ("Deep Stalk", "H", "You are not a legal target while an ally is in your zone this round."),
            ("Facet Kick", "M", "Deal 1 hit and Move to adjacent zone."),
            ("Pale Trail", "E", "After Moving, one ally may Move after you for Easy."),
            ("Hungering Glass", "H", "Deal 2 hits; if foe falls, Move free (no die)."),
            ("Vein Lord's Claim", "H", "Deal 1 hit to every foe in zones adjacent to crystal features (GM)."),
            ("Whisper Step", "E", "Move without allowing opportunity hits."),
            ("Shard Spit", "M", "Deal 1 hit to adjacent zone."),
            ("Patient Blade", "H", "Mark a foe; deal 3 hits next round if you Strike them."),
            ("Lightless Bind", "M", "Foes in your zone treat Strike as Hard Hard against you."),
            ("Crystal Feast", "H", "Spend 1 energy; deal 2 hits and heal 1 hit."),
            ("Stalk Mark", "E", "Mark a foe; your Moves toward them are Easy with any face."),
            ("Corridor Kill", "H", "If only two zones are relevant, deal 2 hits and Guard."),
            ("Glass Quiet", "M", "Cancel one foe Aid in your zone."),
            ("Vein Surge", "H", "Deal 2 hits; all crystal hazards in your zone trigger once."),
            ("Apex Stalker", "H", "Deal 2 hits; you may Skirmish without archetype limit once."),
        ],
        "Debtknife": [
            ("Interest Due", "E", "Deal 1 hit to a foe that owes you (hit them before this fight)."),
            ("Ledger Cut", "E", "Deal 1 hit; mark debt: +1 hit next time you Strike them."),
            ("Kneecap", "E", "Deal 1 hit; foe cannot Move."),
            ("Collection Run", "M", "Move; deal 1 hit; reclaim 1 energy if you already hit them."),
            ("Break Finger", "M", "Deal 1 hit; foe cannot use Hard Hard this round."),
            ("Guild Pressure", "M", "A foe must Guard or take 2 hits (their choice)."),
            ("Blood Invoice", "M", "Deal 1 hit to each foe that has taken a hit this fight (max 2 foes)."),
            ("Foreclosure", "H", "Deal 2 hits; take an item/advantage (GM)."),
            ("Compound Pain", "H", "Deal hits equal to times you hit this foe earlier in the fight (max 3)."),
            ("Final Notice", "H", "Deal 3 hits to a foe you have marked with debt."),
            ("Shake Down", "E", "Reclaim 1 energy from a foe in your zone (flavor: loot)."),
            ("Threaten", "E", "Foe Moves away to adjacent zone or takes 1 hit."),
            ("Late Fees", "M", "If a foe acted before you, deal 2 hits."),
            ("Co-Signer", "M", "An ally deals +1 hit; you take 1 hit."),
            ("Vault Crack", "H", "Deal 2 hits; ignore Guard and zone entry rules once."),
            ("Red Ledger", "H", "All your hits this round deal +1 against marked foes."),
            ("Pocket Slash", "E", "Deal 1 hit; foe loses 1 energy if they have it."),
            ("Escort Fee", "M", "Move an ally with you to an adjacent zone."),
            ("Bone Interest", "H", "Deal 1 hit now and 2 hits at the start of next round."),
            ("Default", "H", "A Guarding foe loses Guard and takes 2 hits."),
            ("Marker Call", "M", "Mark up to two foes; your Strikes against them cost no energy."),
            ("Street Tax", "E", "Deal 1 hit if you share a zone with two or more foes."),
            ("Enforcer Step", "M", "Move into a zone; deal 1 hit to the weakest foe (GM)."),
            ("Kill the Debtor", "H", "Deal 3 hits; if they fall, allies reclaim 1 energy each."),
            ("Black Account", "H", "You may treat one ally's spent energy as yours to spend this round."),
            ("Rough Audit", "M", "Deal 1 hit; reveal one foe intent (GM hints next action)."),
            ("Pay in Pain", "E", "Ally heals 1 hit; you deal 1 hit."),
            ("Lien", "H", "Foe cannot leave zone; deal 2 hits."),
            ("Repo Blade", "H", "Deal 2 hits and Move the foe to an adjacent zone you choose."),
            ("Zero Balance", "H", "Remove all marks; deal 3 hits to one marked foe."),
        ],
        "Glasshand": [
            ("Sliver Cut", "E", "Deal 1 hit; exact precision (cannot be redirected)."),
            ("Grit in the Eye", "E", "Foe in your zone has -1 die face on their next action (min 1)."),
            ("Steady Hand", "E", "Reroll one of your assigned dice."),
            ("Poisoned Edge", "M", "Deal 1 hit; foe takes 1 hit at round end."),
            ("Pressure Point", "M", "Deal 1 hit; foe cannot Guard."),
            ("Glass Rain", "M", "Deal 1 hit to a foe in adjacent zone."),
            ("Needle Flurry", "M", "Deal 1 hit twice to the same foe (two separate hits)."),
            ("Arterial Thread", "H", "Deal 2 hits; ongoing: 1 hit at start of each round until Guarded."),
            ("Shatter Palm", "H", "Deal 2 hits and destroy one environmental cover (GM)."),
            ("Perfect Cut", "H", "Deal 3 hits if you assigned a 6 to this action."),
            ("Dust Toss", "E", "Cancel enemy Aid in your zone."),
            ("Quiet Precision", "E", "Deal 1 hit without breaking stealth/camouflage effects."),
            ("Toxin Wake", "M", "Move; leave poison: next foe entering takes 1 hit."),
            ("Critical Angle", "M", "Deal 1 hit; if die was 5+, deal +1 hit."),
            ("Sever Tendon", "H", "Deal 1 hit; foe cannot Move or Strike next round."),
            ("Crystal Scalpel", "H", "Deal 2 hits ignoring all Guard and wards."),
            ("Focus Breath", "M", "Gain +1 face on one die; deal 1 hit."),
            ("Slip Guard", "E", "Gain Guard against the first hit only from adjacent zones."),
            ("Venom Burst", "H", "All foes in your zone take 1 hit and ongoing 1 next round."),
            ("Masterwork Kill", "H", "Deal 2 hits; reclaim all energy you spent this round."),
            ("Pinprick", "E", "Deal 1 hit; does not wake hazards."),
            ("Hand of Needles", "M", "Deal 1 hit to up to two foes in your zone."),
            ("Deadly Poise", "H", "Until you Move, your Strikes deal +1 hit."),
            ("Glass Net", "M", "Foes leaving your zone take 1 hit."),
            ("Assassin's Geometry", "H", "Deal 3 hits along a line of two zones."),
            ("Clean Wipe", "E", "Remove a condition from yourself."),
            ("Microcut", "M", "Deal 1 hit; foe treats Easy as Medium next action."),
            ("Shard Lancet", "H", "Deal 2 hits; heal yourself 1 hit."),
            ("Transparent Threat", "H", "Foes must Guard against you or take 1 hit when they act."),
            ("Final Facet", "H", "Deal 4 hits; you cannot act next round."),
        ],
        "Night Broker": [
            ("Buy Silence", "E", "Cancel one foe shout/alarm/Aid this round."),
            ("Sell an Opening", "E", "An ally in your zone deals +1 hit on their next action."),
            ("Whisper Deal", "E", "Move a foe one zone by bribery/threat (GM)."),
            ("Contract Knife", "M", "Deal 1 hit; name terms: if they hit you, they take 1 hit."),
            ("Second Price", "M", "After an action fails, reassign its dice to another Easy action."),
            ("Brokered Ambush", "M", "You and one ally Strike the same foe; you deal 1 hit."),
            ("Black Market Guard", "M", "Ally gains Guard; you reclaim 1 energy."),
            ("Assassination Clause", "H", "Deal 2 hits; if foe falls, gain a free Move."),
            ("Hostile Takeover", "H", "Swap control of a zone hazard to benefit you (GM)."),
            ("Midnight Ledger", "H", "Deal 1 hit to every foe that acted this round (max 3)."),
            ("Soft Bribe", "E", "A foe skips attacking you this round."),
            ("Tip the Blade", "E", "Give an ally +1 die face."),
            ("Escrow Pain", "M", "Hold 1 hit: apply it to a foe later this round."),
            ("Cut Commission", "M", "Deal 1 hit; ally reclaims 1 energy."),
            ("Double Contract", "H", "Resolve two Easy actions with one Medium assignment (one die)."),
            ("Nightfall Strike", "H", "Deal 3 hits in a zone with no bright light (GM)."),
            ("Rumors Cut", "M", "Foe attacks a different target (GM choice among legal)."),
            ("Insurance", "E", "Gain Guard; if unused, reclaim 1 energy next round."),
            ("Sell Out", "H", "An ally takes 1 hit; you deal 3 hits."),
            ("Cartel Push", "H", "Allies in adjacent zones may Move into yours; you deal 1 hit."),
            ("Quiet Market", "E", "No foe may Aid in your zone."),
            ("Price of Blood", "M", "Deal 1 hit; mark: brokers +1 hit forever this fight on them."),
            ("Shadow Handshake", "H", "Move into foe zone without being targeted until you hit."),
            ("Clause of Retreat", "M", "You and one ally Move to adjacent zone."),
            ("Kill Fee", "H", "If you fell a foe this round, deal 2 hits to another in range."),
            ("Information Cut", "E", "Learn one foe difficulty this round (GM)."),
            ("Broker's Exit", "M", "Move; cannot be followed this round."),
            ("Syndicate Steel", "H", "Deal 2 hits; one ally gains Guard."),
            ("Under-Table", "H", "Treat a Hard Hard as Medium +1 energy once."),
            ("Final Offer", "H", "Deal 2 hits; foe accepts Move away or takes +1 hit."),
        ],
    }
    return banks[cname]


def mage_bank(cname: str):
    banks = {
        "Aetherwright": [
            ("Spark Bolt", "E", "Deal 1 hit to a foe in your zone."),
            ("Glass Pane", "E", "One ally in your zone gains Guard."),
            ("Pattern Step", "E", "Move yourself or an ally in your zone to an adjacent zone."),
            ("Arc Lattice", "M", "Deal 1 hit to a foe in your zone or adjacent."),
            ("Hardlight Edge", "M", "Deal 1 hit; foe cannot Guard."),
            ("Aether Mend", "M", "Heal 1 hit on an ally in your zone."),
            ("Refraction", "M", "Redirect one hit from an ally to a foe in the same zone."),
            ("Storm Script", "H", "Deal 1 hit to every foe in your zone and one adjacent zone."),
            ("Barrier Dome", "H", "All allies in your zone gain Guard; foes take 1 hit entering."),
            ("Cataclysm Line", "H", "Deal 3 hits along two connected zones."),
            ("Focus Crystal", "E", "Gain +1 face on one die this round."),
            ("Static Kiss", "E", "Deal 1 hit; ignore armor/Guard once."),
            ("Weave Guard", "M", "Two allies gain Guard."),
            ("Lance", "M", "Deal 2 hits to one foe in adjacent zone."),
            ("Overcharge", "H", "Deal 2 hits; take 1 hit of backlash."),
            ("Prism Volley", "H", "Deal 1 hit to up to three different foes within adjacent range."),
            ("Circuit Break", "M", "Cancel one foe Hard Hard action."),
            ("Light Hook", "E", "Pull a foe from adjacent into your zone."),
            ("Aether Engine", "H", "Reclaim 2 energy; deal 1 hit."),
            ("Worldwrite", "H", "Rewrite one zone: treat it as adjacent to an extra zone this round (GM)."),
            ("Sigil Strike", "M", "Deal 1 hit; mark foe for +1 hit from allies."),
            ("Pane Shatter", "E", "Destroy your Guard to deal 1 hit to all foes in zone."),
            ("Geometric Bind", "H", "Foe cannot Move; deal 2 hits."),
            ("Resonant Forge", "M", "Ally's next Strike costs no energy."),
            ("Star-Grave Spark", "H", "Deal 2 hits; trigger Static Rain once in your zone."),
            ("Blueprint", "E", "Aid with +1 face instead of normal Aid effect."),
            ("Ion Ward", "M", "Ward an ally; they also deal 1 hit to attackers."),
            ("Cascade", "H", "Deal 1 hit; repeat once for each foe already hit this round (max 3)."),
            ("Crystal Heart", "H", "Heal 2 hits on one ally; you take 1 hit."),
            ("Aether Apocalypse", "H", "Deal 4 hits split among foes in your zone as you choose."),
        ],
        "Resonance Cantor": [
            ("Hum", "E", "Foes in your zone have -1 face on one die."),
            ("Chorus Guard", "E", "Ally gains Guard."),
            ("Pitch Step", "E", "Move; foes cannot opportunity-hit you."),
            ("Dissonant Note", "M", "Deal 1 hit; foe cannot Aid."),
            ("Harmony Strike", "M", "Deal 1 hit; an ally may Strike Easy once."),
            ("Shatter Song", "M", "Deal 1 hit to all foes in your zone."),
            ("Resonant Pull", "M", "Move a foe one zone toward or away."),
            ("Cacophony", "H", "Deal 2 hits; foes in zone cannot Guard."),
            ("Requiem", "H", "Deal 3 hits to a foe that has taken hits this round."),
            ("Crystal Choir", "H", "Allies in your zone reclaim 1 energy; foes take 1 hit."),
            ("Soft Verse", "E", "Heal 1 hit on ally."),
            ("Counterpoint", "E", "Cancel one foe Easy action."),
            ("Echo Blade", "M", "Deal 1 hit now and 1 hit next round to same foe."),
            ("Bass Drop", "M", "Foes in your zone are Moved to adjacent zones (you choose)."),
            ("High Aria", "H", "Deal 2 hits in adjacent zone."),
            ("Silence Bell", "H", "No actions but yours in your zone until you act again (one round)."),
            ("Tuning Fork", "M", "Set one ally die to 4 if lower."),
            ("Vibrato", "E", "Gain Guard; attackers take -1 hit dealt (min 0)."),
            ("Glass Opera", "H", "Deal 1 hit to every foe that can hear (all adjacent zones)."),
            ("Final Cadence", "H", "Deal 3 hits; you cannot sing/cant next round (no Cantor actions)."),
            ("Drone", "E", "Ongoing: foes entering take 1 hit while you stay."),
            ("Overtonal Cut", "M", "Deal 1 hit ignoring Guard."),
            ("Part Song", "H", "You and one ally each deal 1 hit."),
            ("Tremor Hymn", "M", "Treat your zone as difficult: foe Moves are Hard Hard."),
            ("Shard Anthem", "H", "Allies deal +1 hit this round; you take 1 hit."),
            ("Lull", "E", "One foe skips their next action if they fail a face-4 test (assign any die)."),
            ("Screaming Glass", "M", "Deal 2 hits; take 1 hit."),
            ("Polyphony", "H", "Resolve Ward and Arc Bolt effects once each without archetype actions."),
            ("Dead World's Song", "H", "Deal 2 hits; mark zone as resonant until fight ends (+1 hit on bolts)."),
            ("Absolute Pitch", "H", "Set two assigned dice to 6 for one Hard Hard action."),
        ],
        "Voidbinder": [
            ("Pin Fragment", "E", "A foe in your zone cannot Move."),
            ("Small Cage", "E", "Gain Guard shaped as void shell."),
            ("Hungering Dark", "E", "Deal 1 hit; reclaim 1 energy if foe has Guard."),
            ("Bind Limb", "M", "Deal 1 hit; foe cannot Strike."),
            ("Void Hook", "M", "Pull foe from adjacent zone; deal 1 hit."),
            ("Seal Ally", "M", "Ally becomes untargetable until they act (cage)."),
            ("Crush Cage", "M", "Deal 2 hits to a foe you have Bound this fight."),
            ("Event Horizon", "H", "No one leaves your zone; deal 1 hit to each foe there."),
            ("Unmake", "H", "Deal 3 hits; ignore Guard and wards."),
            ("Star-Grave Maw", "H", "Deal 2 hits; heal equal to hits dealt (max 2)."),
            ("Whisper Chain", "E", "Mark foe; your binds against them are Easy."),
            ("Null Step", "E", "Move through foes' zones."),
            ("Leash", "M", "If marked foe Moves, they take 1 hit and you may Move with them."),
            ("Dark Ward", "M", "Ally gains Guard; attackers take 1 hit from void backlash."),
            ("Twin Bind", "H", "Bind two foes (cannot Move); deal 1 hit to each."),
            ("Collapse", "H", "Deal 2 hits to all Bound foes."),
            ("Hollow Guard", "E", "Ignore first hit; if ignored, foe loses 1 energy."),
            ("Void Needle", "M", "Deal 1 hit to adjacent zone."),
            ("Sacrifice Bind", "H", "Take 2 hits; permanently Bind one foe this fight (no Move)."),
            ("Release to Kill", "H", "End a Bind on a foe to deal 4 hits."),
            ("Shadow Manacle", "M", "Deal 1 hit; foe's Hard Hard becomes impossible this round."),
            ("Dim", "E", "Foes in your zone cannot target adjacent zones."),
            ("Grav Well", "H", "Pull all adjacent foes into your zone; deal 1 hit each (max 3)."),
            ("Anchor Soul", "M", "Ally cannot be Moved; heal 1."),
            ("Voidstorm", "H", "Deal 2 hits; all Guards in your zone shatter."),
            ("Black Thread", "E", "Aid by transferring 1 hit from ally to foe."),
            ("Casket", "M", "Foe skips next action; deal 1 hit."),
            ("Rift Walk", "H", "Move to any zone on the battle field; take 1 hit."),
            ("Devour Light", "H", "Deal 2 hits; cancel one hazard harmful to you this round."),
            ("Absolute Bind", "H", "Bind all foes in your zone; deal 1 hit to each."),
        ],
        "Dust Alchemist": [
            ("Puff", "E", "Foe in your zone: -1 face on one die."),
            ("Salve Dust", "E", "Heal 1 hit on ally in your zone."),
            ("Flash Powder", "E", "Move away after being targeted once."),
            ("Burn Salts", "M", "Deal 1 hit; ongoing burn 1 hit next round."),
            ("Paralytic Pinch", "M", "Deal 1 hit; foe cannot Move."),
            ("Mutagen Guard", "M", "Ally gains Guard and +1 hit on next Strike."),
            ("Catalyst Bomb", "M", "Deal 1 hit to all in your zone except you."),
            ("Transmute Pain", "H", "Convert hits on an ally into 2 hits on a foe."),
            ("Vitriol Spray", "H", "Deal 2 hits to adjacent zone."),
            ("Philosopher's Cut", "H", "Deal 3 hits; heal yourself 1."),
            ("Chalk Line", "E", "Foes crossing into your zone take 1 hit."),
            ("Smoke Flask", "E", "Gain Guard; leave zone obscured (foe Strike -1 face)."),
            ("Adrenal Dust", "M", "Ally reclaims 1 energy and may Move."),
            ("Acid Etch", "M", "Deal 1 hit; destroy Guard."),
            ("Unstable Mix", "H", "Deal 2 hits; roll a spare d6: on 1 take 1 hit."),
            ("Plague Glass", "H", "Deal 1 hit to a foe; it spreads 1 hit to another in zone."),
            ("Tonic", "M", "Heal 1; gain Guard."),
            ("Sand in Gears", "E", "Cancel foe Easy action."),
            ("Dragon Powder", "H", "Deal 2 hits in a line of two zones."),
            ("Magnum Opus", "H", "Heal all allies in zone 1 hit; foes take 1 hit."),
            ("Reagent Blade", "M", "Deal 1 hit; apply two different light conditions (GM)."),
            ("Neutralize", "E", "Remove one hazard effect from your zone."),
            ("Frenzy Dust", "H", "Ally deals +1 hit this round but takes 1 hit after."),
            ("Crystal Snuff", "M", "Reclaim 2 energy; take 1 hit."),
            ("Albedo Flash", "H", "Deal 2 hits; foes cannot Aid."),
            ("Powdered Silence", "E", "No alarms/Aid shouts in your zone."),
            ("Caustic Seal", "M", "Ongoing: zone deals 1 hit to foes ending there."),
            ("Quicksilver Step", "H", "Move two zones; deal 1 hit."),
            ("Black Powder Kiss", "H", "Deal 3 hits; zone becomes hazardous until cleared."),
            ("Dust to Dust", "H", "Deal 2 hits; if foe falls, heal 2 hits on allies split as you like."),
        ],
        "Prism Seer": [
            ("Glance Ahead", "E", "Look at top of encounter intent (GM tip); Move or Guard."),
            ("Warn", "E", "Ally gains Guard."),
            ("Fracture Step", "E", "Move to a zone you occupied earlier this fight."),
            ("Foretold Strike", "M", "Deal 1 hit; if GM confirms this was 'likely', deal +1."),
            ("Rewrite Footing", "M", "Move an ally after seeing a foe commit to an action."),
            ("Bad Future", "M", "Force a foe to reroll a successful action die (they keep second)."),
            ("Prism Guard", "M", "Two allies gain Guard."),
            ("Oracle Bolt", "H", "Deal 2 hits to a foe in any zone you can name on the grid."),
            ("Split Timeline", "H", "Resolve an action twice; keep the better outcome (costs 1 energy extra)."),
            ("Prophetic Doom", "H", "Deal 3 hits to a foe that ignored a previous Warn/Guard."),
            ("Hunch", "E", "Set one die to 3 if lower."),
            ("Second Sight", "E", "Reveal contents of adjacent zone."),
            ("Twist Odds", "M", "Swap two assigned dice between allies."),
            ("Cracked Omen", "M", "Deal 1 hit; foe must reveal next action type (GM)."),
            ("Paradox Ward", "H", "Ignore all hits against one ally this round."),
            ("Future Echo", "H", "Copy an action you resolved last round (same difficulty)."),
            ("Glass Eye", "M", "Deal 1 hit ignoring line limits (any zone)."),
            ("Premonition", "E", "You cannot be surprised by entry hits this round."),
            ("Fate Cut", "H", "Deal 2 hits; cancel one foe plan (skip their action)."),
            ("Apocalypse Reading", "H", "Allies deal +1 hit; you take 2 hits of visions."),
            ("Guide Thread", "M", "Ally treats one Hard Hard as Medium +1 energy."),
            ("Shattered Maybe", "E", "Reroll one party die."),
            ("Inevitability", "H", "Deal 2 hits that cannot be Guarded."),
            ("Crossroads", "M", "After foes act, Move one ally."),
            ("Prism Storm", "H", "Deal 1 hit to every foe on the battle field (max 4)."),
            ("Quiet Reading", "E", "Aid without energy."),
            ("Doom Mark", "M", "Mark foe; first hit against them each round deals +1."),
            ("Time Spasm", "H", "Take an extra Easy action after foes act."),
            ("Sightless Blade", "H", "Deal 2 hits; you are immune to targeting until you act again."),
            ("Final Vision", "H", "Deal 4 hits to one foe; you cannot use Seer actions next round."),
        ],
    }
    return banks[cname]


BANK_FN = {
    "warrior": warrior_bank,
    "rogue": rogue_bank,
    "mage": mage_bank,
}


def pick_actions(cname: str, archetype: str, level: int, used_names: set):
    bank = BANK_FN[archetype](cname)
    need = LEVEL_DIFFS[level]
    chosen = []
    for i, dk in enumerate(need):
        cands = [a for a in bank if a[1] == dk and a[0] not in used_names]
        if not cands:
            cands = [a for a in bank if a[0] not in used_names]
        if cands:
            pick = cands[(level * 5 + i) % len(cands)]
            name, _, effect = pick
        else:
            # Synthesize unique advanced variants from the bank
            base = bank[(level * 5 + i) % len(bank)]
            suffixes = [
                "Improved", "Greater", "Master", "Dire", "Final",
                "Reforged", "Awakened", "Ascendant", "Ruinous", "Absolute",
            ]
            suf = suffixes[(level + i) % len(suffixes)]
            name = f"{suf} {base[0]}"
            n = 2
            while name in used_names:
                name = f"{suf} {base[0]} {n}"
                n += 1
            effect = base[2]
            if dk == "H":
                if "Deal 1 hit" in effect:
                    effect = effect.replace("Deal 1 hit", "Deal 2 hits", 1)
                elif "Deal 2 hits" in effect:
                    effect = effect.replace("Deal 2 hits", "Deal 3 hits", 1)
                else:
                    effect = effect.rstrip(".") + "; deal +1 hit."
            elif dk == "M" and "reclaim" not in effect.lower():
                effect = effect.rstrip(".") + "; reclaim 1 energy if you hit."

        used_names.add(name)
        if level >= 9 and dk == "H" and "Deal 1 hit" in effect:
            effect = effect.replace("Deal 1 hit", "Deal 2 hits", 1)
        chosen.append((name, dk, effect))
    return chosen


def emit_archetype(key: str) -> str:
    meta = CLASSES[key]
    parts = [f"\\subsection{{{meta['section']}}}", "", meta["intro"], ""]
    for cname, hook in meta["classes"]:
        parts.append(f"\\subsubsection{{{cname}}}")
        parts.append(f"\\textit{{{esc(hook)}}}")
        parts.append("")
        used_names: set = set()
        for level in range(1, 11):
            parts.append(f"\\paragraph{{Level {level}.}}")
            parts.append(r"Choose one:")
            actions = pick_actions(cname, key, level, used_names)
            parts.append(level_table(actions))
            parts.append("")
        assert len(used_names) == 50, (cname, len(used_names))
    return "\n".join(parts)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for key in ("warrior", "rogue", "mage"):
        text = emit_archetype(key)
        path = OUT / f"{key}.tex"
        path.write_text(text, encoding="utf-8")
        # count actions
        n = text.count(r"\shardheadercell{Action}")
        print(f"Wrote {path} with {n} level tables")


if __name__ == "__main__":
    main()
