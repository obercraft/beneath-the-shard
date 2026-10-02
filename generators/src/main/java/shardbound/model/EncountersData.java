package shardbound.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;
import java.util.Map;

@JsonIgnoreProperties(ignoreUnknown = true)
public record EncountersData(
        List<Mechanic> mechanics,
        Map<String, String> flavors
) {
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Mechanic(String name, List<Encounter> encounters) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Encounter(String title, String stakes) {}
}
