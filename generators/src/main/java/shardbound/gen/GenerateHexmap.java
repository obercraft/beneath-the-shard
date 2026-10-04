package shardbound.gen;

import shardbound.Data;
import shardbound.Tex;
import shardbound.model.HexmapData;
import shardbound.model.HexmapData.Wedge;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

public final class GenerateHexmap {
    private GenerateHexmap() {}

    public static void run() throws IOException {
        HexmapData cfg = Data.load("hexmap.yaml", HexmapData.class);
        double size = cfg.size();
        int radius = cfg.radius();
        Map<Integer, String> ringLetters = new HashMap<>();
        cfg.ringLetters().forEach((k, v) -> ringLetters.put(Integer.parseInt(k), v));
        List<Wedge> wedges = cfg.wedges();

        List<Hex> hexes = new ArrayList<>();
        for (int q = -radius; q <= radius; q++) {
            for (int r = -radius; r <= radius; r++) {
                int ring = ringOf(q, r);
                if (ring > radius) {
                    continue;
                }
                double x = size * Math.sqrt(3) * (q + r / 2.0);
                double y = size * 1.5 * r;
                double ang = ring == 0 ? 0.0 : Math.toDegrees(Math.atan2(y, x));
                if (ang < 0) {
                    ang += 360.0;
                }
                hexes.add(new Hex(q, r, x, y, ring, ang));
            }
        }

        Map<String, String> ids = new HashMap<>();
        for (int ring = 0; ring <= radius; ring++) {
            List<Hex> members = new ArrayList<>();
            for (Hex h : hexes) {
                if (h.ring == ring) {
                    members.add(h);
                }
            }
            if (ring == 0) {
                ids.put(key(0, 0), "A0");
                continue;
            }
            members.sort(Comparator.comparingDouble(h -> (90.0 - h.ang + 360.0) % 360.0));
            int i = 1;
            for (Hex h : members) {
                ids.put(key(h.q, h.r), ringLetters.get(ring) + i);
                i++;
            }
        }

        Set<String> towns = new HashSet<>();
        for (int w = 0; w < 6; w++) {
            towns.add(key(townHex(hexes, radius, w).q, townHex(hexes, radius, w).r));
        }

        StringBuilder lines = new StringBuilder();
        lines.append("\\begin{center}\n\\begin{tikzpicture}[x=1cm,y=1cm]\n");
        for (Hex h : hexes) {
            String fill;
            String textcol;
            if (h.ring == 0) {
                fill = cfg.centerFill();
                textcol = "bone";
            } else if (h.ring == 1) {
                fill = cfg.ringBFill();
                textcol = "shardink";
            } else {
                int w = ((int) (h.ang / 60.0)) % 6;
                fill = wedges.get(w).fill();
                textcol = "shardink";
            }
            String hid = ids.get(key(h.q, h.r));
            StringBuilder verts = new StringBuilder();
            for (int k = 0; k < 6; k++) {
                if (k > 0) {
                    verts.append(" -- ");
                }
                double vx = h.x + size * Math.cos(Math.toRadians(30 + 60 * k));
                double vy = h.y + size * Math.sin(Math.toRadians(30 + 60 * k));
                verts.append(String.format(Locale.US, "(%.3f,%.3f)", vx, vy));
            }
            lines.append("  \\filldraw[draw=shardink, line width=0.5pt, fill=").append(fill)
                    .append("] ").append(verts).append(" -- cycle;\n");
            String label = towns.contains(key(h.q, h.r)) ? hid + "\\,\\faHome" : hid;
            lines.append("  \\node[anchor=north, color=").append(textcol)
                    .append(", font=\\GameSans\\scriptsize\\bfseries] at (")
                    .append(String.format(Locale.US, "%.3f,%.3f", h.x, h.y + size * 0.78))
                    .append(") {").append(label).append("};\n");
            if (h.ring == 0) {
                lines.append("  \\node[color=bone, font=\\GameSans\\tiny] at (")
                        .append(String.format(Locale.US, "%.3f,%.3f", h.x, h.y - size * 0.25))
                        .append(") {Star-Grave};\n");
            }
        }
        lines.append("\\end{tikzpicture}\n\\end{center}\n");

        var out = Tex.chapters("hexmap-grid.tex");
        Tex.write(out, lines.toString());
        for (int w = 0; w < 6; w++) {
            Hex town = townHex(hexes, radius, w);
            System.out.printf(Locale.US, "%-16s town %s%n", wedges.get(w).name(), ids.get(key(town.q, town.r)));
        }
        System.out.println("Wrote " + out + " with " + hexes.size() + " hexes");
    }

    private static Hex townHex(List<Hex> hexes, int radius, int wedge) {
        double mid = 30.0 + 60.0 * wedge;
        Hex best = null;
        double bestDist = Double.MAX_VALUE;
        for (Hex h : hexes) {
            if (h.ring != radius) {
                continue;
            }
            double d = Math.min(Math.abs(h.ang - mid), 360 - Math.abs(h.ang - mid));
            if (d < bestDist) {
                bestDist = d;
                best = h;
            }
        }
        return best;
    }

    private static int ringOf(int q, int r) {
        int s = -q - r;
        return Math.max(Math.abs(q), Math.max(Math.abs(r), Math.abs(s)));
    }

    private static String key(int q, int r) {
        return q + "," + r;
    }

    private record Hex(int q, int r, double x, double y, int ring, double ang) {}
}
