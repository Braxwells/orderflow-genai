def test_crear_pedido_ok(client, auth_headers):
    res = client.post("/api/pedidos/", json={
        "cliente": "María García",
        "articulo": "Chaqueta vaquera",
        "talla": "S",
        "precio": 45.00,
        "canal": "email"
    }, headers=auth_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["cliente"] == "María García"
    assert data["estado"] == "pendiente"
    assert data["fecha_creacion"] is not None


def test_crear_pedido_sin_cliente(client, auth_headers):
    res = client.post("/api/pedidos/", json={
        "articulo": "Camiseta",
        "talla": "M",
        "precio": 20.00,
        "canal": "whatsapp"
    }, headers=auth_headers)
    assert res.status_code == 422


def test_crear_pedido_sin_precio(client, auth_headers):
    res = client.post("/api/pedidos/", json={
        "cliente": "Juan",
        "articulo": "Pantalón",
        "talla": "L",
        "canal": "whatsapp"
    }, headers=auth_headers)
    assert res.status_code == 422


def test_listar_pedidos(client, auth_headers, pedido_base):
    res = client.get("/api/pedidos/", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_cambiar_estado_a_en_proceso(client, auth_headers, pedido_base):
    pedido_id = pedido_base["id"]
    res = client.patch(
        f"/api/pedidos/{pedido_id}/estado",
        json={"estado": "en_proceso"},
        headers=auth_headers
    )
    assert res.status_code == 200
    assert res.json()["estado"] == "en_proceso"


def test_cambiar_estado_a_enviado_archiva(client, auth_headers, pedido_base):
    pedido_id = pedido_base["id"]
    # Marcar como enviado
    res = client.patch(
        f"/api/pedidos/{pedido_id}/estado",
        json={"estado": "enviado"},
        headers=auth_headers
    )
    assert res.status_code == 200
    assert res.json()["fecha_envio"] is not None

    # Ya no debe aparecer en pedidos activos
    activos = client.get("/api/pedidos/", headers=auth_headers).json()
    ids_activos = [p["id"] for p in activos]
    assert pedido_id not in ids_activos

    # Sí debe aparecer en el histórico
    historico = client.get("/api/historico/", headers=auth_headers).json()
    ids_historico = [p["id"] for p in historico]
    assert pedido_id in ids_historico


def test_editar_pedido_activo(client, auth_headers, pedido_base):
    pedido_id = pedido_base["id"]
    res = client.put(
        f"/api/pedidos/{pedido_id}",
        json={"talla": "XL", "precio": 55.00},
        headers=auth_headers
    )
    assert res.status_code == 200
    assert res.json()["talla"] == "XL"
    assert res.json()["precio"] == 55.00


def test_editar_pedido_historico_prohibido(client, auth_headers, pedido_base):
    pedido_id = pedido_base["id"]
    # Enviamos el pedido al histórico
    client.patch(
        f"/api/pedidos/{pedido_id}/estado",
        json={"estado": "enviado"},
        headers=auth_headers
    )
    # Intentar editar debe dar 403
    res = client.put(
        f"/api/pedidos/{pedido_id}",
        json={"talla": "XS"},
        headers=auth_headers
    )
    assert res.status_code == 403


def test_pedido_no_encontrado(client, auth_headers):
    res = client.patch(
        "/api/pedidos/9999/estado",
        json={"estado": "enviado"},
        headers=auth_headers
    )
    assert res.status_code == 404