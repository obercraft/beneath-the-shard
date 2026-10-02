#!/usr/bin/env python3
"""Generate tables/monsters-bestiary.tex — 100 monster stat blocks."""

from pathlib import Path



def esc(s: str) -> str:
    return (
        s.replace("&", r"\&")
        .replace("%", r"\%")
        .replace("#", r"\#")
        .replace("_", r"\_")
    )


# (name, pool, hits, deploy, threat, [(action, diff, effect), ...])
# diff: E / M / H
# Tiers: 1-40 minion, 41-75 brute, 76-95 elite, 96-100 horror

MINIONS = [
    ("Vein Tick", "2d6", 2, "Front", "d6", [
        ("Close In", "E", "If not sharing a zone with a character, Move toward the nearest one."),
        ("Bite", "M", "Deal 1 hit to one character in its zone."),
        ("Latch", "H", "Deal 1 hit; that character cannot Move next round."),
    ]),
    ("Ash Rat", "1d6", 1, "Swarm", "d6", [
        ("Skitter", "E", "Move to an adjacent zone."),
        ("Nip", "E", "Deal 1 hit to a character in its zone."),
        ("Scatter", "M", "Move; the next Strike against it this round needs +1 face."),
    ]),
    ("Glass Mite", "1d6", 1, "Swarm", "d6", [
        ("Crawl", "E", "Move toward nearest character."),
        ("Shard Bite", "M", "Deal 1 hit; ignore Guard."),
    ]),
    ("Cave Urchin", "2d6", 2, "Front", "d6", [
        ("Roll", "E", "Move into a character's zone."),
        ("Spine", "M", "Deal 1 hit to each character in its zone (max 2)."),
    ]),
    ("Drip Slime", "2d6", 2, "Mid", "d6", [
        ("Ooze", "E", "Move to adjacent zone."),
        ("Engulf", "M", "Deal 1 hit; character loses Guard."),
        ("Split Drip", "H", "Spawn: place another Drip Slime with 1 Hit in an adjacent zone (once per fight)."),
    ]),
    ("Gloom Bat", "1d6", 1, "Rear", "d6", [
        ("Swoop", "E", "Move to a character's zone from up to two zones away."),
        ("Bleed Screech", "M", "Deal 1 hit; that character cannot Aid this round."),
    ]),
    ("Bone Maggot", "1d6", 1, "Swarm", "d6", [
        ("Burrow Edge", "E", "Move."),
        ("Gnaw", "E", "Deal 1 hit to a character who took a hit this round."),
    ]),
    ("Rust Beetle", "2d6", 2, "Front", "d6", [
        ("Clack", "E", "Move adjacent to nearest character."),
        ("Corrode", "M", "Deal 1 hit; next Strike by that character costs +1 energy if Medium."),
    ]),
    ("Shardling Scout", "2d6", 2, "Mid", "d6", [
        ("Advance", "E", "Move toward Z1."),
        ("Crystal Cut", "M", "Deal 1 hit."),
        ("Signal", "H", "All other Shardlings treat Close In as already satisfied this round."),
    ]),
    ("Tunnel Leech", "2d6", 2, "Front", "d6", [
        ("Slither", "E", "Move into occupied zone."),
        ("Drain", "M", "Deal 1 hit; monster heals 1 hit (max Hits)."),
    ]),
    ("Ember Moth", "1d6", 1, "Swarm", "d6", [
        ("Flutter", "E", "Move."),
        ("Singe", "M", "Deal 1 hit; ongoing: 1 hit next round unless Guarded."),
    ]),
    ("Pit Viper", "2d6", 2, "Front", "d6", [
        ("Coil", "E", "Gain Guard."),
        ("Strike", "M", "Deal 1 hit."),
        ("Venom", "H", "Deal 1 hit; character cannot Guard next round."),
    ]),
    ("Carrion Crow", "1d6", 1, "Rear", "d6", [
        ("Circle", "E", "Move to Rear-most empty adjacent step toward party."),
        ("Eye Peck", "M", "Deal 1 hit; -1 face on that character's next die."),
    ]),
    ("Fungal Spore", "1d6", 1, "Swarm", "d6", [
        ("Drift", "E", "Move."),
        ("Choke", "M", "Deal 1 hit; character cannot use Hard Hard this round."),
    ]),
    ("Mine Wight Pup", "2d6", 2, "Front", "d6", [
        ("Shamble", "E", "Move toward nearest character."),
        ("Claw", "M", "Deal 1 hit."),
    ]),
    ("Crystal Gnat Cloud", "2d6", 3, "Swarm", "d6", [
        ("Swarm Move", "E", "Move."),
        ("Sting Cloud", "M", "Deal 1 hit to every character in its zone."),
        ("Disperse", "H", "Ignore the next hit; Move."),
    ]),
    ("Debt Thug", "2d6", 3, "Front", "d6", [
        ("Press", "E", "Move into a character's zone."),
        ("Club", "M", "Deal 1 hit."),
        ("Shake Down", "H", "Deal 1 hit; party marks +1 Debt if they flee this fight."),
    ]),
    ("Gate Urchin", "2d6", 2, "Mid", "d6", [
        ("Cling", "E", "If on Gate terrain (Z5), gain Guard."),
        ("Spike", "M", "Deal 1 hit to character in same or adjacent zone."),
    ]),
    ("Soot Imp", "2d6", 2, "Mid", "d6", [
        ("Cackle Step", "E", "Move."),
        ("Cinder Flick", "M", "Deal 1 hit to adjacent zone."),
        ("Smoke", "H", "Characters in its zone treat Strike as needing +1 face."),
    ]),
    ("Pale Centipede", "2d6", 2, "Front", "d6", [
        ("Undulate", "E", "Move; may pass through a monster zone."),
        ("Mandible", "M", "Deal 1 hit."),
        ("Coil Bind", "H", "Deal 1 hit; character cannot Move."),
    ]),
    ("Scrap Hound", "2d6", 3, "Front", "d6", [
        ("Bay", "E", "Move toward a character who is alone in their zone."),
        ("Maul", "M", "Deal 1 hit."),
        ("Drag", "H", "Deal 1 hit; Move that character one zone toward Z5."),
    ]),
    ("Lantern Jelly", "1d6", 2, "Mid", "d6", [
        ("Pulse", "E", "All characters in adjacent zones are revealed (no stealth)."),
        ("Sting", "M", "Deal 1 hit."),
    ]),
    ("Ore Tick", "2d6", 2, "Front", "d6", [
        ("Magnet Crawl", "E", "Move into zone with most metal (Warrior preferred)."),
        ("Suck Spark", "M", "Deal 1 hit; steal 1 energy if that character would spend any this round."),
    ]),
    ("Grave Larva", "1d6", 1, "Swarm", "d6", [
        ("Writhe", "E", "Move."),
        ("Burrow Flesh", "M", "Deal 1 hit to a character at 1 hit remaining, or 1 hit otherwise."),
    ]),
    ("Echo Sprig", "2d6", 2, "Rear", "d6", [
        ("Mimic Step", "E", "Move to copy a character's last Move destination if adjacent path exists."),
        ("False Call", "M", "Cancel one Aid this round."),
        ("Shatter Chirp", "H", "Deal 1 hit to all in its zone."),
    ]),
    ("Blindfish Walker", "2d6", 2, "Mid", "d6", [
        ("Slap", "E", "Move."),
        ("Gulp Dark", "M", "Deal 1 hit; zone becomes difficult (Moves Hard Hard) until cleared."),
    ]),
    ("Nail Sprite", "1d6", 1, "Swarm", "d6", [
        ("Dart", "E", "Move."),
        ("Puncture", "E", "Deal 1 hit."),
        ("Rust Laugh", "M", "Character's next Guard fails automatically."),
    ]),
    ("Cinder Beetle", "2d6", 2, "Front", "d6", [
        ("Glow", "E", "Gain Guard."),
        ("Burst", "M", "Deal 1 hit to its zone; take 1 hit itself."),
    ]),
    ("Tunnel Brat", "2d6", 2, "Front", "d6", [
        ("Chuck Rock", "M", "Deal 1 hit to adjacent zone."),
        ("Run", "E", "Move toward Z5."),
        ("Jeer", "H", "Nearest character must target this monster if they Strike this round."),
    ]),
    ("Shard Flea", "1d6", 1, "Swarm", "d6", [
        ("Hop", "E", "Move up to two zones."),
        ("Bite", "E", "Deal 1 hit."),
    ]),
    ("Muck Crab", "2d6", 3, "Front", "d6", [
        ("Sideways", "E", "Move."),
        ("Claw", "M", "Deal 1 hit."),
        ("Pinch Gear", "H", "Deal 1 hit; character cannot use archetype actions next round."),
    ]),
    ("Whisper Moth", "1d6", 1, "Rear", "d6", [
        ("Soft Wing", "E", "Move without triggering entry hits."),
        ("Steal Word", "M", "Deal 1 hit; that character cannot use archetype actions until the next round."),
    ]),
    ("Bone Spur", "2d6", 2, "Mid", "d6", [
        ("Plant", "E", "If it does not Move, gain Guard."),
        ("Impale", "M", "Deal 1 hit to character entering its zone, or Strike in zone."),
    ]),
    ("Guild Rat", "2d6", 2, "Front", "d6", [
        ("Flank", "E", "Move to a zone with a character and another monster."),
        ("Shiv", "M", "Deal 1 hit."),
        ("Call Debt", "H", "If it hits, mark +1 Debt."),
    ]),
    ("Static Polyp", "2d6", 2, "Mid", "d6", [
        ("Anchor", "E", "Cannot be Moved this round."),
        ("Arc", "M", "Deal 1 hit to a character in same or adjacent zone."),
        ("Discharge", "H", "Deal 1 hit to all characters in adjacent zones."),
    ]),
    ("Dust Wisp", "1d6", 1, "Swarm", "d6", [
        ("Drift", "E", "Move."),
        ("Choke Dust", "M", "Deal 1 hit; Stress +1 on that character if Resonance is tracked."),
    ]),
    ("Cave Spiderling", "2d6", 2, "Front", "d6", [
        ("Web Line", "E", "Move; leave web: next foe Move into that zone costs Medium for characters."),
        ("Bite", "M", "Deal 1 hit."),
    ]),
    ("Pyre Cub", "2d6", 3, "Front", "d6", [
        ("Pounce", "E", "Move into character zone."),
        ("Rake", "M", "Deal 1 hit."),
        ("Howl Embers", "H", "Deal 1 hit; character takes 1 hit at start of next round."),
    ]),
    ("Lead Slug", "1d6", 3, "Mid", "d6", [
        ("Creep", "E", "Move."),
        ("Crush Toe", "M", "Deal 1 hit; character cannot Move."),
    ]),
    ("Hollow Child Echo", "2d6", 2, "Rear", "d6", [
        ("Beckon", "E", "Nearest character Moves one zone toward this monster if not Hard Hard resisted (assign any die 4+)."),
        ("Cold Touch", "M", "Deal 1 hit."),
        ("Wail", "H", "All characters in adjacent zones take 1 hit."),
    ]),
]

