def test_viewer_cannot_create_scanner(client):
    create_payload = {
        "username": "viewer_test",
        "email": "viewer_test@example.com",
        "password": "StrongPassword123!",
        "role": "viewer",
    }

    create_response = client.post(
        "/api/v1/users/",
        json=create_payload
    )

    assert create_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "viewer_test",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    scanner_payload = {
        "name": "Test Scanner",
        "serial_number": "TEST-RBAC-001",
        "model": "Test Model",
        "status": "active",
        "branch_id": 1,
    }

    response = client.post(
        "/api/v1/scanners/",
        json=scanner_payload,
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403
    
def test_manager_can_create_scanner(client):
    create_payload = {
        "username": "manager_test",
        "email": "manager_test@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    create_response = client.post(
        "/api/v1/users/",
        json=create_payload
    )

    assert create_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "manager_test",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Create a branch first because scanner.branch_id is required.
    branch_payload = {
        "name": "RBAC Test Branch",
        "location": "Test Location",
        "status": "open",
    }

    branch_response = client.post(
        "/api/v1/branches/",
        json=branch_payload,
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert branch_response.status_code == 201

    branch_id = branch_response.json()["id"]

    scanner_payload = {
        "name": "Manager Scanner",
        "serial_number": "RBAC-MANAGER-001",
        "model": "Test Model",
        "status": "active",
        "branch_id": branch_id,
    }

    response = client.post(
        "/api/v1/scanners/",
        json=scanner_payload,
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201
    assert response.json()["serial_number"] == "RBAC-MANAGER-001"
    

def test_manager_cannot_delete_scanner(client):
    create_payload = {
        "username": "delete_manager",
        "email": "delete_manager@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    create_response = client.post(
        "/api/v1/users/",
        json=create_payload
    )

    assert create_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "delete_manager",
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
            "name": "Delete Test Branch",
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
            "name": "Delete Test Scanner",
            "serial_number": "RBAC-DELETE-001",
            "model": "Test Model",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    assert scanner_response.status_code == 201

    scanner_id = scanner_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/scanners/{scanner_id}",
        headers=headers,
    )

    assert delete_response.status_code == 403
    
def test_admin_can_delete_scanner(client):
    create_payload = {
        "username": "delete_admin",
        "email": "delete_admin@example.com",
        "password": "StrongPassword123!",
        "role": "admin",
    }

    create_response = client.post(
        "/api/v1/users/",
        json=create_payload
    )

    assert create_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "delete_admin",
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
            "name": "Admin Delete Branch",
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
            "name": "Admin Delete Scanner",
            "serial_number": "RBAC-ADMIN-DELETE-001",
            "model": "Test Model",
            "status": "active",
            "branch_id": branch_id,
        },
        headers=headers,
    )

    assert scanner_response.status_code == 201

    scanner_id = scanner_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/scanners/{scanner_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204
    
def test_viewer_can_list_scanners(client):
    create_payload = {
        "username": "viewer_read",
        "email": "viewer_read@example.com",
        "password": "StrongPassword123!",
        "role": "viewer",
    }

    create_response = client.post(
        "/api/v1/users/",
        json=create_payload
    )

    assert create_response.status_code == 201

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "viewer_read",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/scanners/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data