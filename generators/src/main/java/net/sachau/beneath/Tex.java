package net.sachau.beneath;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** Shared LaTeX escaping and repository path helpers. */
public final class Tex {
    private Tex() {}

    public static String esc(String s) {
        if (s == null) {
            return "";
        }
        return s.replace("&", "\\&")
                .replace("%", "\\%")
                .replace("#", "\\#")
                .replace("_", "\\_");
    }

    /** Repository root (parent of the {@code generators/} Maven module). */
    public static Path repoRoot() {
        Path cwd = Path.of("").toAbsolutePath().normalize();
        if ("generators".equals(stringName(cwd)) && cwd.resolve("pom.xml").toFile().isFile()) {
            return cwd.getParent();
        }
        if (cwd.resolve("generators/pom.xml").toFile().isFile()) {
            return cwd;
        }
        if (cwd.resolve("pom.xml").toFile().isFile() && cwd.resolve("src/main/resources/data").toFile().isDirectory()) {
            return cwd.getParent();
        }
        throw new IllegalStateException("Run from repo root or generators/: " + cwd);
    }

    public static Path chapters(String relative) {
        return repoRoot().resolve("chapters").resolve(relative);
    }

    public static Path tables(String relative) {
        return repoRoot().resolve("tables").resolve(relative);
    }

    public static void write(Path path, String content) throws IOException {
        Files.createDirectories(path.getParent());
        Files.writeString(path, content, StandardCharsets.UTF_8);
    }

    private static String stringName(Path p) {
        return p.getFileName() == null ? "" : p.getFileName().toString();
    }
}
