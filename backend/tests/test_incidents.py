def create_authenticated_manager(client, username="incident_user"):
    user_payload = {
        "username": username,
        "email": f"{username}@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    user_response = client.post(
        "/api/v1/users/",
        json=user_payload,
    )

    assert user_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": username,
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    return {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }


def create_test_scanner(client, headers, serial_number="INCIDENT-SCANNER-001"):
    branch_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Incident Test Branch",
            "location": "Test Location",
            "status": "open",
        },
        headers=headers,
    )

    assert branch_response.status_code == 201

    branch_id = branch_response.json()["id"]

    scanner_response = client.post(
        "/api/v1/scanners/",
        json={
            "name": "Incident Test Scanner",
            "serial_number": serial_number,
            "model": "Test Model",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    assert scanner_response.status_code == 201

    return scanner_response.json()["id"]


def test_create_incident(client):
    headers = create_authenticated_manager(client, "incident_create")

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-CREATE-001",
    )

    response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Scanner Offline",
            "description": "Scanner is not responding",
            "status": "open",
            "priority": "high",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Scanner Offline"
    assert data["description"] == "Scanner is not responding"
    assert data["status"] == "open"
    assert data["priority"] == "high"
    assert data["scanner_id"] == scanner_id
    assert data["created_at"] is not None
    assert data["resolved_at"] is None


def test_create_incident_with_invalid_scanner(client):
    headers = create_authenticated_manager(
        client,
        "incident_invalid_scanner",
    )

    response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Invalid Scanner Incident",
            "description": "Scanner does not exist",
            "status": "open",
            "priority": "medium",
            "scanner_id": 99999,
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Scanner not found"


def test_create_incident_with_invalid_status(client):
    headers = create_authenticated_manager(
        client,
        "incident_invalid_status",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-STATUS-001",
    )

    response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Invalid Status Incident",
            "description": "Testing invalid status",
            "status": "invalid_status",
            "priority": "medium",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid incident status: invalid_status"


def test_create_incident_with_invalid_priority(client):
    headers = create_authenticated_manager(
        client,
        "incident_invalid_priority",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-PRIORITY-001",
    )

    response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Invalid Priority Incident",
            "description": "Testing invalid priority",
            "status": "open",
            "priority": "invalid_priority",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid incident priority: invalid_priority"


def test_list_incidents(client):
    headers = create_authenticated_manager(
        client,
        "incident_list",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-LIST-001",
    )

    for number in range(1, 3):
        response = client.post(
            "/api/v1/incidents/",
            json={
                "title": f"Incident {number}",
                "description": f"Description {number}",
                "status": "open",
                "priority": "medium",
                "scanner_id": scanner_id,
            },
            headers=headers,
        )

        assert response.status_code == 201

    response = client.get(
        "/api/v1/incidents/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data


def test_list_incidents_with_search(client):
    headers = create_authenticated_manager(
        client,
        "incident_search",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-SEARCH-001",
    )

    client.post(
        "/api/v1/incidents/",
        json={
            "title": "Network Connectivity Failure",
            "description": "Scanner lost network connection",
            "status": "open",
            "priority": "high",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    client.post(
        "/api/v1/incidents/",
        json={
            "title": "Paper Jam",
            "description": "Paper is stuck in scanner",
            "status": "open",
            "priority": "low",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/incidents/?search=Network",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["title"] == "Network Connectivity Failure"


def test_list_incidents_with_status_filter(client):
    headers = create_authenticated_manager(
        client,
        "incident_status_filter",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-FILTER-STATUS-001",
    )

    client.post(
        "/api/v1/incidents/",
        json={
            "title": "Open Incident",
            "description": "Open issue",
            "status": "open",
            "priority": "medium",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    client.post(
        "/api/v1/incidents/",
        json={
            "title": "Resolved Incident",
            "description": "Resolved issue",
            "status": "resolved",
            "priority": "medium",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/incidents/?status=resolved",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["status"] == "resolved"


def test_list_incidents_with_priority_filter(client):
    headers = create_authenticated_manager(
        client,
        "incident_priority_filter",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-FILTER-PRIORITY-001",
    )

    client.post(
        "/api/v1/incidents/",
        json={
            "title": "Critical Incident",
            "description": "Critical issue",
            "status": "open",
            "priority": "critical",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    client.post(
        "/api/v1/incidents/",
        json={
            "title": "Low Incident",
            "description": "Low priority issue",
            "status": "open",
            "priority": "low",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/incidents/?priority=critical",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["priority"] == "critical"


def test_get_incident_by_id(client):
    headers = create_authenticated_manager(
        client,
        "incident_get",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-GET-001",
    )

    create_response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Specific Incident",
            "description": "Specific incident description",
            "status": "open",
            "priority": "medium",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    incident_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/incidents/{incident_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == incident_id
    assert data["title"] == "Specific Incident"


def test_get_nonexistent_incident(client):
    headers = create_authenticated_manager(
        client,
        "incident_notfound",
    )

    response = client.get(
        "/api/v1/incidents/99999",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"


def test_update_incident(client):
    headers = create_authenticated_manager(
        client,
        "incident_update",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-UPDATE-001",
    )

    create_response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Original Incident",
            "description": "Original description",
            "status": "open",
            "priority": "medium",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    incident_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/incidents/{incident_id}",
        json={
            "title": "Updated Incident",
            "description": "Updated description",
            "status": "in_progress",
            "priority": "high",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == incident_id
    assert data["title"] == "Updated Incident"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"
    assert data["resolved_at"] is None


def test_resolve_incident_sets_resolved_at(client):
    headers = create_authenticated_manager(
        client,
        "incident_resolve",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-RESOLVE-001",
    )

    create_response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Resolvable Incident",
            "description": "Incident to resolve",
            "status": "open",
            "priority": "high",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    incident_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/incidents/{incident_id}",
        json={
            "title": "Resolvable Incident",
            "description": "Incident resolved",
            "status": "resolved",
            "priority": "high",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "resolved"
    assert data["resolved_at"] is not None


def test_closed_incident_cannot_be_reopened(client):
    headers = create_authenticated_manager(
        client,
        "incident_closed",
    )

    scanner_id = create_test_scanner(
        client,
        headers,
        "INCIDENT-CLOSED-001",
    )

    create_response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Closed Incident",
            "description": "Incident that will be closed",
            "status": "closed",
            "priority": "high",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    incident_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/incidents/{incident_id}",
        json={
            "title": "Reopened Incident",
            "description": "Attempting to reopen",
            "status": "open",
            "priority": "high",
            "scanner_id": scanner_id,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Closed incidents cannot be reopened"