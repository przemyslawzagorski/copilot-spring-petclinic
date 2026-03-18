# Spring PetClinic Documentation

Spring PetClinic is a reference Spring Boot web application for managing veterinary clinic operations.  
It demonstrates domain-driven modeling, layered MVC architecture, and profile-based database configuration.

## Documentation Sections

- [Introduction](introduction/introduction.md)
- [Configuration](configuration/configuration.md)
- [Architecture](architecture/architecture.md)
- [API Documentation](api/api.md)

## Quick Start

### Prerequisites

- Java 17+
- Maven (`mvnw`) or Gradle (`gradlew`)

### Run the application

```bash
./mvnw spring-boot:run
```

or

```bash
./gradlew bootRun
```

Application URL: <http://localhost:8080/>

### Run with a specific database profile

```bash
./mvnw spring-boot:run -Dspring-boot.run.profiles=mysql
```

```bash
./mvnw spring-boot:run -Dspring-boot.run.profiles=postgres
```
