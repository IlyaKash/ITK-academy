import pytest

@pytest.mark.asyncio
async def test_create_wallet(client):
    """Тест создания кошелька"""
    response = await client.post("/api/v1/wallets")
    assert response.status_code == 201
    assert "uuid" in response.json()

@pytest.mark.asyncio
async def test_get_wallet(client):
    """Тест получения кошелька"""
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["uuid"]
    response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    assert "uuid" in response.json()

@pytest.mark.asyncio
async def test_update_wallet(client):
    """Тест обновления кошелька"""
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["uuid"]
    operation_data = {
        "operation_type": "DEPOSIT",
        "amount": "100.50"
    }
    response = await client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 200
    assert float(response.json()['balance']) == 100.50

@pytest.mark.asyncio
async def test_create_wallet_minimal_balance(client):
    """Тест создания кошелька с минимальным балансом"""
    response = await client.post("/api/v1/wallets")
    assert response.status_code == 201
    data = response.json()
    assert "uuid" in data
    assert float(data["balance"]) == 0.00

@pytest.mark.asyncio
async def test_get_nonexistent_wallet(client):
    """Тест получения несуществующего кошелька"""
    response = await client.get("/api/v1/wallets/non-existent-uuid")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_deposit_negative_amount(client):
    """Тест пополнения отрицательной суммой"""
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["uuid"]
    
    operation_data = {
        "operation_type": "DEPOSIT",
        "amount": "-100.50"
    }
    response = await client.post(f"/api/v1/wallets/{wallet_id}/operation", json=operation_data)
    assert response.status_code == 422 
