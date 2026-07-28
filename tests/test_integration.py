import pytest
from app import create_app
from app.extensions import db
from app.models import User, Position


@pytest.fixture()
def client(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Seed default: admin, positions
        user = User(username="admin", role="admin")
        user.set_password("admin123")
        db.session.add(user)
        pos = Position(name="Staff", base_salary=6000000, description="Staff default")
        db.session.add(pos)
        db.session.commit()
    with app.test_client() as client:
        yield client


def test_login_and_dashboard_redirect(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Dashboard Admin" in response.data


def test_login_case_insensitive(client):
    """Login harus case-insensitive"""
    # Buat user langsung di DB
    with client.application.app_context():
        user = User(username="CaseUser", role="manager")
        user.set_password("casepass123")
        db.session.add(user)
        db.session.commit()
    # Login dengan lowercase
    response = client.post(
        "/login",
        data={"username": "caseuser", "password": "casepass123"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Review Payroll" in response.data