BRUTES = [
    ("Shard Brute", "3d6", 5, "Front", "d6", [
        ("Advance", "E", "Move toward nearest character."),
        ("Smash", "M", "Deal 2 hits to one character in its zone."),
        ("Backhand", "H", "Deal 1 hit to up to two characters in its zone."),
        ("Roar", "M", "Characters in its zone cannot Guard this round."),
    ]),
    ("Tunnel Ogre", "3d6", 5, "Front", "d6", [
        ("Stoop Walk", "E", "Move."),
        ("Club Sweep", "M", "Deal 1 hit to each character in its zone."),
        ("Hurl Rubble", "H", "Deal 2 hits to a character in an adjacent zone."),
    ]),
    ("Crystal Hound Alpha", "3d6", 4, "Front", "d6", [
        ("Hunt", "E", "Move toward the most wounded character."),
        ("Bite", "M", "Deal 2 hits."),
        ("Pack Howl", "H", "All Swarm allies Move once for free (no die)."),
    ]),
    ("Ashblade Mercenary", "3d6", 4, "Front", "d6", [
        ("Close", "E", "Move into a character's zone."),
        ("Burning Cut", "M", "Deal 1 hit; ongoing 1 hit next round."),
        ("Execute", "H", "Deal 3 hits to a character who already took a hit this round."),
    ]),
    ("Vein Stalker Beast", "3d6", 4, "Mid", "d6", [
        ("Stalk", "E", "Move; gain Guard if ending in Mid/Rear."),
        ("Pounce", "M", "Move into zone and deal 1 hit."),
        ("Throat Rip", "H", "Deal 2 hits; character cannot Aid."),
    ]),
    ("Iron Vulture", "2d6", 4, "Rear", "d6", [
        ("Wheel", "E", "Move."),
        ("Dive", "M", "Deal 2 hits to a character in Front (Z1--Z2)."),
        ("Carry Off", "H", "Deal 1 hit; Move character one zone toward Z5."),
    ]),
    ("Quarry Wight", "3d6", 5, "Front", "d6", [
        ("Shamble", "E", "Move."),
        ("Grave Claw", "M", "Deal 2 hits."),
        ("Drain Warmth", "H", "Deal 1 hit; heal 1 hit."),
        ("Wail of Pits", "M", "Characters in zone lose Guard."),
    ]),
    ("Slag Golem Chunk", "3d6", 5, "Mid", "d6", [
        ("Trudge", "E", "Move; ignore forced Move."),
        ("Fist", "M", "Deal 2 hits."),
        ("Slag Burst", "H", "Deal 1 hit to all in its zone; it takes 1 hit."),
    ]),
    ("Gate Enforcer", "3d6", 4, "Front", "d8", [
        ("Lock Step", "E", "Move to block path to Z1 (prefer Z2/Z3)."),
        ("Baton", "M", "Deal 1 hit."),
        ("Arrest", "H", "Deal 2 hits; character cannot leave zone."),
    ]),
    ("Resonance Spawn", "3d6", 4, "Mid", "d6", [
        ("Pulse Step", "E", "Move."),
        ("Static Lash", "M", "Deal 1 hit to same or adjacent zone."),
        ("Overload", "H", "Deal 2 hits; party Resonance Stress +1."),
    ]),
    ("Cave Troll Kin", "3d6", 5, "Front", "d6", [
        ("Lumber", "E", "Move."),
        ("Rend", "M", "Deal 2 hits."),
        ("Regrow", "H", "Heal 2 hits if it dealt a hit this phase."),
    ]),
    ("Blackmarket Ogre", "3d6", 5, "Front", "d6", [
        ("Menace", "E", "Nearest character Moves away one zone or takes 1 hit (player choice)."),
        ("Chain Hook", "M", "Pull a character from adjacent zone; deal 1 hit."),
        ("Crush", "H", "Deal 3 hits."),
    ]),
    ("Glass Serpent", "3d6", 4, "Mid", "d6", [
        ("Slither", "E", "Move up to two zones in a line."),
        ("Fang", "M", "Deal 2 hits."),
        ("Coil Crush", "H", "Deal 1 hit; character cannot Move or Strike."),
    ]),
    ("Pit Knight Remnant", "3d6", 5, "Front", "d8", [
        ("Advance Banner", "E", "Move; allies Front gain Guard."),
        ("Rusted Thrust", "M", "Deal 2 hits."),
        ("Shield Wall", "H", "Gain Guard; deal 1 hit to attackers this round."),
    ]),
    ("Fungal Brute", "3d6", 5, "Front", "d6", [
        ("Stomp", "E", "Move."),
        ("Spore Fist", "M", "Deal 2 hits; character -1 face next die."),
        ("Cloud", "H", "Deal 1 hit to all characters in zone and adjacent."),
    ]),
    ("Debt Collector", "3d6", 4, "Front", "d8", [
        ("Corner", "E", "Move into zone with most characters."),
        ("Bone Interest", "M", "Deal 1 hit; +1 Debt if unpaid after fight."),
        ("Break Finger", "H", "Deal 2 hits; character cannot use Hard Hard next round."),
    ]),
    ("Amber Scorpion", "3d6", 4, "Front", "d6", [
        ("Scuttle", "E", "Move."),
        ("Claw", "M", "Deal 1 hit."),
        ("Stinger", "H", "Deal 2 hits; ongoing poison 1 hit next round."),
    ]),
    ("Mine Horror Half", "3d6", 5, "Mid", "d6", [
        ("Drag Arm", "E", "Move."),
        ("Sweep Bone", "M", "Deal 2 hits."),
        ("Suture", "H", "Heal 1; deal 1 hit to nearest character."),
    ]),
    ("Cinder Boar", "3d6", 4, "Front", "d6", [
        ("Charge", "E", "Move into zone; deal 1 hit if ending on a character."),
        ("Gore", "M", "Deal 2 hits."),
        ("Ash Breath", "H", "Deal 1 hit to all in adjacent zones."),
    ]),
    ("Void Mite Broodmother", "3d6", 5, "Mid", "d6", [
        ("Spawn Signal", "E", "If a Swarm ally is down, place one Ash Rat (1 Hit) in its zone once/fight."),
        ("Bite", "M", "Deal 2 hits."),
        ("Dark Milk", "H", "All Swarm allies heal 1 hit."),
    ]),
    ("Stone Mantid", "3d6", 4, "Front", "d6", [
        ("Climb Wall", "E", "Move; ignore zone capacity once."),
        ("Razor Arm", "M", "Deal 2 hits."),
        ("Snatch", "H", "Deal 1 hit; Move character to its zone."),
    ]),
    ("Blight Elk", "3d6", 4, "Mid", "d6", [
        ("Antler Rush", "E", "Move two zones toward a character; deal 1 hit on contact."),
        ("Trample", "M", "Deal 2 hits."),
        ("Rot Crown", "H", "Deal 1 hit; Stress +1."),
    ]),
    ("Chain Ghoul", "3d6", 4, "Front", "d6", [
        ("Rattle", "E", "Move."),
        ("Lash", "M", "Deal 1 hit to adjacent zone."),
        ("Bind", "H", "Deal 2 hits in zone; character cannot Move."),
    ]),
    ("Slag Hound Pair", "3d6", 4, "Front", "d6", [
        ("Flank Run", "E", "Move to opposite side of a character (adjacent zone if possible)."),
        ("Twin Bite", "M", "Deal 2 hits."),
        ("Trip", "H", "Deal 1 hit; character falls: next action Hard Hard."),
    ]),
    ("Oracle Leech", "2d6", 4, "Rear", "d6", [
        ("Drift Thought", "E", "Move."),
        ("Siphon Vision", "M", "Deal 1 hit; cancel one planned Hard Hard this round."),
        ("Prophecy Burn", "H", "Deal 2 hits to a character who used a Seer/Mage action this fight."),
    ]),
    ("Basalt Ape", "3d6", 5, "Front", "d6", [
        ("Climb", "E", "Move."),
        ("Rock Throw", "M", "Deal 2 hits adjacent."),
        ("Beat Chest", "H", "Allies Front gain +1 hit on their next action; this ape Guards."),
    ]),
    ("Needle Priest", "3d6", 4, "Mid", "d8", [
        ("Chant", "E", "Nearest Swarm moves once free."),
        ("Glass Needle", "M", "Deal 2 hits same/adjacent."),
        ("Bless Pain", "H", "Deal 1 hit; monster allies in zone heal 1."),
    ]),
    ("Rubble Elemental", "3d6", 5, "Mid", "d6", [
        ("Reform", "E", "Heal 1 if it did not Move last round."),
        ("Avalanche Fist", "M", "Deal 2 hits."),
        ("Bury", "H", "Deal 1 hit; character skips next Party phase action."),
    ]),
    ("Wailing Bride", "3d6", 4, "Rear", "d8", [
        ("Glide", "E", "Move."),
        ("Grief Touch", "M", "Deal 1 hit; character cannot Guard."),
        ("Wedding Screech", "H", "Deal 2 hits to all characters in adjacent zones."),
    ]),
    ("Gear Tortoise", "3d6", 5, "Mid", "d6", [
        ("Shell In", "E", "Gain Guard."),
        ("Steam Vent", "M", "Deal 1 hit to all in zone."),
        ("Cannon Snout", "H", "Deal 3 hits to one character within two zones."),
    ]),
    ("Blood Jelly Elder", "3d6", 5, "Front", "d6", [
        ("Flow", "E", "Move."),
        ("Dissolve", "M", "Deal 2 hits; ignore Guard."),
        ("Split Threat", "H", "Deal 1 hit; place a Drip Slime (2 Hits) adjacent once/fight."),
    ]),
    ("Hollow Knight", "3d6", 5, "Front", "d8", [
        ("March", "E", "Move toward Z1."),
        ("Spectral Thrust", "M", "Deal 2 hits."),
        ("Oath Break", "H", "Deal 1 hit; character loses one Guard and one Aid this round."),
    ]),
    ("Cave Manticore Cub", "3d6", 5, "Front", "d6", [
        ("Stalk", "E", "Move."),
        ("Claw", "M", "Deal 2 hits."),
        ("Tail Spikes", "H", "Deal 1 hit to up to three characters in adjacent zones."),
    ]),
    ("Aether Hyena", "3d6", 4, "Front", "d6", [
        ("Laughing Run", "E", "Move."),
        ("Tear", "M", "Deal 2 hits."),
        ("Steal Spark", "H", "Deal 1 hit; steal 1 energy from the party."),
    ]),
    ("Grim Bailiff", "3d6", 4, "Front", "d8", [
        ("Serve Writ", "E", "Move into zone with a character who has Debt."),
        ("Mace", "M", "Deal 2 hits."),
        ("Confiscate", "H", "Deal 1 hit; that character loses Guard and cannot Guard next round."),
    ]),
]

