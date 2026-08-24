# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Code rules

- **Java:** 17+, use records instead of POJOs where feasible
- **Framework:** Spring Boot 4.0.3, Spring Data JPA
- **Tests:** JUnit 5 + Mockito exclusively (never JUnit 4)
- **Naming:** camelCase for methods/vars, PascalCase for classes, lowercase for packages
- **Security:** Always validate input at system boundaries; never log passwords or secrets
- **Code formatting:** Runs via Maven plugin (`mvn spring-javaformat:apply`); committed code should be pre-formatted

## Project structure

```
src/main/java/org/springframework/samples/petclinic/
├── ai/              # AI Assistant chat controller + Thymeleaf UI (ex_30)
├── model/           # BaseEntity, Person (base classes)
├── owner/           # Owner, Pet, Visit entities and OwnerController
├── vet/             # Vet, Specialty entities and VetController
└── system/          # CacheConfig, WelcomeController, app-level setup

src/test/java/      # Test classes (JUnit 5 + Mockito)
docs/               # MkDocs documentation
```

## Common tasks

**Run application:**
```bash
./mvnw spring-boot:run
# Then http://localhost:8080
```

**Run tests:**
```bash
./mvnw test                    # All tests
./mvnw test -Dtest=OwnerTests  # Specific test class
```

**Code quality:**
```bash
./mvnw clean verify            # Full build + tests + code checks
./mvnw checkstyle:check        # Checkstyle only
./mvnw jacoco:report           # Code coverage report (target/site/jacoco/index.html)
./mvnw spring-javaformat:apply # Format code (must do before commit)
```

**Database:**
- Default: H2 in-memory (auto-populated at startup)
- H2 console: http://localhost:8080/h2-console
- Switch to MySQL: `./mvnw spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=mysql"`
- Switch to PostgreSQL: `./mvnw spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=postgres"`

## Claude Code tools in this project

**Agents** (in `.claude/agents/`):
- `mentor` — guides through training modules step-by-step
- `reviewer` — reviews Spring MVC controllers for quality/security (read-only)
- `tdd-expert` — leads Red-Green-Refactor cycle with JUnit 5
- `security-expert` — analyzes code for OWASP vulnerabilities (read-only)
- `feature-builder` — builds new features by understanding architecture first
- `exercise-validator` — validates training material consistency
- `mkdocs-documentation` — generates/updates MkDocs docs

**MCP servers** (in `.mcp.json`):
- `devkit` — DevKit RAG: `web_search`/`read_page` (Tavily, Jina Reader), `deep_research`,
  pamięć wektorowa Qdrant (`memory_*`), RAG po repo (`index_path` + `ask_repo`),
  delegowanie podzadań do Groq (`delegate`). Zasoby: `devkit://status`,
  `devkit://repo/profile`, `devkit://cheatsheet`. Kod: `szkol_referencja/copilot_training_self_paced/mcp_devkit/`,
  klucze API w `mcp_devkit/.env` (nigdy w `.mcp.json`).
- `publiczne-api` — demo: kursy NBP, Pokemon, żarty + zasoby `nbp://rates/*` i przepływy
- `jira-wiki` — Jira & Confluence (wymaga `.env` w `mcp_jira_wiki/`)

**Skills** (slash commands):
- `/project-versions` — shows Java, Spring Boot, Maven versions
- `/method-deep-dive` — analyzes a method's flow, dependencies, security risks
- `/controller-testing` — generates MockMvc integration tests for controllers
- `/dependency-check` — scans for dependency vulnerabilities

## Architecture notes

**AI Assistant (ex_30):**
The `ai/` package contains a live demo of a simple AI-powered chat interface. The `AiAssistantController` processes user messages and integrates with a Thymeleaf template. This is not production code — it's a teaching example.

**Entity hierarchy:**
- `BaseEntity` — base class with ID and equality
- `Person` — base for user types (Owner, Vet)
- `NamedEntity` — entity with a `name` field (Specialty, etc.)

**Caching:**
Default caching is configured in `CacheConfig`. Pets and vets are cached; owners are not. Cache keys follow Spring conventions.

## Training materials

This project includes self-paced training modules:
- `szkol_referencja/copilot_training_self_paced/` — 10 GitHub Copilot modules (modules 01–10)
- `szkol_referencja/claude_code_guide/` — Claude Code adaptation guide

Each module includes a `CLAUDE_CODE.md` file explaining how exercises differ when using Claude Code instead of Copilot.
