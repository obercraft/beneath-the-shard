#!/usr/bin/env python3
"""Generate tables/non-combat-encounters.tex — 100 encounters."""

from pathlib import Path

# Output path set in main()


def esc(s: str) -> str:
    return (
        s.replace("&", r"\&")
        .replace("%", r"\%")
        .replace("#", r"\#")
        .replace("_", r"\_")
    )


# 20 encounters per mechanic: (title, description)
JOURNEY = [
    ("Broken Causeway", "A stone bridge over a shard-chasm has collapsed to a single beam. Advance the Journey Clock by 1 if you take the long way, or assign dice for a Medium crossing: failure drops one character for 1 hit and still advances the clock."),
    ("Ash Wind Front", "A wall of volcanic grit blinds the road. Mark +1 Journey Clock. Camp now (see Campfire Counsel) or push on: Hard Hard to keep the map accurate; failure means you become Lost (next encounter is rolled with disadvantage: use higher of two d100 results when told to roll)."),
    ("Refugee Column", "Starving surface folk block the trail, begging for crystal dust. Give supplies (lose 1 energy from the party) or refuse and gain a Debt mark from their guild patrons later. Clock does not advance if you share."),
    ("Toll of the Free Companies", "Mercenaries claim this ridge. Pay a Favor owed or fight a short skirmish; either way the clock advances unless you sneak (Medium) past without payment."),
    ("Flooded Quarry Road", "Meltwater from shard-heat floods the path. Detour (+2 Journey Clock) or ford: each character risks 1 hit on a failed Easy swim/climb."),
    ("False Milestone", "Someone rotated the waystones. Easy Insight/WIS-style check (assign Easy die) to notice; failure advances clock by 2 as you loop."),
    ("Night Herd", "Crystal-maddened cattle stampede at dusk. Scatter (all Move Easy) or hold the line (one Warrior Medium): failure deals 1 hit to a random character; success yields rations and clock stays."),
    ("Signal Fires on the Ridge", "Three fires form a triangle---ambush code. Advance clock by camping cold (+1 Stress if no fire) or light a counter-signal (Medium) to negotiate passage."),
    ("Collapsed Mining Sled", "Abandoned sled of raw glass. Salvage (gain 1 energy crystal, +1 Resonance Stress) or leave it; scavengers later become a Debt encounter if you take it."),
    ("Border Plague Banner", "A kingdom quarantine blocks the high road. Bribe (pay Favor), detour (+2 clock), or forge papers (Hard Hard on Rogue/Mage)."),
    ("Singing Rails", "Old ore rails hum with shard current. Traveling them cuts 1 clock but marks +1 Resonance Stress per character."),
    ("Guide Who Lies", "A local guide offers a shortcut. Trust them (-1 clock, then roll a Gate Omen early) or dismiss them (clock +1, safe road)."),
    ("River Ferry Strike", "Ferrymen refuse coin, demand Aether-Glass. Pay (Stress +1) or build a raft (party assigns 3 Easy successes) while clock +1."),
    ("Mirror Mirage", "Heat haze shows a second party walking your road. Ignore it (clock +1 from delay) or follow (roll Omens as if at a Gate)."),
    ("Burned Waystation", "Only charred beams remain. Search (Medium) for a map fragment that reduces next clock tick by 1; failure finds corpses and +1 Stress."),
    ("Knight-Errant's Challenge", "A duel for right of way. One character faces a Medium contest; win and clock does not advance; lose and take 1 hit, clock +1."),
    ("Sinking Cart Road", "Mud eats wheels. Abandon gear (lose a tool) to keep clock, or labor (Hard Hard, all help with Aids) to haul through."),
    ("Eclipse Noon", "Shard-dust darkens the sun for an hour. No navigation: auto clock +1, and roll Resonance Stress encounter next."),
    ("Caged Prophet", "A cage hangs over the road; the prisoner knows a shorter path. Free them (Favor to outlaws, -1 clock) or leave them (clock +0, later Debt from their kin)."),
    ("Last League Markers", "You near your destination. Clear the final league Easy or the clock fills: arrive Exhausted (start next combat with -1 party die)."),
]

