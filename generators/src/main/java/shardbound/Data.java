package shardbound;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.io.InputStream;

/** Jackson ObjectMapper loader for classpath JSON under {@code data/}. */
public final class Data {
    private static final ObjectMapper MAPPER = new ObjectMapper()
            .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

    private Data() {}

    public static ObjectMapper mapper() {
        return MAPPER;
    }

    public static <T> T load(String resourceName, Class<T> type) throws IOException {
        String path = resourceName.startsWith("/") ? resourceName : "/data/" + resourceName;
        try (InputStream in = Data.class.getResourceAsStream(path)) {
            if (in == null) {
                throw new IOException("Missing classpath resource: " + path);
            }
            return MAPPER.readValue(in, type);
        }
    }
}
