# API Design

## 1. API Overview

The Enterprise Device Management System will expose REST APIs through the
FastAPI backend.

The Next.js frontend will communicate with the backend exclusively through
these APIs.

### API Flow


Next.js
   |
   | HTTPS / JSON
   v
FastAPI REST API
   |
   v
Service Layer
   |
   v
Repository Layer
   |
   v
PostgreSQL


The API will be responsible for:

- Request validation
- Authentication
- Authorization
- Business operations
- Data retrieval
- Error handling
- Consistent response formatting


## 2. API Design Principles

The API will follow REST-oriented design principles.

### Resource-Oriented URLs

URLs will represent resources rather than actions.

Example:


GET    /api/v1/devices
POST   /api/v1/devices
GET    /api/v1/devices/{device_id}
PATCH  /api/v1/devices/{device_id}
DELETE /api/v1/devices/{device_id}


Action-oriented URLs such as:


/getDevices
/createDevice
/updateDevice


will be avoided.

### API Versioning

APIs will be versioned using the URL path.


/api/v1/...


This allows future versions to evolve without immediately breaking
existing clients.

### JSON

JSON will be used as the primary request and response format.

### Authentication

Protected APIs will require a valid JWT access token.

http
Authorization: Bearer <access_token>


### Authorization

APIs will enforce RBAC permissions at the backend.

Frontend visibility controls will not be treated as a security mechanism.

### Pagination

List endpoints will support pagination.

Example:


GET /api/v1/devices?page=1&page_size=20


### Filtering

List endpoints will support relevant filters.

Example:


GET /api/v1/devices?status=OFFLINE&branch_id={branch_id}


### Sorting

List endpoints may support sorting where useful.

Example:


GET /api/v1/devices?sort_by=last_seen_at&sort_order=desc


### Consistent Errors

API errors will follow the application's standard error structure.

json
{
  "error": {
    "code": "DEVICE_NOT_FOUND",
    "message": "Device not found",
    "details": null
  }
}



## 3. HTTP Methods and Status Codes

### HTTP Methods

| Method | Purpose |
|---|---|
| GET | Retrieve resources |
| POST | Create resources or perform operations that create a new resource |
| PATCH | Partially update a resource |
| DELETE | Delete a resource where deletion is permitted |

### Common HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource successfully created |
| 204 | Successful request with no response body |
| 400 | Invalid request |
| 401 | Authentication required or invalid |
| 403 | User is not authorized |
| 404 | Resource not found |
| 409 | Resource conflict |
| 422 | Request validation failure |
| 500 | Unexpected server error |


## 4. Authentication APIs

### Login


POST /api/v1/auth/login


Purpose:

Authenticate a user and issue access and refresh tokens.

Authentication:

Not required.

Request:

json
{
  "email": "user@example.com",
  "password": "password"
}


Response:

json
{
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>",
  "token_type": "bearer"
}


---

### Refresh Token


POST /api/v1/auth/refresh


Purpose:

Generate a new access token using a valid refresh token.

Request:

json
{
  "refresh_token": "<refresh_token>"
}


Response:

json
{
  "access_token": "<new_access_token>",
  "token_type": "bearer"
}


---

### Get Current User


GET /api/v1/auth/me


Purpose:

Return information about the currently authenticated user.

Authentication:

Required.

Permission:

Authenticated user.

Response:

json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "roles": [
    "Support Engineer"
  ]
}



## 5. User APIs

### List Users


GET /api/v1/users


Purpose:

Retrieve users with pagination and filtering.

Permission:


user:read


Example:


GET /api/v1/users?page=1&page_size=20&status=ACTIVE


---

### Get User


GET /api/v1/users/{user_id}


Permission:


user:read


---

### Create User


POST /api/v1/users


Permission:


user:create


Request:

json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password"
}


---

### Update User


PATCH /api/v1/users/{user_id}


Permission:


user:update


---

### Deactivate User


PATCH /api/v1/users/{user_id}/status


Permission:


user:update


Request:

json
{
  "status": "INACTIVE"
}



## 6. Role APIs

### List Roles


GET /api/v1/roles


Permission:


role:read


### Create Role


POST /api/v1/roles


Permission:


role:create


### Update Role


PATCH /api/v1/roles/{role_id}


Permission:


role:update


### Assign Role to User


POST /api/v1/users/{user_id}/roles


Permission:


user:manage


Request:

json
{
  "role_id": "uuid"
}