RESONANCE = [
    ("Vein Hum", "The ground vibrates with crystal song. Mark +1 Resonance Stress. Medium to tune it out; failure: one character gains a minor mutation (cosmetic, -1 CHA checks)."),
    ("Static Kiss", "Sparks leap to metal. Anyone in mail takes 1 hit unless they Guard (Easy) or strip armor for the day."),
    ("Glass Hunger", "A party member craves raw shard. Spend 1 energy crystal to calm them or mark +2 Stress and they act first in the next fight recklessly."),
    ("Echo of Aethelgard", "A dead language floods a mage's dreams. Gain a free Lore fact; mark +1 Stress. Refuse the vision: Hard Hard or wake with 1 hit."),
    ("Bleeding Focus", "Aether-Glass tools weep red light. Destroy a crystal focus (-1 Stress) or keep it (+1 Stress, +1 hit on next Arc Bolt)."),
    ("Chorus of Flies", "Insects swarm toward the most resonant character. Easy to endure; failure: that character cannot Aid until after a Campfire."),
    ("Memory Theft", "Stress flares: forget one known map detail (GM erases). Recover with Campfire Counsel Heal/Lore."),
    ("Crystal Rash", "Skin facets appear overnight. +1 Stress. Medium CON-style endurance or gain Disfigured (foes target you first once per fight)."),
    ("Sympathetic Pain", "When any ally takes a hit next combat, you take 1 too until Stress is reduced at camp."),
    ("Oracle Bleed", "Nosebleeds during planning. Seer/Mage may force a reroll on one Journey roll now; mark +2 Stress."),
    ("Hollow Appetite", "Food tastes like ash. Rations heal nothing until Stress drops; clock still advances if you delay to forage."),
    ("Shard-Twin", "You glimpse a crystal double of the party. Strike it (Medium) to -1 Stress or flee (+1 Stress, +1 clock)."),
    ("Tuning Fork Bones", "Joints ache near veins. -1 die face on all physical Easy actions until camp."),
    ("Gift of Sparks", "Uncontrolled lightning from fingertips. Free 1 hit to a foe in a future fight, then +1 Stress now."),
    ("Silent Hour", "All sound dies for an hour. Communication only by gesture: next negotiation is Hard Hard; Stress +1."),
    ("Geode Heartbeat", "A character's pulse syncs to the Shard. +1 Stress; they may ignore one Guard-break once."),
    ("Dust Communion", "Inhale glittered air. Heal 1 hit and +2 Stress, or hold breath (Easy) with no effect."),
    ("Name in the Glass", "Crystal shows a loved one's face asking you to dig deeper. Resist (Medium) or mark a personal Quest Debt and +1 Stress."),
    ("Overcharge Cache", "Found battery-crystals. Take them (+1 party energy, +1 Stress each) or smash them (-1 Stress, noise attracts Journey encounter)."),
    ("Resonance Break", "Stress track fills. Immediate mutation table (GM) or burn 2 Favor/Debt marks to vent safely; otherwise start next delve with Horror (cannot Guard first round)."),
]

