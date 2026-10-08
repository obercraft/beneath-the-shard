package net.sachau.beneath.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;
import java.util.Map;

@JsonIgnoreProperties(ignoreUnknown = true)
public record HexmapData(
        double size,
        int radius,
        Map<String, String> ringLetters,
        List<Wedge> wedges,
        String ringBFill,
        String centerFill
) {
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Wedge(String name, String fill) {}
}
