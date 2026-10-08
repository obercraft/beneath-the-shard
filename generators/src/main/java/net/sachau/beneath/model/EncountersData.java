package net.sachau.beneath.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public record EncountersData(List<Mechanic> mechanics) {
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Mechanic(String name, List<Encounter> encounters) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Encounter(String title, String flavor, String stakes) {}
}
