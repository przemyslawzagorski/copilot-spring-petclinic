package org.springframework.samples.petclinic.ai;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import tools.jackson.core.JacksonException;
import tools.jackson.databind.ObjectMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * Kontroler obsługujący zakładkę „AI Asystent" w PetClinic.
 *
 * <p>
 * Wystawia dwa endpointy:
 * <ul>
 * <li>{@code GET /ai-assistant} — renderuje stronę z interfejsem czatu.</li>
 * <li>{@code POST /api/ai/chat} — proxy do mikroserwisu Python (FastAPI :8081).</li>
 * </ul>
 *
 * <p>
 * Mikroserwis Python używa GitHub Copilot SDK z custom tools i odpytuje żywy endpoint
 * {@code GET /vets} tej samej aplikacji Spring.
 */
@Controller
class AiAssistantController {

	private static final Logger log = LoggerFactory.getLogger(AiAssistantController.class);

	private static final String AI_SERVICE_URL = "http://localhost:8081";

	private static final int MAX_MESSAGE_LENGTH = 500;

	private final HttpClient httpClient;

	private final ObjectMapper objectMapper;

	AiAssistantController(ObjectMapper objectMapper) {
		this.httpClient = HttpClient.newBuilder()
			.version(HttpClient.Version.HTTP_1_1)
			.connectTimeout(Duration.ofSeconds(5))
			.build();
		this.objectMapper = objectMapper;
	}

	/** Renderuje stronę z interfejsem AI Asystenta. */
	@GetMapping("/ai-assistant")
	public String showAssistant() {
		return "ai/assistant";
	}

	/**
	 * Proxy do Python AI serwisu — przekazuje wiadomość użytkownika i zwraca odpowiedź AI
	 * jako JSON.
	 */
	@PostMapping(value = "/api/ai/chat", produces = MediaType.APPLICATION_JSON_VALUE)
	@ResponseBody
	public ResponseEntity<AiResponse> chat(@Valid @RequestBody AiRequest request) {
		try {
			byte[] jsonBody = objectMapper.writeValueAsBytes(Map.of("message", request.message()));
			log.info("Wysylam do AI ({} bajtow): {}", jsonBody.length, new String(jsonBody, StandardCharsets.UTF_8));
			HttpRequest httpRequest = HttpRequest.newBuilder()
				.uri(URI.create(AI_SERVICE_URL + "/chat"))
				.timeout(Duration.ofSeconds(120))
				.header("Content-Type", "application/json")
				.POST(HttpRequest.BodyPublishers.ofByteArray(jsonBody))
				.build();
			HttpResponse<byte[]> httpResponse = httpClient.send(httpRequest, HttpResponse.BodyHandlers.ofByteArray());
			if (httpResponse.statusCode() >= 400) {
				String errBody = new String(httpResponse.body(), StandardCharsets.UTF_8);
				log.error("AI service returned {}: {}", httpResponse.statusCode(), errBody);
				return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
					.body(new AiResponse("Blad AI (" + httpResponse.statusCode() + "): " + errBody, List.of()));
			}
			AiResponse response = objectMapper.readValue(httpResponse.body(), AiResponse.class);
			return ResponseEntity.ok(response);
		}
		catch (java.net.ConnectException ex) {
			log.warn("AI service unreachable: {}", ex.getMessage());
			return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
				.body(new AiResponse("Serwis AI jest niedostępny. Uruchom: uvicorn ai_server:app --port 8081",
						List.of()));
		}
		catch (JacksonException ex) {
			log.error("Blad serializacji zadania", ex);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
				.body(new AiResponse("Blad serializacji: " + ex.getMessage(), List.of()));
		}
		catch (Exception ex) {
			log.error("AI chat error: {}", ex.getMessage(), ex);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
				.body(new AiResponse("Błąd: " + ex.getMessage(), List.of()));
		}
	}

	// ── Wewnętrzne typy dla JSON ─────────────────────────────────────────────

	/**
	 * Żądanie od przeglądarki do Spring.
	 *
	 * @param message treść pytania użytkownika (max 500 znaków)
	 */
	record AiRequest(@NotBlank(message = "Wiadomość nie może być pusta") @Size(max = MAX_MESSAGE_LENGTH,
			message = "Wiadomość może mieć maksymalnie 500 znaków") String message) {
	}

	/**
	 * Odpowiedź z serwisu AI zwracana do przeglądarki.
	 *
	 * @param reply odpowiedź tekstowa wygenerowana przez AI
	 * @param toolsCalled lista narzędzi wywołanych przez model
	 */
	record AiResponse(String reply, @JsonProperty("tools_called") List<String> toolsCalled) {
	}

}
