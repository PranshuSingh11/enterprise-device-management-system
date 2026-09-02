# Database Design

## 1. Database Overview

The Enterprise Device Management System will use a relational database to
store and manage application data.

The database will serve as the primary source of truth for:

- Users and access control
- Business domains
- Branches
- Devices
- Incidents
- Audit records

The data model contains multiple relationships between these entities.

For example:


Business Domain
      |
      | 1:N
      v
    Branch
      |
      | 1:N
      v
    Device
      |
      | 1:N
      v
   Incident


The database will enforce data integrity through primary keys, foreign
keys, unique constraints, appropriate indexes, and transactional
operations.

The application will access the database through the FastAPI backend.
The frontend will never directly communicate with the database.

### Database Flow


Next.js
   |
   | REST API
   v
FastAPI
   |
   | SQLAlchemy
   v
PostgreSQL


PostgreSQL will be treated as the authoritative source of persistent
business data. Other infrastructure components such as Redis, if
introduced later, will not replace PostgreSQL as the system of record.


## 2. Database Selection

### Selected Database

**PostgreSQL**

PostgreSQL will be used as the primary relational database for the
Enterprise Device Management System.

### Why PostgreSQL?

The application's data has strong relationships between entities such as:


Users
  |
Roles
  |
Permissions

Business Domains
  |
Branches
  |
Devices
  |
Incidents


These relationships make a relational database a natural fit for the
system.

PostgreSQL provides capabilities that are important for EDMS, including:

- Strong relational data modeling
- Foreign key constraints
- Transactions
- Unique constraints
- Indexing
- Complex queries
- Aggregations
- Referential integrity
- Mature tooling and ecosystem

The application will require queries such as:

- Find all devices belonging to a branch.
- Find all offline devices within a business domain.
- Find all incidents for a device.
- Find all incidents associated with a branch.
- Calculate device statistics for the dashboard.
- Calculate incident statistics.
- Generate reports across branches and business domains.

These operations benefit from PostgreSQL's relational query capabilities.

### Why Not MongoDB?

MongoDB is a capable document database and could be used for this type of
application. However, it is not the preferred choice for the initial
implementation.

The EDMS domain contains many structured relationships and requires strong
data integrity between related entities.

For example:


Business Domain
      |
    Branch
      |
    Device
      |
   Incident


Maintaining these relationships, enforcing constraints, and executing
transactional operations are central requirements of the system.

MongoDB's flexible document model is therefore not a strong enough reason
to choose it over PostgreSQL for this particular application.

### Database as the System of Record

PostgreSQL will be the authoritative source of persistent business data.

Other infrastructure components may be introduced for specific purposes:

- Redis for caching
- Background workers for asynchronous processing
- Object storage for files, if required in the future

These components will not replace PostgreSQL as the primary system of
record.

### ORM

The application will use **SQLAlchemy** as the database access layer.

SQLAlchemy will provide:

- Database connection management
- ORM capabilities
- Query construction
- Transaction management
- Integration with PostgreSQL

Database schema changes will be managed using **Alembic** migrations.


## 3. Entity Identification

The database entities are divided into three categories:

1. Identity and access entities
2. Core business entities
3. Supporting and operational entities

### 3.1 Identity and Access Entities

#### User

Represents an individual who can access the EDMS application.

#### Role

Represents a logical collection of permissions assigned to users.

Initial roles include:

- Administrator
- Operations Manager
- Support Engineer
- Branch User
- Read-Only User

#### Permission

Represents an individual authorization capability.

Examples:

- device:read
- device:create
- device:update
- device:delete
- branch:read
- incident:read
- user:manage

#### User Role

Associates users with roles.

This is a junction entity supporting a many-to-many relationship between
users and roles.

#### Role Permission

Associates roles with permissions.

This is a junction entity supporting a many-to-many relationship between
roles and permissions.


### 3.2 Core Business Entities

#### Business Domain

Represents a logical business area within the organization.

Examples:

- Retail Banking
- Corporate Banking
- Operations
- Payments

A business domain can contain multiple branches.

#### Branch

Represents a physical or operational branch location.

A branch belongs to a business domain and can contain multiple devices.

A branch will have an operational status such as Open or Closed.

