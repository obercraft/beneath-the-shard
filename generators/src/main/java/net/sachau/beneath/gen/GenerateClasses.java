package net.sachau.beneath.gen;

import net.sachau.beneath.Data;
import net.sachau.beneath.Tex;
import net.sachau.beneath.model.ActionEntry;
import net.sachau.beneath.model.ClassesData;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

public final class GenerateClasses {
    private GenerateClasses() {}

    public static void run() throws IOException {
        ClassesData data = Data.load("classes.yaml", ClassesData.class);
        Map<Integer, List<String>> levelDiffs = new HashMap<>();
        data.levelDiffs().forEach((k, v) -> levelDiffs.put(Integer.parseInt(k), v));

        for (String arch : List.of("warrior", "rogue", "mage")) {
            ClassesData.ArchetypeMeta meta = data.archetypes().get(arch);
            StringBuilder sb = new StringBuilder();
            sb.append("\\subsection{").append(Tex.esc(meta.section())).append("}\n\n");
            sb.append(meta.intro()).append("\n\n");

            for (ClassesData.ClassMeta clazz : meta.classes()) {
                List<ActionEntry> bank = fullBank(clazz.name(), data);
                checkBank(clazz.name(), bank, levelDiffs, data);
                sb.append("\\subsubsection{").append(Tex.esc(clazz.name())).append("}\n");
                sb.append("\\textit{").append(Tex.esc(clazz.hook())).append("}\n\n");

                Set<String> used = new LinkedHashSet<>();
                List<List<ActionEntry>> byLevel = new ArrayList<>();
                for (int level = 1; level <= 10; level++) {
                    byLevel.add(pickActions(bank, levelDiffs.get(level), used));
                }
                if (used.size() != 50) {
                    throw new IllegalStateException(clazz.name() + " used " + used.size());
                }
                sb.append(classTable(byLevel, data));
                sb.append('\n');
            }

            var out = Tex.chapters("classes/" + arch + ".tex");
            Tex.write(out, sb.toString());
            System.out.println("Wrote " + out);
        }
    }

    private static List<ActionEntry> fullBank(String className, ClassesData data) {
        List<ActionEntry> legacy = new ArrayList<>();
        legacy.addAll(data.banks().get(className));
        legacy.addAll(data.extraBank().get(className));

        List<ActionEntry> kept = new ArrayList<>();
        for (String dk : List.of("E", "M", "H")) {
            kept.addAll(trim(legacy, dk, data.keep().getOrDefault(dk, 0), data));
        }
        kept.sort(Comparator.comparingInt(legacy::indexOf));

        List<ActionEntry> out = new ArrayList<>(kept);
        out.addAll(data.powerBank().get(className));
        return out;
    }

    private static List<ActionEntry> trim(List<ActionEntry> actions, String dk, int keepN, ClassesData data) {
        List<ActionEntry> cands = actions.stream().filter(a -> dk.equals(a.diff())).toList();
        if (cands.size() <= keepN) {
            return new ArrayList<>(cands);
        }
        List<ActionEntry> chosen = new ArrayList<>();
        for (ActionEntry a : cands) {
            if (isDefensive(a.effect(), data) && chosen.size() < keepN) {
                chosen.add(a);
            }
        }
        for (ActionEntry a : cands) {
            if (chosen.size() >= keepN) {
                break;
            }
            if (!chosen.contains(a)) {
                chosen.add(a);
            }
        }
        List<ActionEntry> out = new ArrayList<>();
        for (ActionEntry a : cands) {
            if (chosen.contains(a)) {
                out.add(a);
            }
        }
        return out.subList(0, Math.min(keepN, out.size()));
    }

    private static void checkBank(
            String className,
            List<ActionEntry> bank,
            Map<Integer, List<String>> levelDiffs,
            ClassesData data) {
        Set<String> names = new HashSet<>();
        for (ActionEntry a : bank) {
            if (!names.add(a.name())) {
                throw new IllegalStateException(className + " duplicate " + a.name());
            }
            if (a.effect().contains("GM")) {
                throw new IllegalStateException(className + " GM in " + a.name());
            }
        }
        Map<String, Integer> need = new HashMap<>();
        levelDiffs.values().forEach(diffs -> diffs.forEach(d -> need.merge(d, 1, Integer::sum)));
        Map<String, Integer> have = new HashMap<>();
        bank.forEach(a -> have.merge(a.diff(), 1, Integer::sum));
        if (!need.equals(have)) {
            throw new IllegalStateException(className + " bank mismatch need=" + need + " have=" + have);
        }
        long defensive = bank.stream().filter(a -> isDefensive(a.effect(), data)).count();
        if (defensive < data.minDefensive()) {
            throw new IllegalStateException(className + " too few defensive: " + defensive);
        }
    }

    private static List<ActionEntry> pickActions(List<ActionEntry> bank, List<String> need, Set<String> used) {
        List<ActionEntry> chosen = new ArrayList<>();
        for (String dk : need) {
            ActionEntry pick = bank.stream()
                    .filter(a -> dk.equals(a.diff()) && !used.contains(a.name()))
                    .findFirst()
                    .orElseThrow(() -> new IllegalStateException("bank exhausted for " + dk));
            used.add(pick.name());
            chosen.add(pick);
        }
        return chosen;
    }

    private static String classTable(List<List<ActionEntry>> byLevel, ClassesData data) {
        StringBuilder rows = new StringBuilder();
        int row = 0;
        for (int level = 0; level < byLevel.size(); level++) {
            List<ActionEntry> actions = byLevel.get(level);
            for (int i = 0; i < actions.size(); i++) {
                ActionEntry a = actions.get(i);
                String color = (row % 2 == 0) ? "\\rowcolor{bone}" : "\\rowcolor{ash!15}";
                String tag = isDefensive(a.effect(), data) ? "\\defensive{} " : "";
                String lvl = (i == 0) ? "\\textbf{" + (level + 1) + "}" : "";
                rows.append("  ").append(color).append(' ').append(lvl).append(" & ").append(tag)
                        .append("\\textbf{").append(Tex.esc(a.name())).append("} & ")
                        .append(data.diffMacros().get(a.diff())).append(" & ")
                        .append(Tex.esc(a.effect())).append(" \\\\\n");
                row++;
            }
        }
        String header =
                "  \\shardheadercell{Lv} & \\shardheadercell{Action} & \\shardheadercell{Diff.} & \\shardheadercell{Effect} \\\\\n";
        return "\\noindent\n"
                + "{\\normalsize\n"
                + "\\renewcommand{\\arraystretch}{1.35}\n"
                + "\\begin{longtable}{@{\\hspace{2pt}}"
                + " >{\\centering\\arraybackslash}p{0.9cm}"
                + " >{\\raggedright\\arraybackslash}p{3.6cm}"
                + " >{\\centering\\arraybackslash}p{3.0cm}"
                + " >{\\raggedright\\arraybackslash}p{7.6cm} @{}}\n"
                + header
                + "\\endfirsthead\n"
                + header
                + "\\endhead\n"
                + rows
                + "\\end{longtable}\n"
                + "}\n"
                + "\\vspace{0.55em}\n";
    }

    private static boolean isDefensive(String effect, ClassesData data) {
        String e = effect.toLowerCase(Locale.ROOT);
        for (String offset : data.defensiveOffsets()) {
            e = e.replace(offset.toLowerCase(Locale.ROOT), "");
        }
        for (String key : data.defensiveKeys()) {
            if (e.contains(key.toLowerCase(Locale.ROOT))) {
                return true;
            }
        }
        return false;
    }
}
