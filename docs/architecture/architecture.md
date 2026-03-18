# Architecture

## Architectural Overview

Spring PetClinic is primarily an MVC web application built with Spring Boot and Spring Data JPA.  
Most features follow a layered model (`Controller -> Use Case/Repository -> Database`).

Inside the `owner` area, the visit flow additionally applies a lightweight hexagonal style:

- `VisitOwnerPort` defines a domain-facing port
- `OwnerRepositoryVisitAdapter` implements the port
- `VisitUseCase` orchestrates domain behavior

## C4 Context Diagram

```mermaid
C4Context
    title Spring PetClinic - System Context

    Person(ownerUser, "Clinic Staff/User", "Manages owners, pets, and visits")
    Person(vetUser, "Veterinarian", "Views veterinary information")

    System(petclinic, "Spring PetClinic", "Web application for veterinary clinic management")
    System_Ext(dbms, "Database", "H2 / MySQL / PostgreSQL")

    Rel(ownerUser, petclinic, "Uses via browser", "HTTPS")
    Rel(vetUser, petclinic, "Uses via browser", "HTTPS")
    Rel(petclinic, dbms, "Reads/Writes clinic data", "JDBC")
```

## C4 Container Diagram

```mermaid
C4Container
    title Spring PetClinic - Container View

    Person(user, "Clinic User", "Uses the UI")

    System_Boundary(petclinic_boundary, "Spring PetClinic") {
        Container(webapp, "Spring Boot MVC Application", "Java 17+, Spring Boot, Thymeleaf", "Serves HTML, handles requests, validates input")
        ContainerDb(database, "Relational Database", "H2 / MySQL / PostgreSQL", "Stores owners, pets, visits, vets, specialties")
    }

    Rel(user, webapp, "Uses", "HTTP :8080")
    Rel(webapp, database, "Reads from and writes to", "JPA/Hibernate over JDBC")
```

## C4 Component Diagram

```mermaid
C4Component
    title Spring PetClinic - Component View (Application Package Level)

    Container_Boundary(webapp, "Spring Boot MVC Application") {
        Component(systemPkg, "system package", "Spring MVC Config + Controllers", "WelcomeController, CrashController, CacheConfiguration, WebConfiguration")
        Component(ownerPkg, "owner package", "MVC + Use Case + Port/Adapter", "Owner/Pet/Visit flows, repositories, VisitUseCase")
        Component(vetPkg, "vet package", "MVC + Repository", "Veterinarian listing and data access")
        Component(modelPkg, "model package", "Domain base model", "BaseEntity, NamedEntity, Person")
    }

    ComponentDb(db, "Database", "H2/MySQL/PostgreSQL", "Persistent clinic records")

    Rel(systemPkg, ownerPkg, "Uses owner workflows")
    Rel(ownerPkg, modelPkg, "Extends and uses base entities")
    Rel(vetPkg, modelPkg, "Uses base entities")
    Rel(ownerPkg, db, "Persists and queries", "JPA")
    Rel(vetPkg, db, "Persists and queries", "JPA")
```

## Architectural Patterns

### MVC (Primary Pattern)

- Controllers handle request routing and validation boundaries.
- Views are rendered by Thymeleaf templates.
- Repositories and use-case components coordinate persistence and business flow.

### Hexagonal Influence in `owner` Visit Flow

- Port: `VisitOwnerPort`
- Adapter: `OwnerRepositoryVisitAdapter`
- Application service: `VisitUseCase`

This keeps visit orchestration decoupled from direct repository implementation details.

## Layered Flow

Typical execution path:

1. **Controller layer** receives web request and performs request-level validation.
2. **Use case / repository layer** executes business logic and persistence operations.
3. **Database layer** stores and retrieves domain data.
