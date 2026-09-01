# System Architecture

## 1. Architecture Overview

The Enterprise Device Management System (EDMS) is a web-based enterprise
application designed to provide centralized management and operational
visibility of devices deployed across multiple business domains and branch
locations.

The system follows a modular monolith architecture with a Next.js frontend,
FastAPI backend, and PostgreSQL database.

The architecture is designed to provide clear separation of concerns,
secure access control, maintainability, and future extensibility.

---

## 2. Architecture Goals

The architecture is designed around the following goals:

- Clear separation of frontend, application, and data responsibilities.
- Secure authentication and authorization.
- Maintainable and modular backend architecture.
- Strong data integrity.
- Efficient search, filtering, and reporting.
- Support for future caching and background processing.
- Production-oriented logging and observability.
- Containerized and reproducible deployment.
- Ability to integrate with external enterprise systems in the future.

---

## 3. Architecture Style

The system will initially follow a **modular monolith architecture**.

The application will be deployed as a single backend application while
maintaining logical boundaries between functional modules such as:

- Authentication
- Users
- Roles and Permissions
- Business Domains
- Branches
- Devices
- Incidents
- Reporting
- Audit

A modular monolith is preferred over microservices for the initial version
because the system does not require independent service deployment or
distributed processing at its current scale.

The modular structure will allow individual modules to evolve independently
and provides a potential path toward service extraction if future scale or
organizational requirements justify it.

---

## 4. System Context

The EDMS is used by multiple categories of users:

- System Administrators
- Operations Managers
- Support Engineers
- Branch Users
- Auditors / Read-Only Users

The system may integrate with external enterprise services in future
iterations, including:

- Enterprise Identity Provider / SSO
- Notification Services
- Device Monitoring Platforms
- ITSM Platforms

The initial implementation will simulate device operational data rather
than directly communicating with physical scanner hardware.

---

## 5. System Context Diagram

The system context can be represented as:

System Administrator ───────┐
                            │
Operations Manager ─────────┤
                            │
Support Engineer ───────────┤
                            ▼
Branch User ─────────────► EDMS
                            ▲
Auditor ────────────────────┘
                            │
                            ├──── Enterprise Identity Provider
                            │
                            └──── Notification Service

## 5. High-Level Architecture

The system follows a layered modular monolith architecture.

The major components are:

1. Next.js frontend
2. FastAPI backend
3. PostgreSQL database

Future components such as Redis caching and background workers may be
introduced when justified by application requirements.


                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                              HTTPS
                                │
                                ▼
                    ┌─────────────────────┐
                    │       Next.js       │
                    │      Frontend       │
                    │                     │
                    │ UI / Forms / Tables │
                    │ Charts / Navigation │
                    └──────────┬──────────┘
                               │
                           REST / JSON
                               │
                               ▼
        ┌─────────────────────────────────────────┐
        │                  FastAPI                │
        │                                         │
        │ Authentication / Authorization          │
        │                                         │
        │ ┌────────────┐     ┌───────────────┐   │
        │ │  Routers   │ ──► │   Services    │   │
        │ └────────────┘     └───────┬───────┘   │
        │                            │            │
        │                     ┌──────▼──────┐     │
        │                     │ Repositories │     │
        │                     └──────┬──────┘     │
        │                            │            │
        │ Modules:                  │            │
        │ Users                     │            │
        │ Branches                  │            │
        │ Devices                   │            │
        │ Incidents                 │            │
        │ Reporting                 │            │
        │ Audit                     │            │
        └────────────────────────────┼────────────┘
                                     │
                                     │ SQL
                                     ▼
                            ┌─────────────────┐
                            │   PostgreSQL    │
                            │                 │
                            │ Users           │
                            │ Branches        │
                            │ Devices         │
                            │ Incidents       │
                            │ Audit Logs      │
                            └─────────────────┘

                         Future Components
                         ──────────────────

                         ┌──────────────┐
                         │    Redis     │
                         │    Cache     │
                         └──────────────┘

                         ┌──────────────┐
                         │ Job / Worker │
                         │   System     │
                         └──────────────┘

