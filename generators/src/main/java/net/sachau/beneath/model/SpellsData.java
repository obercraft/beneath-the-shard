package net.sachau.beneath.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public record SpellsData(
        List<Spell> circleI,
        List<Spell> circleII,
        List<Spell> circleIII
) {
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Spell(String name, String diff, boolean defensive, String effect, String overcast) {}
}
