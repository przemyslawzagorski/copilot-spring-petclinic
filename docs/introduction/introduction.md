# Introduction

## Project Purpose

Spring PetClinic is a sample business application that models daily operations in a veterinary clinic.  
Its goal is to provide a practical, production-style Spring Boot codebase for learning, extension, and architectural exploration.

## Business Domain

The application supports core clinic workflows:

- Managing owners and their contact details
- Managing pets assigned to owners
- Recording pet visits
- Managing veterinarians and their specialties
- Navigating clinic information through server-rendered web pages

## Main Functional Areas

### Owner Management

Users can create, search, update, and delete owner records, then open owner details.

### Pet Management

Within each owner context, users can add and update pets, including type and birth date.

### Visit Management

Users can schedule visits for specific pets under a selected owner.

### Veterinarian Management

Users can view veterinarians in HTML and JSON-oriented representations.

## Technology Stack

- Java 17+
- Spring Boot (web MVC, validation, actuator, cache)
- Spring Data JPA + Hibernate
- Thymeleaf templates for server-side rendering
- Databases:
  - H2 (default, in-memory)
  - MySQL (profile: `mysql`)
  - PostgreSQL (profile: `postgres`)
- Build tools: Maven and Gradle