## 6. Component Responsibilities

Next.js Frontend

Responsible for:

User interface
Navigation
Forms
Tables
Charts
Client-side interactions
Frontend validation
API communication
Loading and error states

The frontend must not be responsible for enforcing application
authorization rules.

FastAPI Backend

Responsible for:

REST APIs
Authentication
Authorization
Request validation
Business logic
Database access
Audit logging
Error handling
Application logging
PostgreSQL Database

Responsible for:

Persistent data storage
Relationships
Constraints
Transactions
Indexes
Query execution
Data integrity

## 7. Backend Architecture

Router
   |
   v
Service
   |
   v
Repository
   |
   v
PostgreSQL

Backend Modules

The FastAPI application will be organized into logical modules:

Authentication
Users
Roles and Permissions
Business Domains
Branches
Devices
Incidents
Dashboard
Reporting
Audit

These modules will operate within a single deployable application while
maintaining clear logical boundaries.

## 8. Data Flow

The application follows a request-response flow between the frontend,
backend, and database.

For a device search operation:

1. The user submits search criteria through the Next.js frontend.
2. Next.js sends a REST API request to the FastAPI backend.
3. The backend authenticates the request.
4. The backend validates the user's authorization.
5. The Device Router receives the request.
6. The Device Service applies relevant business rules.
7. The Device Repository retrieves the required data from PostgreSQL.
8. The result is returned through the service and router layers.
9. FastAPI returns a JSON response to the frontend.
10. Next.js renders the results to the user.

The frontend does not directly access the database.


## 9. Authentication Flow

The MVP will use application-managed authentication using username/password
credentials and JWT-based authentication.

### Login

1. The user submits credentials through the Next.js frontend.
2. Next.js sends the credentials to the FastAPI authentication endpoint.
3. FastAPI retrieves the corresponding user from PostgreSQL.
4. FastAPI verifies the supplied password against the stored password hash.
5. If authentication succeeds, FastAPI generates an access token and refresh
   token.
6. The tokens are returned to the frontend.
7. The frontend uses the access token when calling protected APIs.

### Protected API Requests

1. Next.js sends the access token with the API request.
2. FastAPI validates the token.
3. FastAPI identifies the authenticated user.
4. The request proceeds to authorization and application processing.

Access tokens will be short-lived, while refresh tokens will be used to
obtain new access tokens when required.

The MVP will use application-managed authentication. Future versions may
integrate with an enterprise Identity Provider using OAuth 2.0/OpenID
Connect.

## 10. Authorization Flow

The system will use Role-Based Access Control (RBAC) to control access to
application functionality.

After a user's identity has been established through authentication, the
backend evaluates whether the user has the required permission for the
requested operation.

The authorization flow is:

1. The user sends an authenticated API request.
2. FastAPI validates the user's authentication token.
3. The authenticated user's role and permissions are identified.
4. The backend checks whether the required permission exists.
5. If the user is authorized, the request proceeds to the relevant service.
6. If the user is not authorized, the API returns an appropriate
   authorization error.

The initial application roles are:

- Administrator
- Operations Manager
- Support Engineer
- Branch User
- Read-Only User

Permissions will be represented independently from roles so that
permissions can be reused and roles can evolve without changing the
application's core business logic.

The system may also enforce data-level authorization. For example, a Branch
User may be permitted to view devices but restricted to devices belonging
to their assigned branch.

Authorization will always be enforced at the backend. Frontend visibility
controls will be treated as a user-experience feature and not as a security
mechanism.

## 11. Error Handling

The application will use centralized error handling to provide consistent
and predictable API responses.

Errors will be categorized according to their nature.

### Validation Errors

Invalid request data will result in an appropriate client error response.

### Authentication Errors

Requests with missing, invalid, or expired authentication credentials will
return an HTTP 401 response.

### Authorization Errors

Authenticated users attempting to perform an operation for which they do
not have sufficient permissions will receive an HTTP 403 response.

### Resource Errors

Requests for resources that do not exist will return an HTTP 404 response.