ELITES = [
    ("Shard Captain", "4d6", 6, "Front", "d8", [
        ("Rally Filth", "E", "One allied monster Moves free."),
        ("Captain's Cut", "M", "Deal 2 hits."),
        ("Formation", "M", "All Front allies gain Guard."),
        ("Execute Order", "H", "Deal 3 hits to one character in its zone."),
    ]),
    ("Resonance Cantor Apostate", "4d6", 6, "Mid", "d8", [
        ("Dissonant Step", "E", "Move."),
        ("Shatter Note", "M", "Deal 2 hits in zone."),
        ("Silence Bell", "H", "Characters in zone cannot Aid or Ward."),
        ("Choir of Knives", "H", "Deal 1 hit to every character on the field (max 3)."),
    ]),
    ("Voidbinder Thrall", "4d6", 6, "Mid", "d8", [
        ("Pin", "E", "A character in its zone cannot Move."),
        ("Void Hook", "M", "Pull from adjacent; deal 1 hit."),
        ("Cage Crush", "H", "Deal 3 hits to a Bound/pinned character."),
        ("Horizon", "H", "No one leaves its zone; deal 1 hit to each character there."),
    ]),
    ("Dust Alchemist Renegade", "3d6", 6, "Rear", "d8", [
        ("Flask Step", "E", "Move."),
        ("Vitriol", "M", "Deal 2 hits adjacent."),
        ("Mutagen Cloud", "H", "Deal 1 hit to all in Mid zones; Stress +1."),
        ("Magnum Shock", "H", "Deal 3 hits to one character."),
    ]),
    ("Iron Vanguard Fallen", "4d6", 7, "Front", "d8", [
        ("Bulwark Walk", "E", "Move; gain Guard."),
        ("Shield Bash", "M", "Deal 2 hits; character cannot Move."),
        ("Phalanx", "M", "Allies in zone gain Guard."),
        ("Judgment", "H", "Deal 3 hits."),
    ]),
    ("Night Broker Boss", "4d6", 6, "Mid", "d8", [
        ("Buy Opening", "E", "One ally Strikes with +1 hit this phase."),
        ("Contract Knife", "M", "Deal 2 hits."),
        ("Sell Out", "H", "Deal 1 hit to a character; another character takes 1 hit (Broker chooses)."),
        ("Midnight Clause", "H", "Deal 2 hits; cancel one Party Hard Hard this round."),
    ]),
    ("Gatecutter Assassin", "4d6", 5, "Rear", "d8", [
        ("Soft Entry", "E", "Move into any zone ignoring capacity once."),
        ("Keystrike", "M", "Deal 2 hits."),
        ("Kill the Keeper", "H", "Deal 3 hits to a character who has not Moved this round."),
        ("Seal Behind", "M", "After Moving, characters cannot follow into its zone this round."),
    ]),
    ("Prism Seer Wraith", "4d6", 6, "Rear", "d8", [
        ("Glance Ahead", "E", "Force party to discard one unassigned die next Party phase."),
        ("Oracle Bolt", "M", "Deal 2 hits any zone."),
        ("Bad Future", "H", "Force reroll of one successful party action die."),
        ("Prophetic Doom", "H", "Deal 3 hits to a character who ignored a Guard warning."),
    ]),
    ("Crucible Champion", "4d6", 7, "Front", "d8", [
        ("Pain Tithe", "E", "Take 1 hit; deal 1 hit."),
        ("Anvil Blow", "M", "Deal 2 hits."),
        ("No Quarter", "H", "Deal 3 hits; neither side Guards this exchange."),
        ("Molten Aura", "M", "Characters ending in its zone take 1 hit."),
    ]),
    ("Oathbreaker Duellist", "4d6", 6, "Front", "d8", [
        ("Cut Ties", "E", "Move; cannot be Aided against."),
        ("Spite Cut", "M", "Deal 2 hits."),
        ("Turncloak", "H", "Deal 1 hit to a character and force an ally in zone to take 1 hit."),
        ("Forsaken Surge", "H", "If alone vs characters in zone, deal 4 hits."),
    ]),
    ("Aetherwright Construct", "4d6", 6, "Mid", "d8", [
        ("Lattice Step", "E", "Move itself or pull a minion."),
        ("Hardlight Edge", "M", "Deal 2 hits; ignore Guard."),
        ("Barrier Dome", "H", "Gain Guard; characters entering take 1 hit."),
        ("Cataclysm Line", "H", "Deal 3 hits along two zones."),
    ]),
    ("Tunnel Knight Haunt", "4d6", 6, "Front", "d8", [
        ("Choke Point", "E", "Only one character may enter its zone next round."),
        ("Cave-In Blow", "M", "Deal 2 hits; character cannot leave."),
        ("Collapse Threat", "H", "Deal 1 hit to each character in zone; Move them adjacent."),
        ("Dead End", "H", "Deal 3 hits if exactly one character shares its zone."),
    ]),
    ("Glasshand Killer", "4d6", 5, "Mid", "d8", [
        ("Sliver", "E", "Deal 1 hit (precision; cannot redirect)."),
        ("Poison Edge", "M", "Deal 2 hits; ongoing 1."),
        ("Arterial", "H", "Deal 2 hits; ongoing each round until Guarded."),
        ("Perfect Cut", "H", "If a 6 was rolled in its pool, deal 4 hits."),
    ]),
    ("Veinstalker Apex", "4d6", 6, "Mid", "d8", [
        ("Vein Step", "E", "Move along crystal; gain Guard."),
        ("Ambush", "M", "Deal 2 hits to a character that Moved."),
        ("Quartz Throat", "H", "Deal 3 hits to a lone character in its zone."),
        ("Hungering Glass", "H", "Deal 2 hits; if character falls, Move free."),
    ]),
    ("Debtknife Captain", "4d6", 6, "Front", "d8", [
        ("Corner Ledger", "E", "Move to character with Debt."),
        ("Collection", "M", "Deal 2 hits."),
        ("Foreclosure", "H", "Deal 3 hits; the party loses 1 Energy."),
        ("Final Notice", "H", "Deal 4 hits to a marked debtor."),
    ]),
    ("Ashblade Zealot", "4d6", 6, "Front", "d8", [
        ("Cinder Cut", "E", "Deal 1 hit."),
        ("Wildfire", "M", "Deal 1 hit to two characters in zone."),
        ("Cremate", "H", "Deal 3 hits; heal 1 if target falls."),
        ("White-Hot", "H", "Deal 2 hits; next party Hard Hard becomes Medium+energy once (zealot bleeds advantage)."),
    ]),
    ("Static Rain Elemental", "4d6", 6, "Mid", "d8", [
        ("Charge Air", "E", "Characters in metal (Warrior) take 1 hit if they lack Guard."),
        ("Bolt", "M", "Deal 2 hits same/adjacent."),
        ("Storm Sheet", "H", "Deal 1 hit to all characters."),
        ("Grounding Crush", "H", "Deal 3 hits; end all Guards on the field."),
    ]),
    ("Mining Guild Juggernaut", "4d6", 7, "Front", "d8", [
        ("Steam Advance", "E", "Move toward Z1."),
        ("Drill Fist", "M", "Deal 2 hits."),
        ("Vent", "M", "Deal 1 hit to all in zone."),
        ("Overburden", "H", "Deal 3 hits; character cannot Move next round."),
    ]),
    ("Star-Cult Hierophant", "4d6", 6, "Rear", "d8", [
        ("Preach", "E", "One ally heals 1 or Moves free."),
        ("Glass Sacrament", "M", "Deal 2 hits any zone."),
        ("Compel Kneel", "H", "Character in Mid/Front loses next Easy action."),
        ("Falling Sun Rite", "H", "Deal 2 hits to all characters; Stress +1."),
    ]),
    ("Bone Colossus Fragment", "4d6", 7, "Mid", "d8", [
        ("Rebuild", "E", "Heal 1."),
        ("Osseous Slam", "M", "Deal 2 hits."),
        ("Ribcage Prison", "H", "Deal 2 hits; character cannot Move or be Aided."),
        ("Shatter Salvo", "H", "Deal 1 hit to every character; take 1 hit."),
    ]),
]