DEBT = [
    ("Guild Ledger Nail", "A nail-post lists your party names. Tear it down (angers guild: +2 Debt) or leave it (collectors arrive next town)."),
    ("Interest in Flesh", "A broker offers to clear 1 Debt for a finger's worth of crystal fused to skin (+1 Stress)."),
    ("Witness for the Crown", "Crown agents demand testimony against a Mining Guild. Testify (Favor with Crown, Debt with Guild) or refuse (Debt with Crown)."),
    ("Hostage Letter", "Proof a relative is held. Pay 2 crystal/energy or accept a timed Quest: fail and gain Desperate Debt (all Favor costs double)."),
    ("Forgiven---For Now", "A patron clears 1 Debt if you carry a sealed box to a Gate. Do not open it (Hard Hard temptation); opening rolls an Omen immediately."),
    ("Street Tithe", "Urchins working for Debtknife gangs demand coin. Pay (clear local heat) or chase them (Medium; failure +1 Debt rumor)."),
    ("Contract Rewrite", "A scribe can alter your obligation. Hard Hard CHA/INT; success converts Debt to Favor owed by them; failure doubles Debt."),
    ("Blood Co-Signer", "An ally must co-sign your Debt. They mark +1 personal Debt; party Debt -1."),
    ("Smuggler's Credit", "Buy gear on credit. Gain an item; +1 Debt. Default later and lose the item plus a Favor."),
    ("Church of Clearance", "A cult clears Debt through confession---and public branding. Clear 1 Debt; gain Branded (surface towns hostile once)."),
    ("Rival Party's Marker", "Another delve team holds your Favor chit. Trade a future aid promise or steal it (Rogue Medium; failure: combat stub)."),
    ("Assessor's Scale", "Officials weigh your crystal. Undervalued unless Mage Medium to argue purity; failure: taxed (+1 Debt equivalent)."),
    ("Inheritance Trap", "A will names you heirs to a bankrupt claim. Accept (+2 Debt, claim rights) or renounce (safe, lose lore hook)."),
    ("Favor Called In", "Someone you owe demands escort through a Journey leg. Complete it (-1 Debt) or refuse (+2 Debt, enemy for life)."),
    ("Blackmail Plate", "Etched plate shows your crime. Destroy (Medium stealth) or buy silence (1 Favor). Leave it: next roll on this table is forced."),
    ("Debtors' Arena", "Fight as entertainment to erase 1 Debt. One character: win a Medium duel stub; lose and Debt remains +1 Stress."),
    ("Ledger Fire", "Chance to burn guild records. Hard Hard infiltration; success clears 2 Debt; failure: Wanted (all towns +1 Debt)."),
    ("Mercy of the Countess", "A noble offers Favor if you ruin a guild rival socially. Succeed Medium intrigue; fail and both factions Debt you."),
    ("Child of the Bond", "A bonded child seeks freedom. Free them (Favor with outcasts, Debt with owners) or return them (-1 Debt, +1 Stress)."),
    ("Zero Balance Knife", "Assassin offers to kill your creditor. Accept (Debt clears, gain Blood Favor owed to killer) or refuse (creditor warned, +1 Debt)."),
]