### Unexpected Errors

Unexpected application or infrastructure errors will return a generic HTTP
500 response to the client.

Detailed internal information will not be exposed to the client.

### Error Response Format

The API will use a consistent error structure:

{
  "error": {
    "code": "DEVICE_NOT_FOUND",
    "message": "Device not found",
    "details": null
  }
}

Application errors will be logged internally with sufficient context for
troubleshooting while avoiding sensitive information.

A centralized exception-handling mechanism will be used so that individual
API endpoints do not need to implement repetitive error-handling logic.

## 12. Logging and Observability

The application will implement structured application logging to support
troubleshooting and operational visibility.

Application logs will capture relevant information such as:

- Timestamp
- Log level
- Request ID
- User ID where applicable
- HTTP method
- API endpoint
- Response status
- Request duration
- Error information where applicable

Sensitive information such as passwords, authentication tokens, and
application secrets must never be written to logs.

### Request IDs

Each API request should have a unique request identifier.

The request ID will allow developers and operators to trace an operation
through the application and correlate related log entries.

### Log Levels

The application will use appropriate log levels:

- DEBUG
- INFO
- WARNING
- ERROR

### Audit vs Application Logging

Application logging and audit logging serve different purposes.

Application logs are intended for troubleshooting and operational
visibility.

Audit logs record important user actions and changes to business data for
accountability and traceability.

The application will initially rely on structured application logs and
health endpoints for observability. Dedicated metrics and monitoring
platforms may be introduced in future iterations if required.

## 13. Caching Strategy

The primary source of truth for application data will be PostgreSQL.

Redis will not be required for the initial MVP.

Caching may be introduced for data that is frequently accessed and
relatively expensive to calculate.

Potential caching candidates include:

- Dashboard statistics
- Frequently accessed reference data
- Other read-heavy data identified through performance analysis

The application will avoid caching transactional data where stale values
could lead to incorrect business decisions.

### Cache Invalidation

The initial caching strategy may use time-based expiration (TTL) for
suitable read-heavy data.

Where required, application events may be used to invalidate affected
cache entries.

Caching will be introduced based on measured application requirements
rather than added solely for architectural complexity.

### Initial Architecture
Next.js
   |
   v
FastAPI
   |
   v
PostgreSQL

## 14. Background Processing

The initial MVP will primarily process operations synchronously through the
FastAPI application.

Background processing may be introduced for operations that are
long-running, resource-intensive, or do not need to block the user's API
request.

Potential use cases include:

- Bulk device imports
- Large report generation
- Notification delivery
- Device health processing
- Scheduled operational tasks

A background job architecture may use a message broker and worker process,
such as Redis and Celery.

### Example
User
  |
  v
FastAPI
  |
  | Create Job
  v
Job Queue
  |
  v
Worker
  |
  v
PostgreSQL / External Service

## 15. Scalability Considerations

The initial system is designed as a modular monolith. Scalability will be
addressed primarily through efficient application and database design
before introducing distributed architecture.

### Application Scalability

The backend should remain stateless wherever practical so that multiple
backend instances can be deployed behind a load balancer if required.

User session state should not depend on local application memory.

### Database Scalability

PostgreSQL will remain the primary source of truth.

The database design will consider:

- Appropriate indexes
- Efficient queries
- Connection pooling
- Pagination
- Transaction management
- Avoidance of unnecessary database queries

Database performance will be evaluated using query analysis and application
monitoring as the dataset grows.

### Caching

Redis may be introduced for read-heavy workloads such as dashboard
statistics and frequently accessed reference data.

### Background Processing

Long-running operations may be moved to background workers to prevent them
from consuming API resources.

### Horizontal Scaling

If application traffic increases, multiple FastAPI instances can be
deployed behind a load balancer.

The architecture is intentionally designed so that the frontend and
backend can scale independently.

### Future Evolution

If individual modules eventually require independent scaling,
deployment, or ownership, selected modules could potentially be extracted
into separate services.

Microservices will not be introduced unless there is a clear technical or
organizational requirement for them.

## 16. Security Considerations