HORRORS = [
    ("Prismatic Heart Guardian", "4d6", 8, "Mid", "d8", [
        ("Orbit", "E", "Move; gain Guard."),
        ("Facet Beam", "M", "Deal 2 hits any zone."),
        ("Refract Pain", "H", "Redirect all hits dealt to it this round onto a character in its zone."),
        ("Heartflare", "H", "Deal 3 hits to all characters in Front; Stress +1."),
        ("Seal the Breach", "H", "Deal 4 hits to the character closest to Z5."),
    ]),
    ("Nameless from Aethelgard", "4d6", 8, "Rear", "d8", [
        ("Unwalk", "E", "Move to any zone."),
        ("Erase Name", "M", "Deal 2 hits; character cannot be Aided by name this round."),
        ("World Crack", "H", "Deal 3 hits along any two zones."),
        ("Silence of Stars", "H", "No Party Hard Hard this round; deal 2 hits to one character."),
        ("Remember the Cabal", "H", "Deal 4 hits; spawn two Glass Mites (1 Hit) in its zone."),
    ]),
    ("Star-Grave Leviathan Spawn", "4d6", 8, "Front", "d8", [
        ("Surge", "E", "Move toward Z1; crush: deal 1 hit if entering occupied zone."),
        ("Maw", "M", "Deal 3 hits."),
        ("Tidal Glass", "H", "Deal 2 hits to all in Front zones."),
        ("Swallow Dark", "H", "Deal 3 hits; heal 2."),
        ("Depth Pressure", "H", "Characters in its zone treat all actions as Hard Hard this round."),
    ]),
    ("The Guild's Hungering Vault", "4d6", 8, "Mid", "d8", [
        ("Ledger Pulse", "E", "Mark all characters with Debt; they take 1 hit if already Debted."),
        ("Vault Door", "M", "Deal 2 hits; gain Guard."),
        ("Compound Interest", "H", "Deal hits equal to party Debt marks (max 4)."),
        ("Foreclose Reality", "H", "Deal 3 hits; destroy one Guard on each character."),
        ("Zero Balance", "H", "Deal 4 hits to the character with most Debt; clear that Debt."),
    ]),
    ("Echo of the Falling Sun", "4d6", 8, "Rear", "d8", [
        ("Second Dawn", "E", "All monsters heal 1."),
        ("Blind Noon", "M", "Deal 2 hits; characters cannot target Rear this round."),
        ("Ash Tide", "H", "Deal 2 hits to all characters."),
        ("Night of Fire", "H", "Deal 3 hits to Z1 and Z2 characters."),
        ("Remember Impact", "H", "Deal 5 hits split among characters as it chooses (min 1 each if 3 alive)."),
    ]),
]


