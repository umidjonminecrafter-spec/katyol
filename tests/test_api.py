import pytest

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["app"] == "Kotyol ERP Backend"

@pytest.mark.asyncio
async def test_login_success_and_invalid(client):
    # Invalid login
    res_bad = await client.post("/api/v1/auth/login", json={"username": "admin@kotyol.uz", "password": "WrongPassword"})
    assert res_bad.status_code == 401
    assert res_bad.json()["success"] is False

    # Valid login
    res = await client.post("/api/v1/auth/login", json={"username": "admin@kotyol.uz", "password": "Password123!"})
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert body["data"]["user"]["username"] == "admin@kotyol.uz"

@pytest.mark.asyncio
async def test_products_and_safe_delete(client):
    # Login as admin
    login_res = await client.post("/api/v1/auth/login", json={"username": "admin@kotyol.uz", "password": "Password123!"})
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch Categories to get valid category_id and unit_id
    cat_res = await client.get("/api/v1/master-data/product-categories", headers=headers)
    cat_id = cat_res.json()["data"][0]["id"]

    unit_res = await client.get("/api/v1/master-data/units", headers=headers)
    unit_id = unit_res.json()["data"][0]["id"]

    # Create product
    prod_data = {
        "code": "PRD-101",
        "name": "Kotyol K-50kW",
        "category_id": cat_id,
        "unit_id": unit_id,
        "type": "FINISHED_GOOD",
        "min_stock_level": 5.0,
        "unit_price": 2500.00
    }
    prod_res = await client.post("/api/v1/products", json=prod_data, headers=headers)
    assert prod_res.status_code == 201
    prod_body = prod_res.json()
    assert prod_body["success"] is True
    assert prod_body["data"]["code"] == "PRD-101"

    # Attempt to delete the Category which is now referenced by PRD-101
    del_cat_res = await client.delete(f"/api/v1/master-data/product-categories/{cat_id}", headers=headers)
    assert del_cat_res.status_code == 400
    del_cat_body = del_cat_res.json()
    assert del_cat_body["success"] is False
    assert del_cat_body["error_code"] == "ENTITY_IN_USE"
    assert del_cat_body["details"]["reference_count"] == 1

@pytest.mark.asyncio
async def test_dashboard_summary(client):
    login_res = await client.post("/api/v1/auth/login", json={"username": "admin@kotyol.uz", "password": "Password123!"})
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    dash_res = await client.get("/api/v1/dashboard/summary", headers=headers)
    assert dash_res.status_code == 200
    dash_body = dash_res.json()
    assert dash_body["success"] is True
    assert "monthly_revenue" in dash_body["data"]
    assert "active_orders_count" in dash_body["data"]