Security is a core architectural concern because the application manages
operational and administrative information.

### Authentication

The application will require authentication for protected functionality.

The MVP will use JWT-based authentication.

Future versions may integrate with enterprise SSO through an Identity
Provider.

### Authorization

Authorization will be enforced at the backend.

The application will use Role-Based Access Control (RBAC) with permissions
assigned to roles.

Where required, data-level authorization will restrict users to resources
they are permitted to access.

### Password Security

Passwords will never be stored in plain text.

A secure password hashing algorithm will be used.

### API Security

The API will implement:

- Request validation
- Authentication
- Authorization
- Appropriate HTTP methods
- Consistent error responses
- Rate limiting where required
- Secure CORS configuration

### Secrets Management

Sensitive configuration such as:

- Database credentials
- JWT signing secrets
- API keys
- External service credentials

will not be committed to source control.

Environment variables or a secure secrets-management mechanism will be
used.

### Data Protection

The application should avoid exposing sensitive operational information
through:

- API responses
- Error messages
- Logs
- Client-side code

### Auditability

Important administrative and operational changes will be recorded through
audit logging.

### Dependency Security

Application dependencies should be periodically reviewed for known
security vulnerabilities.## 17. Deployment Architecture

## 17. Deployment Architecture

The application will use a containerized deployment model.

The initial deployment architecture will consist of:

- Next.js frontend
- FastAPI backend
- PostgreSQL database

Future infrastructure may include:

- Redis
- Background workers
- Monitoring services
- External identity provider
- Notification services

### Deployment Flow

Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +---- Lint
    |
    +---- Test
    |
    +---- Build
    |
    +---- Docker Image
    |
    v
Deployment Environment
    |
    +---- Next.js
    |
    +---- FastAPI
    |
    +---- PostgreSQL


---

## 18. Technology Stack

### Frontend

**Next.js**

Used for the web application and user interface.

**TypeScript**

Used to provide static typing and improve maintainability.

**Tailwind CSS**

Used for application styling.

**shadcn/ui**

Used for reusable UI components.

---

### Backend

**Python**

Primary backend programming language.

**FastAPI**

Used to build REST APIs and backend application services.

**SQLAlchemy**

Used as the ORM/database abstraction layer.

**Alembic**

Used for database schema migrations.

---

### Database

**PostgreSQL**

Used as the primary relational database.

PostgreSQL was selected because the system contains strongly related
entities such as users, roles, branches, devices, and incidents and
requires transactions, constraints, indexing, and relational querying.

---

### Caching

**Redis**

Planned as an optional caching and background-job infrastructure
component.

It will only be introduced when justified by application requirements.

---

### Background Processing

**Celery**

Potentially used for long-running background operations such as bulk
processing, report generation, and notifications.

This is not required for the initial MVP.

---

### Testing

**Pytest**

Used for backend unit and integration testing.

**Playwright**

Used for end-to-end testing of important user workflows.

---

### Infrastructure

**Docker**

Used for containerization and reproducible environments.

**Docker Compose**

Used for local multi-container development.

---

### CI/CD

**GitHub Actions**

Used for automated linting, testing, building, and deployment workflows.

---

### API Documentation

**OpenAPI**

Used to define and document backend API contracts.

FastAPI will provide automatic OpenAPI documentation.

## 19. Architectural Trade-offs

The architecture intentionally prioritizes simplicity, maintainability,
and clear separation of responsibilities over unnecessary infrastructure
complexity.

### Modular Monolith vs Microservices

A modular monolith was selected for the initial implementation.

Advantages:

- Simpler development
- Simpler deployment
- Easier debugging
- Easier local development
- Lower infrastructure overhead
- Straightforward transactions

Microservices may provide benefits when independent scaling, deployment,
or team ownership becomes necessary.

For the current application, those benefits do not justify the additional
distributed-system complexity.

---

### PostgreSQL vs MongoDB

PostgreSQL was selected as the primary database.

The domain contains highly related entities:

Users
  |
Roles
  |
Branches
  |
Devices
  |
Incidents