def diff_tex(d):
    return {"E": r"\easy", "M": r"\medium", "H": r"\hard{} \hard{}"}[d]


def actions_list_tex(actions):
    lines = [r"\begin{enumerate}\setlength{\itemsep}{0.15em}\setlength{\parskip}{0pt}"]
    for name, d, effect in actions:
        lines.append(
            rf"  \item \textbf{{{esc(name)}}} ({diff_tex(d)}): {esc(effect)}"
        )
    lines.append(r"\end{enumerate}")
    return "\n".join(lines)


def all_monsters():
    m = []
    m.extend(MINIONS)
    m.extend(BRUTES)
    m.extend(ELITES)
    m.extend(HORRORS)
    assert len(m) == 100, len(m)
    return m


OUT_BESTIARY = Path("/home/msachau/shardbound/tables/monsters-bestiary.tex")


def main():
    import sys
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from monster_flavor import FLAVOR

    monsters = all_monsters()
    tiers = [
        (1, 40, "Minions", "Small hungers, swarms, and hired knives. Cheap Threat, ugly deaths."),
        (41, 75, "Brutes \\& Skirmishers", "Heavy meat and mid-dark predators. They set the tempo of a delve."),
        (76, 95, "Elites", "Named dangers, cult blades, and guild engines. Threat often rolls d8."),
        (96, 100, "Horrors", "Apocalypse fragments. Budget carefully---or not at all."),
    ]

    lines = []
    idx = 1
    for lo, hi, title, intro in tiers:
        lines.append("\\section{" + title + "}")
        lines.append("")
        lines.append(esc(intro))
        lines.append("")
        while idx <= hi:
            name, pool, hits, deploy, threat, actions = monsters[idx - 1]
            fl = FLAVOR[name]
            lines.append(
                "\\subsection*{\\#"
                + f"{idx:02d} --- "
                + esc(name)
                + "\\index{"
                + esc(name)
                + "}}"
            )
            lines.append("")
            lines.append("\\textbf{Appearance.} " + esc(fl["appearance"]))
            lines.append("")
            lines.append("\\textbf{Behavior.} " + esc(fl["behavior"]))
            lines.append("")
            lines.append("\\textbf{Lore.} " + esc(fl["lore"]))
            lines.append("")
            lines.append("\\begin{monsterentry}{Stats}")
            lines.append(
                "\\textbf{Pool} "
                + pool
                + "\\quad\\textbf{Hits} "
                + str(hits)
                + "\\quad\\textbf{Deploy} "
                + deploy
                + "\\quad\\textbf{Threat} "
                + threat
            )
            lines.append("")
            lines.append("\\textbf{Actions (top to bottom)}")
            lines.append(actions_list_tex(actions))
            lines.append("\\end{monsterentry}")
            lines.append("")
            idx += 1

    OUT_BESTIARY.parent.mkdir(parents=True, exist_ok=True)
    OUT_BESTIARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_BESTIARY} with {len(monsters)} monsters")



if __name__ == "__main__":
    main()
