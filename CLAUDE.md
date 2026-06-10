# Reguły dla Claude Code w tym projekcie

## Reguły kodu

- Język kodu: Java 17+, używaj rekordów zamiast POJO gdzie to możliwe.
- Framework: Spring Boot 4.x, Spring Data JPA.
- Testy: JUnit 5 + Mockito. Nigdy JUnit 4.
- Nazewnictwo: camelCase, klasy z dużej litery, pakiety lowercase.
- Komentarze: Javadoc po polsku dla klas publicznych.
- Bezpieczeństwo: zawsze waliduj dane wejściowe. Nigdy nie loguj haseł.

## Struktura projektu

```
copilot-spring-petclinic/
├── src/main/java/org/springframework/samples/petclinic/
│   ├── ai/              # AI Assistant Controller (ex_30 live demo)
│   ├── model/           # BaseEntity, Person
│   ├── owner/           # Owner, Pet, Visit, OwnerController
│   ├── vet/             # Vet, Specialty, VetController
│   └── system/          # CacheConfig, WelcomeController
├── src/test/java/       # Testy JUnit 5 + Mockito
├── szkol_referencja/    # Materiały szkoleniowe (Copilot + Claude Code)
│   ├── copilot_training_self_paced/   # 10 modułów szkolenia Copilot
│   └── claude_code_guide/            # Przewodnik Claude Code (START TUTAJ)
├── .github/             # Konfiguracja Copilot (agents/, skills/, hooks/, prompts/)
├── .claude/             # Konfiguracja Claude Code (agents/, skills/)
├── docs/                # Dokumentacja MkDocs
└── pom.xml              # Java 17, Spring Boot 4.0.3
```

## Uruchamianie projektu

```bash
./mvnw spring-boot:run    # Maven (zalecane)
./gradlew bootRun         # Gradle
# Aplikacja: http://localhost:8080
```

## Materiały szkoleniowe

Szkolenie dotyczy GitHub Copilot, ale zawiera też adaptacje dla Claude Code:
- `szkol_referencja/claude_code_guide/README.md` — przewodnik Claude Code (start tutaj)
- W każdym module szkolenia znajdziesz `CLAUDE_CODE.md` z adaptacją ćwiczeń

## Dla uczestnika szkolenia Claude Code

Pliki konfiguracyjne Claude Code w tym projekcie:
- `.claude/agents/` — subagenci (mentor, reviewer, tdd-expert, security-expert, feature-builder)
- `.claude/skills/` — slash commands (/project-versions, /method-deep-dive, /controller-testing, /dependency-check)
- `.claude/settings.json` — uprawnienia i hooki
- `.mcp.json` — serwery MCP

Zacznij od: `szkol_referencja/claude_code_guide/README.md`
