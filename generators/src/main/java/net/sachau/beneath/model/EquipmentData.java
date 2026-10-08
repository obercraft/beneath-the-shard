package net.sachau.beneath.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public record EquipmentData(
        List<Weapon> weapons,
        List<PricedItem> offhand,
        List<Armor> armor,
        List<GearItem> gear,
        Relics relics
) {
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Weapon(String name, String hands, String price, String effect) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record PricedItem(String name, String price, String effect) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Armor(String name, String boxes, String price, String notes) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record GearItem(String name, String price, String type, String effect) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Relics(
            List<Relic> common,
            List<Relic> uncommon,
            List<Relic> rare,
            List<Relic> prismatic
    ) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Relic(String name, String effect) {}
}
