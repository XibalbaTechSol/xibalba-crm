from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, get_db
from app.models.user import User
from app.models.standard_entities import Account
from sqlalchemy.orm import sessionmaker
import pytest

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # User
    if not db.query(User).filter(User.user_name == 'admin').first():
        user = User(id='1', user_name='admin', first_name='Admin', is_admin=True)
        db.add(user)

    # Account
    if not db.query(Account).filter(Account.name == 'Test Account').first():
        account = Account(id='test_acc_1', name='Test Account')
        db.add(account)

    db.commit()
    db.close()
    yield

def test_list_accounts_generic():
    # Test GET /api/v1/Account
    response = client.get("/api/v1/Account")
    assert response.status_code == 200
    data = response.json()
    assert "list" in data
    assert "total" in data
    assert len(data["list"]) >= 1
    assert data["list"][0]["name"] == "Test Account"

def test_create_account_generic():
    # Test POST /api/v1/Account
    new_account = {"name": "New Generic Account", "billingAddressCity": "New City"}
    response = client.post("/api/v1/Account", json=new_account)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Generic Account"
    assert "id" in data

    # Verify it appears in list
    response = client.get("/api/v1/Account")
    data = response.json()
    names = [r["name"] for r in data["list"]]
    assert "New Generic Account" in names
