# Configuration

## Runtime Profiles

Spring PetClinic supports three main runtime configurations:

- **default**: H2 in-memory database (`database=h2`)
- **mysql**: MySQL database profile
- **postgres**: PostgreSQL database profile

Use profiles via Spring Boot standard mechanisms (CLI, environment variable, IDE run config).

## Properties Reference (`application.properties`)

| Property | Default Value | Responsibility |
|---|---|---|
| `database` | `h2` | Selects SQL scripts folder for schema/data initialization. |
| `spring.sql.init.schema-locations` | `classpath*:db/${database}/schema.sql` | Points to schema SQL script based on selected `database`. |
| `spring.sql.init.data-locations` | `classpath*:db/${database}/data.sql` | Points to seed data SQL script based on selected `database`. |
| `spring.thymeleaf.mode` | `HTML` | Sets Thymeleaf template rendering mode. |
| `spring.jpa.hibernate.ddl-auto` | `none` | Disables automatic schema generation/update by Hibernate. |
| `spring.jpa.open-in-view` | `false` | Disables Open Session in View pattern to reduce persistence-layer leakage into views. |
| `spring.jpa.hibernate.naming.physical-strategy` | `org.hibernate.boot.model.naming.PhysicalNamingStrategySnakeCaseImpl` | Maps logical names to snake_case physical database names. |
| `spring.jpa.properties.hibernate.default_batch_fetch_size` | `16` | Improves performance by batching relationship fetches. |
| `spring.messages.basename` | `messages/messages` | Base name for i18n message bundles. |
| `management.endpoints.web.exposure.include` | `*` | Exposes all Actuator endpoints over HTTP (subject to security/runtime controls). |
| `logging.level.org.springframework` | `INFO` | Configures Spring framework logging level. |
| `spring.web.resources.cache.cachecontrol.max-age` | `12h` | Sets static resource browser cache duration. |

## Database-Specific Properties

### MySQL (`application-mysql.properties`)

| Property | Default / Pattern | Responsibility |
|---|---|---|
| `database` | `mysql` | Selects MySQL SQL scripts under `db/mysql`. |
| `spring.datasource.url` | `${MYSQL_URL:jdbc:mysql://localhost/petclinic}` | JDBC URL, overridable by `MYSQL_URL`. |
| `spring.datasource.username` | `${MYSQL_USER:petclinic}` | Database user, overridable by `MYSQL_USER`. |
| `spring.datasource.password` | `${MYSQL_PASS:petclinic}` | Database password, overridable by `MYSQL_PASS`. |
| `spring.sql.init.mode` | `always` | Always runs SQL init scripts; scripts are idempotent. |

### PostgreSQL (`application-postgres.properties`)

| Property | Default / Pattern | Responsibility |
|---|---|---|
| `database` | `postgres` | Selects PostgreSQL SQL scripts under `db/postgres`. |
| `spring.datasource.url` | `${POSTGRES_URL:jdbc:postgresql://localhost/petclinic}` | JDBC URL, overridable by `POSTGRES_URL`. |
| `spring.datasource.username` | `${POSTGRES_USER:petclinic}` | Database user, overridable by `POSTGRES_USER`. |
| `spring.datasource.password` | `${POSTGRES_PASS:petclinic}` | Database password, overridable by `POSTGRES_PASS`. |
| `spring.sql.init.mode` | `always` | Always runs SQL init scripts; scripts are idempotent. |

## Running with Docker Compose

The repository provides `docker-compose.yml` with profile-specific services.

Start MySQL container:

```bash
docker compose up mysql
```

Start PostgreSQL container:

```bash
docker compose up postgres
```

Then run application with the matching Spring profile (`mysql` or `postgres`).

## Environment Variables

You can customize external database connectivity through:

- MySQL: `MYSQL_URL`, `MYSQL_USER`, `MYSQL_PASS`
- PostgreSQL: `POSTGRES_URL`, `POSTGRES_USER`, `POSTGRES_PASS`

This enables local overrides and CI/CD-friendly configuration without modifying source files.