OMENS = [
    ("Falling Sun Echo", "At the Gate, daylight burns underground for a minute. Next delve: all Strikes +1 hit but Stress +1 when you exit."),
    ("Three Blind Birds", "Dead birds fall from the Gate arch. Omens say: no flying/falling shortcuts; Move between vertical zones costs Medium."),
    ("Mirror Gate", "The Gate shows your party exiting already bloody. Heed it: start with Guard on all, or ignore and first combat foes Strike first."),
    ("Salt Rain", "White grit falls upward into the Gate. Water rations spoil; next Campfire Heal is Hard Hard."),
    ("Counting Shadows", "Shadows don't match bodies. One shadow too many: a stalker joins the delve (extra foe) unless you leave an offering (1 energy)."),
    ("Gate That Breathes", "Air pulls inward. First zone: all Easy actions need face 2+. Close visors (no scent clues)."),
    ("Name Spoken Backward", "Someone says a companion's name reversed. That character is Marked: hazards target them until a Campfire Lore clears it."),
    ("Glass Teeth", "Gate rim grows teeth. Entering deals 1 hit unless Guard Easy. Teeth keep a trophy (item lost) on failure."),
    ("Second Threshold", "Two Gates overlap. Choose left (Journey Clock +0, Stress +1) or right (Clock +1, find a Favor token)."),
    ("Priestless Blessing", "A hollow robe bows. Accept a ward (one free Guard this delve) and +1 Stress, or pass by clean."),
    ("Red Thread", "A thread ties two party members. They must share zones this delve or each take 1 hit per separated round."),
    ("Silent Market", "Ghost stalls sell memories. Buy (lose a Motivation detail, gain 1 energy) or smash stalls (Omen becomes hostile: +1 foe)."),
    ("Clockface Moss", "Moss grows in clock shapes. Read it (Easy): learn exact Journey ticks remaining; misread (fail): Clock +2."),
    ("Child Gatekeeper", "A mute child holds the key-crystal. Kindness (Aid Medium) opens safely; cruelty opens but +2 Stress."),
    ("Inverted Drip", "Water drips up. Next Resonance encounter is mandatory after first combat."),
    ("Banner of the Old World", "Aethelgard colors flicker. Mage may learn one free class-flavor cantrip once; Party Stress +1."),
    ("Door of Knives", "Entering requires leaving a weapon. Retrieve on exit Easy; failure: weapon is bound to a foe."),
    ("Laughing Echo", "Your voices return wrong. No Aid by speech this delve (Aid still ok by gesture/Easy without voice)."),
    ("Omen of Plenty", "Crystal dew coats you. +1 energy each; next Debt collector knows you struck rich (+1 Debt pressure)."),
    ("Sealed With Lead", "The Gate is lead-banded. Break seal (Hard Hard) and roll again on Omens, or walk away (Clock +1, delve delayed)."),
]

CAMPFIRE = [
    ("Shared Watch", "Assign dice: Scout (Easy) keeps night safe; fail and Journey encounter interrupts sleep (no Heal)."),
    ("Blade and Story", "Repair (Medium) restores a broken tool; Lore (Easy) reveals a rumor that -1 next Omen severity."),
    ("Confession Circle", "Speak a fear. Clear 1 Stress if honest; gain a Bond (once/fight, Aid that ally without energy)."),
    ("Ration Argument", "Split food unfairly. Medium CHA to keep peace; failure: one character refuses Aid tomorrow."),
    ("Map by Embers", "Redraw the route in ash. Success (Easy) -1 Journey Clock; failure smudges map (next travel Lost risk)."),
    ("Shard Meditation", "Mage vents Stress into the fire. -1 Stress; on 1 on a spare d6, fire becomes a hazard (1 hit)."),
    ("Silent Meal", "No talk---only dice. Each character may Heal (Easy) or Guard-for-dawn (Easy); no Bargain allowed tonight."),
    ("Trader at the Edge of Light", "A night merchant. Bargain (Medium) for supplies; fail and they steal 1 energy."),
    ("Dream Delve", "All dream the same dungeon room. Lore (Medium) to map it; use that map for advantage (one free Easy) next Gate."),
    ("Stitch and Swear", "Heal (Medium) removes 1 hit from one character; swear a Vow (mark Favor to each other)."),
    ("Burn the Letter", "Destroy Debt evidence in the fire. Clear 1 Debt; smoke signals attract a Journey encounter at dawn."),
    ("Counting Favors", "Publicly track who owes whom. Rearrange 1 Debt/Favor mark between party and NPCs known so far."),
    ("Scarecrow Watch", "Build a decoy. Scout success: skip next night ambush; failure: waste materials (lose tool)."),
    ("Bitter Brew", "Dust Alchemist-style tea. Heal all 1 hit and +1 Stress each, or skip."),
    ("Naming the Dead", "Lore for fallen NPCs. Gain a Favor with their kin faction; Stress -1."),
    ("Sparring Embers", "Two characters practice. Both spend Medium; both gain +1 face once tomorrow, or take 1 hit on failure."),
    ("False Dawn Pack-Up", "Leave early. Clock -1 but no one Heals; or sleep in (Heal allowed, Clock +0)."),
    ("Omen in the Coals", "Read fire (Easy). Preview next Gate Omen category; misread: GM lies once."),
    ("Last Song", "Cantor/anyone sings. Allies -1 Stress; foes within a mile (GM) may mark your camp on their map."),
    ("Scatter the Ashes", "Break camp clean. Next collectors/trackers need Hard Hard to find your trail; fail to scatter and Debt agents arrive next stop."),
]

