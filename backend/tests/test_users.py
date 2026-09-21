from app.models.user import User

def test_create_user(client):
    payload = {
        "username": "testadmin",
        "email": "testadmin@example.com",
        "password": "StrongPassword123!",
        "role": "admin",
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testadmin"
    assert data["email"] == "testadmin@example.com"
    assert data["role"] == "admin"

    assert "password" not in data
    assert "password_hash" not in data
    
def test_create_user_password_is_hashed(client, db_session):
    payload = {
        "username": "hash_test",
        "email": "hash_test@example.com",
        "password": "StrongPassword123!",
        "role": "admin",
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 201

    user = db_session.query(User).filter(
        User.username == "hash_test"
    ).first()

    assert user is not None
    assert user.password_hash != "StrongPassword123!"
    assert user.password_hash.startswith("$argon2")
    

def test_create_duplicate_user(client):
    payload = {
        "username": "duplicate_user",
        "email": "duplicate@example.com",
        "password": "StrongPassword123!",
        "role": "admin",
    }

    first_response = client.post("/api/v1/users/", json=payload)

    assert first_response.status_code == 201

    second_response = client.post("/api/v1/users/", json=payload)

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Username or email already exists"
    

def test_user_login(client):
    create_payload = {
        "username": "login_test",
        "email": "login@example.com",
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
            "username": "login_test",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0
    

def test_user_login_with_invalid_password(client):
    create_payload = {
        "username": "invalid_login",
        "email": "invalid_login@example.com",
        "password": "CorrectPassword123!",
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
            "username": "invalid_login",
            "password": "WrongPassword123!",
        },
    )

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid username or password"
    

def test_get_current_user(client):
    create_payload = {
        "username": "me_test",
        "email": "me_test@example.com",
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
            "username": "me_test",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    me_response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert me_response.status_code == 200

    data = me_response.json()

    assert data["username"] == "me_test"
    assert data["email"] == "me_test@example.com"
    assert data["role"] == "manager"
    
def test_get_current_user_without_token(client):
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401
    

def test_get_current_user_with_invalid_token(client):
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"