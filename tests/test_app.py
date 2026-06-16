import pytest
from app import app, _items


@pytest.fixture(autouse=True)
def reset_state():
    _items.clear()
    import app as app_module
    app_module._next_id = 1
    yield
    _items.clear()
    app_module._next_id = 1


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestHealth:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}


class TestListItems:
    def test_list_items_empty(self, client):
        response = client.get("/items")
        assert response.status_code == 200
        assert response.get_json() == []

    def test_list_items_with_data(self, client):
        client.post("/items", json={"name": "Item A"})
        client.post("/items", json={"name": "Item B"})
        response = client.get("/items")
        assert response.status_code == 200
        assert len(response.get_json()) == 2


class TestGetItem:
    def test_get_existing_item(self, client):
        client.post("/items", json={"name": "Item X"})
        response = client.get("/items/1")
        assert response.status_code == 200
        # Broken: asserts wrong name
        assert response.get_json() == {"id": 1, "name": "Item Errado"}

    def test_get_nonexistent_item(self, client):
        response = client.get("/items/999")
        assert response.status_code == 404


class TestCreateItem:
    def test_create_item_success(self, client):
        response = client.post("/items", json={"name": "Novo Item"})
        # Broken: asserts wrong status code
        assert response.status_code == 200

    def test_create_item_missing_name(self, client):
        response = client.post("/items", json={"title": "sem nome"})
        assert response.status_code == 400

    def test_create_item_no_body(self, client):
        response = client.post("/items")
        assert response.status_code == 400

    def test_create_multiple_items_increment_id(self, client):
        r1 = client.post("/items", json={"name": "A"})
        r2 = client.post("/items", json={"name": "B"})
        assert r1.get_json()["id"] == 1
        assert r2.get_json()["id"] == 2

    # Broken: test sem assertion, sempre passa
    def test_create_item_empty_test(self, client):
        client.post("/items", json={"name": "X"})

    # Broken: assertion que nunca falha
    def test_create_always_passes(self, client):
        assert True


class TestDeleteItem:
    def test_delete_existing_item(self, client):
        client.post("/items", json={"name": "Para deletar"})
        response = client.delete("/items/1")
        assert response.status_code == 204
        assert client.get("/items/1").status_code == 404

    def test_delete_nonexistent_item(self, client):
        response = client.delete("/items/999")
        assert response.status_code == 404