#### Device

Represents an enterprise device managed by the platform.

The initial implementation will primarily represent scanners, while the
model will allow additional device types in the future.

A device belongs to a branch and has an associated device type.

#### Device Type

Represents the category of a device.

Examples:

- Scanner
- Printer
- Kiosk
- Barcode Reader

Multiple devices can belong to the same device type.


### 3.3 Supporting Entities

#### Incident

Represents an operational issue associated with a device and/or branch.

Incident management is intentionally lightweight in the initial
application. Incidents primarily provide operational context for devices
and branches rather than implementing a complete ITSM workflow.

The initial incident data will include:

- Incident ID
- Title
- Description
- Status
- Priority
- Associated Device
- Associated Branch
- Created At
- Resolved At

#### Audit Log

Represents an immutable record of important actions performed within the
application.

Examples include:

- Device updated
- Branch modified
- User role changed
- Incident status changed

Audit logs are maintained separately from normal business entities so
that important application actions can be tracked independently.


## 4. Entity Relationships

The primary relationships in the database are:

| Relationship | Cardinality | Description |
|---|---|---|
| Business Domain → Branch | 1:N | A business domain can contain multiple branches. |
| Branch → Device | 1:N | A branch can contain multiple devices. |
| Device Type → Device | 1:N | A device type can be associated with multiple devices. |
| Device → Incident | 1:N | A device can have multiple incidents over its lifecycle. |
| Branch → Incident | 1:N | A branch can have multiple incidents. |
| User ↔ Role | N:N | A user can have multiple roles and a role can belong to multiple users. |
| Role ↔ Permission | N:N | A role can have multiple permissions and a permission can belong to multiple roles. |
| User → Audit Log | 1:N | A user can generate multiple audit log entries. |

Many-to-many relationships will be implemented using dedicated junction
tables rather than storing multiple related IDs in a single column.


## 5. Entity Definitions

### 5.1 User

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| name | VARCHAR | Yes | User's display name |
| email | VARCHAR | Yes | Unique login email |
| password_hash | VARCHAR | Yes | Hashed password |
| status | ENUM | Yes | ACTIVE / INACTIVE |
| created_at | TIMESTAMP | Yes | Creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

The application will never store plain-text passwords.


### 5.2 Role

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| name | VARCHAR | Yes | Role name |
| description | TEXT | No | Role description |
| created_at | TIMESTAMP | Yes | Creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

Role names must be unique.


### 5.3 Permission

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| name | VARCHAR | Yes | Permission identifier |
| description | TEXT | No | Permission description |
| created_at | TIMESTAMP | Yes | Creation timestamp |

Permission names must be unique.


### 5.4 User Role

| Field | Type | Required | Description |
|---|---|---|---|
| user_id | UUID | Yes | Foreign key to User |
| role_id | UUID | Yes | Foreign key to Role |
| assigned_at | TIMESTAMP | Yes | Assignment timestamp |

The combination of user_id and role_id must be unique.


### 5.5 Role Permission

| Field | Type | Required | Description |
|---|---|---|---|
| role_id | UUID | Yes | Foreign key to Role |
| permission_id | UUID | Yes | Foreign key to Permission |
| assigned_at | TIMESTAMP | Yes | Assignment timestamp |

The combination of role_id and permission_id must be unique.


### 5.6 Business Domain

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| name | VARCHAR | Yes | Domain name |
| description | TEXT | No | Domain description |
| status | ENUM | Yes | ACTIVE / INACTIVE |
| created_at | TIMESTAMP | Yes | Creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

Domain names must be unique.


### 5.7 Branch

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| branch_code | VARCHAR | Yes | Unique branch identifier |
| name | VARCHAR | Yes | Branch name |
| business_domain_id | UUID | Yes | Foreign key to Business Domain |
| address | TEXT | No | Branch address |
| city | VARCHAR | No | Branch city |
| status | ENUM | Yes | OPEN / CLOSED |
| created_at | TIMESTAMP | Yes | Creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

Branch codes must be unique.


### 5.8 Device Type

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| name | VARCHAR | Yes | Device type |
| description | TEXT | No | Device type description |
| created_at | TIMESTAMP | Yes | Creation timestamp |

