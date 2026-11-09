from fastapi.testclient import TestClient


def order(client: TestClient, drop_id: int):
    return client.post(f"/drops/{drop_id}/orders")


def test_an_order_decrements_the_stock(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=3)

    response = order(client, drop["id"])

    assert response.status_code == 201
    created = response.json()
    assert created["drop_id"] == drop["id"]
    assert created["drop"]["remaining"] == 2
    assert created["drop"]["status"] == "live"
    assert client.get(f"/drops/{drop['id']}").json()["remaining"] == 2


def test_the_last_pair_makes_the_drop_sold_out(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=1)

    response = order(client, drop["id"])

    assert response.status_code == 201
    assert response.json()["drop"]["remaining"] == 0
    assert response.json()["drop"]["status"] == "sold_out"
    assert client.get(f"/drops/{drop['id']}").json()["status"] == "sold_out"


def test_ordering_a_sold_out_drop_is_refused(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=1)
    order(client, drop["id"])

    response = order(client, drop["id"])

    assert response.status_code == 409
    assert response.json()["detail"] == f"Le drop {drop['id']} est épuisé"
    assert client.get(f"/drops/{drop['id']}").json()["remaining"] == 0


def test_the_last_pair_is_never_sold_twice(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=2)

    statuses = [order(client, drop["id"]).status_code for _ in range(4)]

    assert statuses == [201, 201, 409, 409]
    assert client.get(f"/drops/{drop['id']}").json()["remaining"] == 0


def test_ordering_a_drop_not_open_yet_is_refused(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=5, opens_at="2100-01-01T00:00:00Z")

    response = order(client, drop["id"])

    assert response.status_code == 409
    assert response.json()["detail"] == f"Le drop {drop['id']} n'est pas encore ouvert"
    assert client.get(f"/drops/{drop['id']}").json()["remaining"] == 5


def test_ordering_an_unknown_drop_is_refused(client: TestClient) -> None:
    response = order(client, 999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Drop 999 introuvable"