### Remove Role from User


DELETE /api/v1/users/{user_id}/roles/{role_id}


Permission:


user:manage



## 7. Permission APIs

### List Permissions


GET /api/v1/permissions


Permission:


permission:read


### Assign Permission to Role


POST /api/v1/roles/{role_id}/permissions


Permission:


role:manage


Request:

json
{
  "permission_id": "uuid"
}


### Remove Permission from Role


DELETE /api/v1/roles/{role_id}/permissions/{permission_id}


Permission:


role:manage



## 8. Business Domain APIs

### List Business Domains


GET /api/v1/business-domains


Permission:


domain:read


### Get Business Domain


GET /api/v1/business-domains/{domain_id}


Permission:


domain:read


### Create Business Domain


POST /api/v1/business-domains


Permission:


domain:create


Request:

json
{
  "name": "Retail Banking",
  "description": "Retail banking operations"
}


### Update Business Domain


PATCH /api/v1/business-domains/{domain_id}


Permission:


domain:update



## 9. Branch APIs

### List Branches


GET /api/v1/branches


Supports:


page
page_size
status
business_domain_id
search


Example:


GET /api/v1/branches?status=OPEN&business_domain_id={domain_id}


Permission:


branch:read


### Get Branch


GET /api/v1/branches/{branch_id}


Permission:


branch:read


### Create Branch


POST /api/v1/branches


Permission:


branch:create


Request:

json
{
  "branch_code": "BR001",
  "name": "Boisar Branch",
  "business_domain_id": "uuid",
  "address": "Example Address",
  "city": "Boisar",
  "status": "OPEN"
}


### Update Branch


PATCH /api/v1/branches/{branch_id}


Permission:


branch:update


### Change Branch Status


PATCH /api/v1/branches/{branch_id}/status


Permission:


branch:update


Request:

json
{
  "status": "CLOSED"
}



## 10. Device APIs

This is the primary API group in the project.

### List Devices


GET /api/v1/devices


Supports:


page
page_size
status
branch_id
device_type_id
business_domain_id
search
sort_by
sort_order


Example:


GET /api/v1/devices?status=OFFLINE&branch_id={branch_id}&page=1&page_size=20


Permission:


device:read


Response:

