package net.sachau.beneath.gen;

import net.sachau.beneath.Data;
import net.sachau.beneath.Tex;
import net.sachau.beneath.model.ActionEntry;
import net.sachau.beneath.model.MonstersData;
import net.sachau.beneath.model.MonstersData.Monster;
import net.sachau.beneath.model.MonstersData.Tier;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public final class GenerateMonsters {
    private GenerateMonsters() {}

    public static void run() throws IOException {
        MonstersData data = Data.load("monsters.yaml", MonstersData.class);
        List<Monster> monsters = new ArrayList<>();
        monsters.addAll(data.minions());
        monsters.addAll(data.brutes());
        monsters.addAll(data.elites());
        monsters.addAll(data.horrors());
        if (monsters.size() != 100) {
            throw new IllegalStateException("expected 100 monsters, got " + monsters.size());
        }

        StringBuilder lines = new StringBuilder();
        int idx = 1;
        for (Tier tier : data.tiers()) {
            lines.append("\\section{").append(tier.title()).append("}\n\n");
            lines.append(Tex.esc(tier.intro())).append("\n\n");
            while (idx <= tier.hi()) {
                Monster monster = monsters.get(idx - 1);
                if (monster.appearance() == null || monster.behavior() == null || monster.lore() == null) {
                    throw new IllegalStateException("missing flavor fields for " + monster.name());
                }
                lines.append("\\subsection*{\\#").append(String.format("%02d", idx)).append(" --- ")
                        .append(Tex.esc(monster.name())).append("\\index{")
                        .append(Tex.esc(monster.name())).append("}}\n\n");
                lines.append("\\textbf{Appearance.} ").append(Tex.esc(monster.appearance())).append("\n\n");
                lines.append("\\textbf{Behavior.} ").append(Tex.esc(monster.behavior())).append("\n\n");
                lines.append("\\textbf{Lore.} ").append(Tex.esc(monster.lore())).append("\n\n");
                lines.append("\\begin{monsterentry}{Stats}\n");
                lines.append("\\textbf{Pool} ").append(monster.pool())
                        .append("\\quad\\textbf{Hits} ").append(monster.hits())
                        .append("\\quad\\textbf{Deploy} ").append(monster.deploy())
                        .append("\\quad\\textbf{Threat} ").append(monster.threat()).append("\n\n");
                lines.append("\\textbf{Actions (top to bottom)}\n");
                lines.append(actionsList(monster.actions(), data));
                lines.append("\\end{monsterentry}\n\n");
                idx++;
            }
        }

        var out = Tex.tables("monsters-bestiary.tex");
        Tex.write(out, lines.toString());
        System.out.println("Wrote " + out + " with " + monsters.size() + " monsters");
    }

    private static String actionsList(List<ActionEntry> actions, MonstersData data) {
        StringBuilder sb = new StringBuilder();
        sb.append("\\begin{enumerate}\\setlength{\\itemsep}{0.15em}\\setlength{\\parskip}{0pt}\n");
        for (ActionEntry action : actions) {
            String diffTex = data.diffMacros().getOrDefault(action.diff(), action.diff());
            sb.append("  \\item \\textbf{").append(Tex.esc(action.name())).append("} (")
                    .append(diffTex).append("): ").append(Tex.esc(action.effect())).append('\n');
        }
        sb.append("\\end{enumerate}\n");
        return sb.toString();
    }
}
