def test_historico_vacio_inicial(client, auth_headers):
    res = client.get("/api/historico/", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_historico_contiene_pedido_enviado(client, auth_headers, pedido_base):
    pedido_id = pedido_base["id"]
    client.patch(
        f"/api/pedidos/{pedido_id}/estado",
        json={"estado": "enviado"},
        headers=auth_headers
    )
    res = client.get("/api/historico/", headers=auth_headers)
    assert res.status_code == 200
    assert any(p["id"] == pedido_id for p in res.json())


def test_busqueda_historico_por_cliente(client, auth_headers, pedido_base):
    pedido_id = pedido_base["id"]
    client.patch(
        f"/api/pedidos/{pedido_id}/estado",
        json={"estado": "enviado"},
        headers=auth_headers
    )
    res = client.get("/api/historico/?q=Cliente", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_busqueda_historico_sin_resultados(client, auth_headers, pedido_base):
    pedido_id = pedido_base["id"]
    client.patch(
        f"/api/pedidos/{pedido_id}/estado",
        json={"estado": "enviado"},
        headers=auth_headers
    )
    res = client.get("/api/historico/?q=zzznoresult", headers=auth_headers)
    assert res.status_code == 200
    assert res.json() == []