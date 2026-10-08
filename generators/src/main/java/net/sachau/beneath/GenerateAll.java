package net.sachau.beneath;

import net.sachau.beneath.gen.GenerateClasses;
import net.sachau.beneath.gen.GenerateEncounters;
import net.sachau.beneath.gen.GenerateEquipment;
import net.sachau.beneath.gen.GenerateHexmap;
import net.sachau.beneath.gen.GenerateMonsters;
import net.sachau.beneath.gen.GenerateSpells;

/** Entry point: regenerate all TeX catalogs from classpath JSON. */
public final class GenerateAll {
    public static void main(String[] args) throws Exception {
        GenerateClasses.run();
        GenerateEquipment.run();
        GenerateSpells.run();
        GenerateMonsters.run();
        GenerateEncounters.run();
        GenerateHexmap.run();
        System.out.println("All generators finished.");
    }
}