json
{
  "items": [
    {
      "id": "uuid",
      "device_identifier": "SCN-00123",
      "serial_number": "SN123456",
      "device_type": "Scanner",
      "branch": {
        "id": "uuid",
        "name": "Boisar Branch"
      },
      "status": "OFFLINE",
      "firmware_version": "4.2.1",
      "last_seen_at": "2026-08-13T12:30:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}


---

### Get Device


GET /api/v1/devices/{device_id}


Permission:


device:read


Response:

json
{
  "id": "uuid",
  "device_identifier": "SCN-00123",
  "serial_number": "SN123456",
  "device_type": "Scanner",
  "manufacturer": "Example",
  "model": "Scanner X",
  "branch": {
    "id": "uuid",
    "name": "Boisar Branch"
  },
  "status": "OFFLINE",
  "firmware_version": "4.2.1",
  "certificate_status": "VALID",
  "last_seen_at": "2026-08-13T12:30:00Z"
}


---

### Create Device


POST /api/v1/devices


Permission:


device:create


Request:

json
{
  "device_identifier": "SCN-00123",
  "serial_number": "SN123456",
  "device_type_id": "uuid",
  "branch_id": "uuid",
  "manufacturer": "Example",
  "model": "Scanner X",
  "ip_address": "10.10.10.10",
  "status": "ONLINE",
  "firmware_version": "4.2.1"
}


---

### Update Device


PATCH /api/v1/devices/{device_id}


Permission:


device:update


Request:

json
{
  "status": "MAINTENANCE",
  "firmware_version": "4.3.0"
}


---

### Change Device Status


PATCH /api/v1/devices/{device_id}/status


Permission:


device:update


Request:

json
{
  "status": "OFFLINE"
}


---

### Move Device to Another Branch


PATCH /api/v1/devices/{device_id}/branch


Permission:


device:update


Request:

json
{
  "branch_id": "uuid"
}


---

### Decommission Device

Physical deletion will generally be avoided for operational devices.

Instead:


PATCH /api/v1/devices/{device_id}/status


with:

json
{
  "status": "DECOMMISSIONED"
}


Permission:


device:update



## 11. Device Type APIs

### List Device Types


GET /api/v1/device-types


Permission:


device_type:read


### Create Device Type


POST /api/v1/device-types


Permission:


device_type:create


### Update Device Type


PATCH /api/v1/device-types/{device_type_id}


Permission:


device_type:update



## 12. Incident APIs

Incident functionality is intentionally lightweight and primarily provides
operational context for devices and branches.

### List Incidents


GET /api/v1/incidents


Supports:


page
page_size
status
priority
device_id
branch_id


Permission:


incident:read


### Get Incident


GET /api/v1/incidents/{incident_id}


Permission:


incident:read


### Create Incident


POST /api/v1/incidents


Permission:


incident:create


Request:

json
{
  "title": "Scanner offline",
  "description": "Scanner is not responding",
  "status": "OPEN",
  "priority": "HIGH",
  "device_id": "uuid",
  "branch_id": "uuid"
}


### Update Incident


PATCH /api/v1/incidents/{incident_id}


Permission:


incident:update


Example:

json
{
  "status": "RESOLVED"
}



## 13. Dashboard APIs

### Dashboard Summary


GET /api/v1/dashboard/summary


Purpose:

Return high-level operational statistics.

Permission:


dashboard:read


Response:

json
{
  "devices": {
    "total": 1250,
    "online": 1180,
    "offline": 40,
    "maintenance": 20,
    "decommissioned": 10
  },
  "branches": {
    "total": 500,
    "open": 480,
    "closed": 20
  },
  "incidents": {
    "open": 25,
    "critical": 4
  }
}


### Device Status Summary


GET /api/v1/dashboard/devices/status


Returns device counts grouped by status.

### Incident Summary


GET /api/v1/dashboard/incidents/summary


Returns incident counts grouped by status and priority.


## 14. Audit APIs

### List Audit Logs


GET /api/v1/audit-logs


Supports:


page
page_size
user_id
entity_type
entity_id
action
from_date
to_date


Permission:


audit:read


Audit logs will be read-only through the API.

The application will not expose an API that allows normal users to modify
or delete audit records.


## 15. Response Standards

### Single Resource

Single-resource responses will return the resource directly.

Example:

json
{
  "id": "uuid",
  "name": "Boisar Branch",
  "status": "OPEN"
}


### Collection Response

Collection APIs will return pagination metadata.

Example:

json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 100
}


### Pagination

List endpoints will use:


page
page_size


Example:


GET /api/v1/devices?page=2&page_size=25


The backend will enforce a maximum page size to prevent excessively large
requests.

### Error Response

All API errors will follow a consistent structure:

json
{
  "error": {
    "code": "DEVICE_NOT_FOUND",
    "message": "Device not found",
    "details": null
  }
}



## 16. API Security

All protected APIs require a valid JWT access token.

http
Authorization: Bearer <access_token>


Authentication establishes the identity of the user.

Authorization determines whether the user has the required permission.

For example:


GET /api/v1/devices
        |
        v
Authentication
        |
        v
Authorization
        |
        v
device:read
        |
        v
Allow / Deny


Authorization will always be enforced on the backend.

The frontend may hide functionality that the user cannot access, but this
will not be considered a security control.

Sensitive information such as passwords, access tokens, and secrets will
not be returned in API responses.


## 17. API Documentation

FastAPI will automatically generate an OpenAPI specification for the
application.

Interactive API documentation will be available during development to
allow developers to:

- Explore available endpoints
- View request schemas
- View response schemas
- Test APIs
- Understand authentication requirements

The API contract will be maintained alongside the application code.

The OpenAPI specification will serve as the primary technical reference
for frontend-backend integration.


## 18. API Design Summary

The EDMS backend will expose versioned REST APIs through FastAPI.

The API design follows these principles:

- Resource-oriented URLs
- HTTP methods aligned with CRUD operations
- API versioning
- JWT-based authentication
- Backend-enforced RBAC authorization
- Request validation
- Pagination
- Filtering
- Sorting where required
- Consistent response structures
- Consistent error handling
- OpenAPI documentation

The primary API resources are:


/api/v1/auth
/api/v1/users
/api/v1/roles
/api/v1/permissions
/api/v1/business-domains
/api/v1/branches
/api/v1/device-types
/api/v1/devices
/api/v1/incidents
/api/v1/audit-logs
/api/v1/dashboard


The API design is intentionally focused on the core MVP requirements.
Additional endpoints will only be introduced when required by actual
application functionality.
