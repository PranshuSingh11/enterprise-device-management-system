def test_create_scanner(client):
    user_payload = {
        "username": "scanner_creator",
        "email": "scanner_creator@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    user_response = client.post(
        "/api/v1/users/",
        json=user_payload
    )

    assert user_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "scanner_creator",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    branch_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Scanner Test Branch",
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
            "name": "Test Scanner",
            "serial_number": "SCANNER-TEST-001",
            "model": "Fujitsu fi-8170",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    assert scanner_response.status_code == 201

    data = scanner_response.json()

    assert data["id"] is not None
    assert data["name"] == "Test Scanner"
    assert data["serial_number"] == "SCANNER-TEST-001"
    assert data["model"] == "Fujitsu fi-8170"
    assert data["status"] == "active"
    assert data["branch_id"] == branch_id


def test_create_scanner_with_invalid_branch(client):
    user_payload = {
        "username": "invalid_branch_user",
        "email": "invalid_branch@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    user_response = client.post(
        "/api/v1/users/",
        json=user_payload
    )

    assert user_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "invalid_branch_user",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/scanners/",
        json={
            "name": "Invalid Branch Scanner",
            "serial_number": "SCANNER-INVALID-BRANCH-001",
            "model": "Test Model",
            "status": "active",
            "branch_id": 99999,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"


def test_list_scanners(client):
    user_payload = {
        "username": "scanner_list_user",
        "email": "scanner_list@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "scanner_list_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    branch_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "List Scanner Branch",
            "location": "Test Location",
            "status": "open",
        },
        headers=headers,
    )

    branch_id = branch_response.json()["id"]

    client.post(
        "/api/v1/scanners/",
        json={
            "name": "Scanner One",
            "serial_number": "LIST-001",
            "model": "Model A",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    client.post(
        "/api/v1/scanners/",
        json={
            "name": "Scanner Two",
            "serial_number": "LIST-002",
            "model": "Model B",
            "status": "inactive",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/scanners/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data

    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_scanners_with_search(client):
    user_payload = {
        "username": "scanner_search_user",
        "email": "scanner_search@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "scanner_search_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    branch_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Search Branch",
            "location": "Test Location",
            "status": "open",
        },
        headers=headers,
    )

    branch_id = branch_response.json()["id"]

    client.post(
        "/api/v1/scanners/",
        json={
            "name": "Production Scanner",
            "serial_number": "SEARCH-001",
            "model": "Model A",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    client.post(
        "/api/v1/scanners/",
        json={
            "name": "Backup Scanner",
            "serial_number": "SEARCH-002",
            "model": "Model B",
            "status": "inactive",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/scanners/?search=Production",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["name"] == "Production Scanner"


def test_list_scanners_with_status_filter(client):
    user_payload = {
        "username": "scanner_filter_user",
        "email": "scanner_filter@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "scanner_filter_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    branch_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Filter Branch",
            "location": "Test Location",
            "status": "open",
        },
        headers=headers,
    )

    branch_id = branch_response.json()["id"]

    client.post(
        "/api/v1/scanners/",
        json={
            "name": "Active Scanner",
            "serial_number": "FILTER-001",
            "model": "Model A",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    client.post(
        "/api/v1/scanners/",
        json={
            "name": "Inactive Scanner",
            "serial_number": "FILTER-002",
            "model": "Model B",
            "status": "inactive",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/scanners/?status=active",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["status"] == "active"


def test_get_scanner_by_id(client):
    user_payload = {
        "username": "scanner_get_user",
        "email": "scanner_get@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "scanner_get_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    branch_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Get Scanner Branch",
            "location": "Test Location",
            "status": "open",
        },
        headers=headers,
    )

    branch_id = branch_response.json()["id"]

    create_response = client.post(
        "/api/v1/scanners/",
        json={
            "name": "Specific Scanner",
            "serial_number": "GET-001",
            "model": "Model A",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    scanner_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/scanners/{scanner_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == scanner_id
    assert data["name"] == "Specific Scanner"


def test_get_nonexistent_scanner(client):
    user_payload = {
        "username": "scanner_notfound_user",
        "email": "scanner_notfound@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "scanner_notfound_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/scanners/99999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Scanner not found"


def test_update_scanner(client):
    user_payload = {
        "username": "scanner_update_user",
        "email": "scanner_update@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "scanner_update_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    branch_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Update Scanner Branch",
            "location": "Test Location",
            "status": "open",
        },
        headers=headers,
    )

    branch_id = branch_response.json()["id"]

    create_response = client.post(
        "/api/v1/scanners/",
        json={
            "name": "Original Scanner",
            "serial_number": "UPDATE-001",
            "model": "Model A",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    scanner_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/v1/scanners/{scanner_id}",
        json={
            "name": "Updated Scanner",
            "serial_number": "UPDATE-001",
            "model": "Model B",
            "status": "inactive",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == scanner_id
    assert data["name"] == "Updated Scanner"
    assert data["model"] == "Model B"
    assert data["status"] == "inactive"


def test_update_nonexistent_scanner(client):
    user_payload = {
        "username": "scanner_update_notfound",
        "email": "scanner_update_notfound@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "scanner_update_notfound",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    response = client.put(
        "/api/v1/scanners/99999",
        json={
            "name": "Updated Scanner",
            "serial_number": "UPDATE-404",
            "model": "Model B",
            "status": "inactive",
            "branch_id": 1,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Scanner not found"