Device type names must be unique.


### 5.9 Device

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| device_identifier | VARCHAR | Yes | Unique internal device identifier |
| serial_number | VARCHAR | Yes | Device serial number |
| device_type_id | UUID | Yes | Foreign key to Device Type |
| branch_id | UUID | Yes | Foreign key to Branch |
| manufacturer | VARCHAR | No | Device manufacturer |
| model | VARCHAR | No | Device model |
| ip_address | INET | No | Device IP address |
| status | ENUM | Yes | ONLINE / OFFLINE / MAINTENANCE / DECOMMISSIONED |
| firmware_version | VARCHAR | No | Current firmware version |
| certificate_status | ENUM | No | VALID / EXPIRING / EXPIRED |
| last_seen_at | TIMESTAMP | No | Last known connectivity time |
| installed_at | TIMESTAMP | No | Installation timestamp |
| created_at | TIMESTAMP | Yes | Creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

Device identifiers and serial numbers must be unique.


### 5.10 Incident

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| incident_number | VARCHAR | Yes | Human-readable incident identifier |
| title | VARCHAR | Yes | Incident title |
| description | TEXT | No | Incident details |
| status | ENUM | Yes | OPEN / IN_PROGRESS / RESOLVED / CLOSED |
| priority | ENUM | Yes | LOW / MEDIUM / HIGH / CRITICAL |
| device_id | UUID | No | Foreign key to Device |
| branch_id | UUID | Yes | Foreign key to Branch |
| created_at | TIMESTAMP | Yes | Creation timestamp |
| resolved_at | TIMESTAMP | No | Resolution timestamp |

Incident management is intentionally lightweight.


### 5.11 Audit Log

| Field | Type | Required | Description |
|---|---|---|---|
| id | UUID | Yes | Primary key |
| user_id | UUID | No | Foreign key to User |
| action | VARCHAR | Yes | Action performed |
| entity_type | VARCHAR | Yes | Entity affected |
| entity_id | UUID | No | ID of affected entity |
| old_value | JSONB | No | Previous state |
| new_value | JSONB | No | New state |
| request_id | VARCHAR | No | Request correlation ID |
| created_at | TIMESTAMP | Yes | Event timestamp |

Audit logs should be treated as append-only records.


## 6. Entity Relationship Diagram

The conceptual relationship model is:


                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                               N:N
                                │
                         ┌──────▼───────┐
                         │     Role     │
                         └──────┬───────┘
                                │
                               N:N
                                │
                         ┌──────▼────────┐
                         │  Permission   │
                         └───────────────┘


┌──────────────────┐
│ Business Domain  │
└────────┬─────────┘
         │ 1:N
         ▼
┌──────────────────┐
│     Branch       │
└────────┬─────────┘
         │
         │ 1:N
         ▼
┌──────────────────┐
│     Device       │
└────────┬─────────┘
         │
         │ N:1
         ▼
┌──────────────────┐
│   Device Type    │
└──────────────────┘

Device 1 ───────── N Incident
Branch  1 ───────── N Incident

User 1 ─────────── N Audit Log


### Simplified Relationship View


Business Domain 1 ─── N Branch
Branch          1 ─── N Device
Device Type     1 ─── N Device
Device          1 ─── N Incident
Branch          1 ─── N Incident

User            N ─── N Role
Role            N ─── N Permission

User            1 ─── N Audit Log



## 7. Primary Keys

All primary entities will use UUID-based primary keys.

The following entities will use a UUID as their primary key:

- User
- Role
- Permission
- Business Domain
- Branch
- Device Type
- Device
- Incident
- Audit Log

The junction tables will use composite primary keys:


user_roles
    (user_id, role_id)

role_permissions
    (role_id, permission_id)


UUIDs provide globally unique identifiers and avoid exposing sequential
database IDs through public APIs.

Human-readable identifiers such as branch_code, device_identifier, and
incident_number will be maintained separately where required.


## 8. Foreign Keys

Foreign keys will enforce relationships between related entities.

### User Role


user_roles.user_id
        ↓
users.id

user_roles.role_id
        ↓
roles.id


### Role Permission


role_permissions.role_id
        ↓
roles.id

role_permissions.permission_id
        ↓
permissions.id


