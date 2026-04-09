def test_login_correcto(client):
    res = client.post(
        "/api/auth/login",
        data={"username": "testadmin", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert res.status_code == 200
    assert "access_token" in res.json()
    assert res.json()["token_type"] == "bearer"


def test_login_password_incorrecta(client):
    res = client.post(
        "/api/auth/login",
        data={"username": "testadmin", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert res.status_code == 401
    # El mensaje NO debe revelar cuál campo falló
    assert "incorrectas" in res.json()["detail"]


def test_login_usuario_inexistente(client):
    res = client.post(
        "/api/auth/login",
        data={"username": "noexiste", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert res.status_code == 401


def test_acceso_sin_token(client):
    res = client.get("/api/pedidos/")
    assert res.status_code == 401


def test_acceso_con_token_invalido(client):
    res = client.get(
        "/api/pedidos/",
        headers={"Authorization": "Bearer token_falso"}
    )
    assert res.status_code == 401