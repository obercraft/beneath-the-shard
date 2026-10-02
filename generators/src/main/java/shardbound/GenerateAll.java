package shardbound;

import shardbound.gen.GenerateClasses;
import shardbound.gen.GenerateEncounters;
import shardbound.gen.GenerateEquipment;
import shardbound.gen.GenerateHexmap;
import shardbound.gen.GenerateMonsters;
import shardbound.gen.GenerateSpells;

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
