package shardbound.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;
import java.util.Map;

@JsonIgnoreProperties(ignoreUnknown = true)
public record MonstersData(
        List<Tier> tiers,
        Map<String, String> diffMacros,
        List<Monster> minions,
        List<Monster> brutes,
        List<Monster> elites,
        List<Monster> horrors,
        Map<String, Flavor> flavor
) {
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Tier(int lo, int hi, String title, String intro) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Monster(
            String name,
            String pool,
            int hits,
            String deploy,
            String threat,
            List<ActionEntry> actions
    ) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Flavor(String appearance, String behavior, String lore) {}
}
