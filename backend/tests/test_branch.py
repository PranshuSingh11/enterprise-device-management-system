def test_create_branch(client):
    user_payload = {
        "username": "branch_creator",
        "email": "branch_creator@example.com",
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
            "username": "branch_creator",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Mumbai Branch",
            "location": "Mumbai",
            "status": "open",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["name"] == "Mumbai Branch"
    assert data["location"] == "Mumbai"
    assert data["status"] == "open"


def test_list_branches(client):
    user_payload = {
        "username": "branch_list_user",
        "email": "branch_list@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "branch_list_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/branches/",
        json={
            "name": "Branch One",
            "location": "Mumbai",
            "status": "open",
        },
        headers=headers,
    )

    client.post(
        "/api/v1/branches/",
        json={
            "name": "Branch Two",
            "location": "Pune",
            "status": "closed",
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/branches/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data


def test_list_branches_with_search(client):
    user_payload = {
        "username": "branch_search_user",
        "email": "branch_search@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "branch_search_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/branches/",
        json={
            "name": "Mumbai Central",
            "location": "Mumbai",
            "status": "open",
        },
        headers=headers,
    )

    client.post(
        "/api/v1/branches/",
        json={
            "name": "Pune Central",
            "location": "Pune",
            "status": "open",
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/branches/?search=Mumbai",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["name"] == "Mumbai Central"


def test_list_branches_with_status_filter(client):
    user_payload = {
        "username": "branch_filter_user",
        "email": "branch_filter@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "branch_filter_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/branches/",
        json={
            "name": "Open Branch",
            "location": "Mumbai",
            "status": "open",
        },
        headers=headers,
    )

    client.post(
        "/api/v1/branches/",
        json={
            "name": "Closed Branch",
            "location": "Pune",
            "status": "closed",
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/branches/?status=open",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["status"] == "open"


def test_get_branch_by_id(client):
    user_payload = {
        "username": "branch_get_user",
        "email": "branch_get@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "branch_get_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Specific Branch",
            "location": "Mumbai",
            "status": "open",
        },
        headers=headers,
    )

    branch_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/branches/{branch_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == branch_id
    assert data["name"] == "Specific Branch"


def test_get_nonexistent_branch(client):
    user_payload = {
        "username": "branch_notfound_user",
        "email": "branch_notfound@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "branch_notfound_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/branches/99999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"


def test_update_branch(client):
    user_payload = {
        "username": "branch_update_user",
        "email": "branch_update@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "branch_update_user",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/api/v1/branches/",
        json={
            "name": "Original Branch",
            "location": "Mumbai",
            "status": "open",
        },
        headers=headers,
    )

    branch_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/branches/{branch_id}",
        json={
            "name": "Updated Branch",
            "location": "Pune",
            "status": "closed",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == branch_id
    assert data["name"] == "Updated Branch"
    assert data["location"] == "Pune"
    assert data["status"] == "closed"


def test_update_nonexistent_branch(client):
    user_payload = {
        "username": "branch_update_notfound",
        "email": "branch_update_notfound@example.com",
        "password": "StrongPassword123!",
        "role": "manager",
    }

    client.post("/api/v1/users/", json=user_payload)

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "branch_update_notfound",
            "password": "StrongPassword123!",
        },
    )

    token = login_response.json()["access_token"]

    response = client.put(
        "/api/v1/branches/99999",
        json={
            "name": "Updated Branch",
            "location": "Pune",
            "status": "closed",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"