### Branch


branches.business_domain_id
        ↓
business_domains.id


### Device


devices.branch_id
        ↓
branches.id

devices.device_type_id
        ↓
device_types.id


### Incident


incidents.device_id
        ↓
devices.id

incidents.branch_id
        ↓
branches.id


### Audit Log


audit_logs.user_id
        ↓
users.id


Foreign key constraints will be used to prevent invalid references and
maintain referential integrity.


## 9. Constraints

The database will use constraints to protect data integrity.

### Primary Key Constraints

Every entity will have a primary key.

### Unique Constraints

Unique constraints will be applied to values that must not be duplicated.

Examples:


users.email
roles.name
permissions.name
business_domains.name
branches.branch_code
device_types.name
devices.device_identifier
devices.serial_number
incidents.incident_number


### Foreign Key Constraints

Foreign keys will ensure that relationships point to valid records.

### Not Null Constraints

Mandatory business fields will use NOT NULL constraints.

For example:


Device:
    device_identifier
    serial_number
    branch_id
    device_type_id
    status


### Check Constraints

Where appropriate, database-level constraints may be used to prevent
invalid values.

For example, an incident priority should only contain supported values.

Application-level validation will still be used for user-friendly request
validation.


## 10. Indexing Strategy

Indexes will be created based on common query patterns rather than
indexing every column.

### Primary Key Indexes

Primary keys automatically provide indexes.

### Unique Indexes

Unique fields such as email, branch code, and device identifier will have
unique indexes.

### Foreign Key / Filtering Indexes

Indexes will be considered for frequently queried fields such as:


devices.branch_id
devices.device_type_id
devices.status
devices.last_seen_at

branches.business_domain_id
branches.status

incidents.device_id
incidents.branch_id
incidents.status
incidents.priority

audit_logs.user_id
audit_logs.entity_type
audit_logs.entity_id
audit_logs.created_at


### Search

If device searches frequently use fields such as serial number or device
identifier, appropriate indexes will be used.

More advanced search strategies will only be introduced if required by
actual query performance.

### Indexing Principle

Indexes improve read performance but increase storage requirements and can
increase the cost of writes.

Indexes will therefore be introduced based on actual access patterns and
query analysis.


## 11. Transaction Strategy

Transactions will be used when multiple database operations must succeed
or fail together.

For example, updating a device and recording the corresponding audit event
may require transactional handling:


BEGIN TRANSACTION

Update Device
       |
       v
Create Audit Log

       |
       v

COMMIT


If either operation fails:


ROLLBACK


This prevents the database from reaching an inconsistent state.

Simple read-only queries do not require explicit application-level
transactions beyond the normal database transaction handling.

Transaction boundaries will primarily be managed in the service layer,
while the repository layer will handle database operations.


## 12. Data Lifecycle

The system will maintain timestamps for important entities.

Common lifecycle fields include:


created_at
updated_at


Some entities will also contain domain-specific lifecycle fields.

For example:


Device:
    installed_at
    last_seen_at

Incident:
    created_at
    resolved_at


### Soft Delete

Business-critical records will generally not be physically deleted unless
there is a clear requirement to do so.

For example, devices may move to:


DECOMMISSIONED


rather than being permanently deleted.

This preserves historical relationships and operational information.

Users may similarly be marked:


INACTIVE


instead of being physically deleted.

### Audit Data

Audit logs will be treated as append-only records.

Existing audit records should not normally be modified or deleted through
standard application operations.

### Data Retention

The initial implementation will not define a complex automated data
retention policy.

Retention periods can be introduced later based on actual business,
security, or compliance requirements.


## 13. Database Design Summary

The EDMS database uses PostgreSQL as its system of record and follows a
relational data model.

The primary relationships are:


Business Domain
      |
    Branch
      |
    Device
      |
   Incident


while access control is modeled as:


User
  |
User Role
  |
Role
  |
Role Permission
  |
Permission


The design uses:

- UUID primary keys
- Foreign keys
- Unique constraints
- NOT NULL constraints
- Appropriate indexes
- Transactions
- Append-only audit records
- Soft deactivation/decommissioning where appropriate

The model is intentionally designed around the application's core
requirements without introducing unnecessary database complexity.
