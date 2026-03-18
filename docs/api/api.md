# API Documentation

## Overview

Spring PetClinic is primarily an MVC application that serves HTML pages.  
Most endpoints return rendered views and perform redirects after successful form submissions.

## MVC Endpoints by Controller

### WelcomeController

| Method | URL | Description |
|---|---|---|
| GET | `/` | Displays the application welcome page. |

### CrashController

| Method | URL | Description |
|---|---|---|
| GET | `/oups` | Intentionally throws an exception to demonstrate error handling. |

### OwnerController

| Method | URL | Description |
|---|---|---|
| GET | `/owners/new` | Displays owner creation form. |
| POST | `/owners/new` | Creates a new owner. |
| GET | `/owners/find` | Displays owner search form. |
| GET | `/owners` | Searches owners (supports pagination via `page` query parameter). |
| GET | `/owners/{ownerId}` | Displays owner details. |
| GET | `/owners/{ownerId}/edit` | Displays owner edit form. |
| POST | `/owners/{ownerId}/edit` | Updates owner data. |
| GET | `/owners/delete/{ownerId}` | Deletes owner by id. |

### PetController (under owner scope)

| Method | URL | Description |
|---|---|---|
| GET | `/owners/{ownerId}/pets/new` | Displays pet creation form for selected owner. |
| POST | `/owners/{ownerId}/pets/new` | Creates pet for selected owner. |
| GET | `/owners/{ownerId}/pets/{petId}/edit` | Displays pet edit form. |
| POST | `/owners/{ownerId}/pets/{petId}/edit` | Updates pet details. |

### VisitController

| Method | URL | Description |
|---|---|---|
| GET | `/owners/{ownerId}/pets/{petId}/visits/new` | Displays visit booking form for a pet. |
| POST | `/owners/{ownerId}/pets/{petId}/visits/new` | Books a new visit. |

### VetController

| Method | URL | Description |
|---|---|---|
| GET | `/vets.html` | Displays paginated vet list view (`page` query parameter). |
| GET | `/vets` | Returns vets in a data-oriented representation (`Vets` wrapper). |

## Actuator Endpoints

Actuator web exposure is configured as:

- `management.endpoints.web.exposure.include=*`

This means all available actuator endpoints are exposed by configuration.  
Commonly used endpoints include:

- `/actuator/health`
- `/actuator/info`
- `/actuator/metrics`
- `/actuator/env`
- `/actuator/beans`
- `/actuator/mappings`

> Actual response shape and available endpoints depend on runtime setup, dependencies, and security configuration.

## Example Requests and Responses

### Example 1: Open owner search screen

**Request**

```http
GET /owners/find HTTP/1.1
Host: localhost:8080
```

**Response (conceptual)**

- Status: `200 OK`
- Content-Type: `text/html`
- Body: rendered owner search page.

### Example 2: Create owner

**Request**

```http
POST /owners/new HTTP/1.1
Host: localhost:8080
Content-Type: application/x-www-form-urlencoded

firstName=John&lastName=Doe&address=Main+Street&city=Warsaw&telephone=123456789
```

**Response (success path)**

- Status: `302 Found`
- Redirect: `/owners/{newOwnerId}`

### Example 3: Actuator health

**Request**

```http
GET /actuator/health HTTP/1.1
Host: localhost:8080
```

**Response (typical)**

```json
{
  "status": "UP"
}
```