MECHANICS = [
    ("Journey Clock", JOURNEY),
    ("Resonance Stress", RESONANCE),
    ("Debt & Favors", DEBT),
    ("Shard-Gate Omens", OMENS),
    ("Campfire Counsel", CAMPFIRE),
]

# Atmospheric prose (stakes remain in the tuples above)
FLAVORS = {
    "Broken Causeway": "A shard-chasm splits the old royal road. Wind moans through crystal teeth below; one beam is all that remains of the bridge the Guild swore would last forever.",
    "Ash Wind Front": "The Ash Frontier exhales. Grit scours paint from shields and turns the sun into a rumor.",
    "Refugee Column": "Families flee a Gate that woke hungry. Their hands are empty except for hope and the Guild brands on their wrists.",
    "Toll of the Free Companies": "Mercenary banners stitch the ridge. Coin or blood---they are not picky, only patient.",
    "Flooded Quarry Road": "Shard-heat melted the snow wrong. Black water fills the quarry cut like a held breath.",
    "False Milestone": "Someone twisted the waystones for a joke or a murder. Moss still grows toward the old true north.",
    "Night Herd": "Cattle with crystal cataracts thunder at dusk, lowing in frequencies that itch the teeth.",
    "Signal Fires on the Ridge": "Three fires make a triangle the Free Companies use for ambush. Your fire would answer---or betray.",
    "Collapsed Mining Sled": "A sled of raw glass lies broken, humming faintly. Scavengers' footprints circle like unfinished prayers.",
    "Border Plague Banner": "Yellow cloth and spears. The quarantine is half medicine, half tax.",
    "Singing Rails": "Abandoned ore rails sing when the Shard pulses. Riding them feels like cheating the clock---and feeding it your nerves.",
    "Guide Who Lies": "A smiling local offers a shortcut through thorn and rumor. Their eyes flick too often toward the Gate.",
    "River Ferry Strike": "Ferrymen want Aether-Glass, not crowns. The river does not care who drowns waiting.",
    "Mirror Mirage": "Heat paints a second party walking your road. They wave with your hands.",
    "Burned Waystation": "Char and bone. Someone fought a Gate omen here and lost the argument.",
    "Knight-Errant's Challenge": "A knight without a kingdom bars the way with courtesy sharp as a spear.",
    "Sinking Cart Road": "Mud eats wheels the way Debt eats years. Something below the road is drinking.",
    "Eclipse Noon": "Shard-dust veils the sun. Birds fall silent; clocks become guesses.",
    "Caged Prophet": "A cage hangs over the road. The prisoner knows a shorter path and a longer curse.",
    "Last League Markers": "Mileposts lean toward your Gate like teeth. The last league always costs more than the map admits.",
    "Vein Hum": "The ground vibrates with crystal song. Even the silent feel lyrics under their skin.",
    "Static Kiss": "Sparks leap to mail and knives. The air tastes of storms that never reach the sky.",
    "Glass Hunger": "A companion stares at raw shard the way the starved stare at bread.",
    "Echo of Aethelgard": "A dead world's tongue floods a sleeper's mouth. Morning tastes like starlight and blood.",
    "Bleeding Focus": "Your Aether tools weep red light. Power wants out---or wants you.",
    "Chorus of Flies": "Insects braid toward the most resonant soul. They know who the Shard has already marked.",
    "Memory Theft": "A map detail evaporates mid-thought. The Star-Grave edits travelers.",
    "Crystal Rash": "Facets bloom under skin overnight---jewelry you cannot pawn.",
    "Sympathetic Pain": "Your nerves braid with your allies'. Their wounds will find you.",
    "Oracle Bleed": "Nosebleeds during planning. Futures leak.",
    "Hollow Appetite": "Rations taste of ash and apology. The body refuses comfort while Stress sings.",
    "Shard-Twin": "A crystal double of your party steps from haze---same faces, emptier eyes.",
    "Tuning Fork Bones": "Joints ache in chord with nearby veins. Every Easy motion feels tuned sharp.",
    "Gift of Sparks": "Lightning nests in fingertips. A promise of violence prepaid in Stress.",
    "Silent Hour": "Sound dies. Mouths move; meaning arrives late and wrong.",
    "Geode Heartbeat": "A pulse syncs to the Shard. Guard breaks may miss you---once.",
    "Dust Communion": "Glittered air offers healing like a cult offers wine.",
    "Name in the Glass": "Crystal shows a loved face begging you deeper. The Motivation grows teeth.",
    "Overcharge Cache": "Battery-crystals left by someone who ran. Warm. Waiting.",
    "Resonance Break": "The Stress track overflows. Mutation or ruin---the Shard collects either way.",
    "Guild Ledger Nail": "A nail-post lists your names in wet ink. The Guild wants witnesses.",
    "Interest in Flesh": "A broker smiles with crystal under the skin of their palm. Debt has new interest rates.",
    "Witness for the Crown": "Crown agents want testimony. Guilds want silence. You are the hinge.",
    "Hostage Letter": "Proof of a relative in a cage. Time is a second creditor.",
    "Forgiven---For Now": "A patron clears a mark for one sealed errand. The box hums like an Omen.",
    "Street Tithe": "Urchins with Debtknife tattoos ask politely while counting exits.",
    "Contract Rewrite": "A scribe offers to rewrite fate in triplicate. Ink costs more than blood.",
    "Blood Co-Signer": "The ledger wants a second signature from someone you love.",
    "Smuggler's Credit": "Gear now, ruin later. The interest wears a smile.",
    "Church of Clearance": "A cult clears Debt with confession and a brand that towns remember.",
    "Rival Party's Marker": "Another delve team holds your Favor chit like a knife.",
    "Assessor's Scale": "Officials undervalue crystal unless purity argues back.",
    "Inheritance Trap": "A will names you heirs to a bankrupt claim---rights wrapped in rope.",
    "Favor Called In": "Someone you owe wants escort. Refuse and make an enemy with a long map.",
    "Blackmail Plate": "Your crime etched in plate. Destroy, buy, or let the road force the roll.",
    "Debtors' Arena": "Erase a mark in public bloodsport. The crowd loves a clean ledger.",
    "Ledger Fire": "Guild records burn beautifully. So do the wanted posters that follow.",
    "Mercy of the Countess": "A noble offers Favor for social ruin. Fail and both factions bill you.",
    "Child of the Bond": "A bonded child asks for freedom. Every answer writes Debt somewhere.",
    "Zero Balance Knife": "An assassin offers to kill your creditor. Blood Favor smells like freedom.",
    "Falling Sun Echo": "Daylight burns underground for a minute. The catastrophe still rehearses.",
    "Three Blind Birds": "Dead birds fall from the Gate arch. The omen forbids easy flight between heights.",
    "Mirror Gate": "The Gate shows you exiting already bloody. Premonition or invitation.",
    "Salt Rain": "White grit falls upward. Water dies; Heal becomes a struggle.",
    "Counting Shadows": "One shadow too many. Something joined the party without asking.",
    "Gate That Breathes": "Air pulls inward. Easy becomes slightly less easy at the threshold.",
    "Name Spoken Backward": "A companion's name returns reversed. Hazards learn the Mark.",
    "Glass Teeth": "The rim grows teeth. Entry bites; failure keeps a trophy.",
    "Second Threshold": "Two Gates overlap like a lie. Left costs Stress; right costs Clock.",
    "Priestless Blessing": "A hollow robe bows. Ward for Stress---or walk clean and alone.",
    "Red Thread": "Fate ties two of you. Separate zones bleed.",
    "Silent Market": "Ghost stalls sell memories by the ounce.",
    "Clockface Moss": "Moss grows in clock shapes. Read true or lose hours.",
    "Child Gatekeeper": "A mute child holds the key-crystal. Kindness and cruelty both open doors.",
    "Inverted Drip": "Water drips up. Resonance will follow your first kill.",
    "Banner of the Old World": "Aethelgard colors flicker. Power for Stress.",
    "Door of Knives": "Leave a weapon to enter. Retrieve it---or meet it in a foe's hand.",
    "Laughing Echo": "Voices return wrong. Spoken Aid dies; gestures still live.",
    "Omen of Plenty": "Crystal dew coats you rich. Collectors will smell it.",
    "Sealed With Lead": "Lead bands the Gate. Break and reroll omen---or walk away ticking.",
    "Shared Watch": "Night around a Gate is never empty. Dice decide who sleeps.",
    "Blade and Story": "Steel and rumor share the firelight. Both can be repaired.",
    "Confession Circle": "Fear spoken aloud thins Stress and ties Bonds.",
    "Ration Argument": "Hunger makes accountants of friends.",
    "Map by Embers": "Ash is a good ink until the wind edits it.",
    "Shard Meditation": "Vent Stress into flame. Sometimes the flame answers.",
    "Silent Meal": "No talk---only Heal, Guard, and the crackle of distrust.",
    "Trader at the Edge of Light": "A merchant stands where firelight fails. Prices include theft.",
    "Dream Delve": "You all dream one room. Map it before it maps you.",
    "Stitch and Swear": "Needle, vow, Favor between battered hands.",
    "Burn the Letter": "Debt evidence curls to smoke---and signals dawn hunters.",
    "Counting Favors": "Marks rearrange like knives on a table.",
    "Scarecrow Watch": "A decoy wears your fear. Ambush may swallow straw instead.",
    "Bitter Brew": "Alchemist's tea: heal now, Stress later.",
    "Naming the Dead": "Speak the fallen; their kin may answer with Favor.",
    "Sparring Embers": "Practice cuts that tomorrow might need.",
    "False Dawn Pack-Up": "Leave early and lean; or sleep and owe the Clock nothing.",
    "Omen in the Coals": "Fire previews the Gate---or lies for sport.",
    "Last Song": "A hymn thins Stress and thickens the map for listening foes.",
    "Scatter the Ashes": "Clean camps confuse collectors. Dirty ones invite them.",
}


OUT = Path("/home/msachau/shardbound/tables/encounters-book.tex")


def main():
    assert all(len(e) == 20 for _, e in MECHANICS)
    lines = []
    roll = 1
    for mech, encounters in MECHANICS:
        lo, hi = roll, roll + 19
        lines.append("\\section{" + esc(mech) + f" ({lo:02d}--{hi:02d})" + "}")
        lines.append("")
        for title, stakes in encounters:
            flavor = FLAVORS.get(
                title,
                f"Terramyr presses in. {title} unfolds under Shardlight and bad choices.",
            )
            lines.append(
                "\\begin{encounterentry}{"
                + f"{roll:02d} --- "
                + esc(title)
                + "\\index{"
                + esc(title)
                + "}}"
            )
            lines.append("\\textit{" + esc(mech) + "}")
            lines.append("")
            lines.append(esc(flavor))
            lines.append("")
            lines.append("\\textbf{Stakes.} " + esc(stakes))
            lines.append("\\end{encounterentry}")
            lines.append("")
            roll += 1
    assert roll == 101
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} with {roll-1} encounters")


if __name__ == "__main__":
    main()
