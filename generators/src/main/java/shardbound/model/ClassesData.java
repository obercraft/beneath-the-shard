package shardbound.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;
import java.util.Map;

@JsonIgnoreProperties(ignoreUnknown = true)
public record ClassesData(
        Map<String, String> diffMacros,
        Map<String, List<String>> levelDiffs,
        int minDefensive,
        Map<String, Integer> keep,
        Map<String, ArchetypeMeta> archetypes,
        Map<String, List<ActionEntry>> banks,
        Map<String, List<ActionEntry>> extraBank,
        Map<String, List<ActionEntry>> powerBank,
        List<String> defensiveKeys,
        List<String> defensiveOffsets
) {
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record ArchetypeMeta(String section, String intro, List<ClassMeta> classes) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record ClassMeta(String name, String hook) {}
}
