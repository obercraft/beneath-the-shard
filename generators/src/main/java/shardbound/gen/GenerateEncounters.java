package shardbound.gen;

import shardbound.Data;
import shardbound.Tex;
import shardbound.model.EncountersData;
import shardbound.model.EncountersData.Encounter;
import shardbound.model.EncountersData.Mechanic;

import java.io.IOException;

public final class GenerateEncounters {
    private GenerateEncounters() {}

    public static void run() throws IOException {
        EncountersData data = Data.load("encounters.yaml", EncountersData.class);
        StringBuilder lines = new StringBuilder();
        int roll = 1;
        for (Mechanic mechanic : data.mechanics()) {
            if (mechanic.encounters().size() != 20) {
                throw new IllegalStateException(mechanic.name() + " expected 20, got " + mechanic.encounters().size());
            }
            int lo = roll;
            int hi = roll + 19;
            lines.append("\\section{").append(Tex.esc(mechanic.name())).append(" (")
                    .append(String.format("%02d", lo)).append("--")
                    .append(String.format("%02d", hi)).append(")}\n\n");
            for (Encounter encounter : mechanic.encounters()) {
                String flavor = data.flavors().getOrDefault(
                        encounter.title(),
                        "Terramyr presses in. " + encounter.title() + " unfolds under Shardlight and bad choices.");
                lines.append("\\begin{encounterentry}{")
                        .append(String.format("%02d", roll)).append(" --- ")
                        .append(Tex.esc(encounter.title())).append("\\index{")
                        .append(Tex.esc(encounter.title())).append("}}\n");
                lines.append("\\textit{").append(Tex.esc(mechanic.name())).append("}\n\n");
                lines.append(Tex.esc(flavor)).append("\n\n");
                lines.append("\\textbf{Stakes.} ").append(Tex.esc(encounter.stakes())).append('\n');
                lines.append("\\end{encounterentry}\n\n");
                roll++;
            }
        }
        if (roll != 101) {
            throw new IllegalStateException("expected 100 encounters, roll=" + roll);
        }
        var out = Tex.tables("encounters-book.tex");
        Tex.write(out, lines.toString());
        System.out.println("Wrote " + out + " with 100 encounters");
    }
}
