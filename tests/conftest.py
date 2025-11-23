import pytest
from HelpDesk import create_app
from HelpDesk.extensions import db
from HelpDesk.models import User, Ticket
from werkzeug.security import generate_password_hash

class TestConfig:
    TESTING = True
    SECRET_KEY = "Test"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    DISABLE_2FA = True  # disabled for testing purposes

@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_user(app):
    with app.app_context():
        user = User(
            email="adminuser@test.com",
            forename="Admin",
            surname="User",
            password=generate_password_hash("Password123!"),
            is_admin=True,
        )
        db.session.add(user)
        db.session.commit()
        return db.session.get(User, user.id)

@pytest.fixture
def non_admin_user(app):
    with app.app_context():
        user = User(
            email="nonadmin@test.com",
            forename="NonAdmin",
            surname="User",
            password=generate_password_hash("Password123!"),
            is_admin=False,
        )
        db.session.add(user)
        db.session.commit()
        return db.session.get(User, user.id)
    
@pytest.fixture
def logged_in_admin(client, admin_user):
    """Log in the admin user and return the client."""
    client.post(
        "/login",
        data={"email": admin_user.email, "password": "Password123!"},
        follow_redirects=True
    )
    return client

@pytest.fixture
def logged_in_non_admin(client, non_admin_user):
    client.post(
        "/login",
        data={"email": non_admin_user.email, "password": "Password123!"},
        follow_redirects=True
    )
    return client

@pytest.fixture
def non_admin_ticket(app, non_admin_user):
    with app.app_context():
        non_admin_ticket = Ticket(
            ticket_type="Bug Report",
            subject="Test Subject",
            description="Test Description",
            status="Open",
            priority="Normal",
            estimated_time=4.00,
            created_by=non_admin_user.id,
            user_id=non_admin_user.id
        )
        db.session.add(non_admin_ticket)
        db.session.commit()
        return db.session.get(Ticket, non_admin_ticket.id)
    
@pytest.fixture
def admin_ticket(app, admin_user):
    with app.app_context():
        admin_ticket = Ticket(
            ticket_type="Bug Report",
            subject="Test Subject",
            description="Test Description",
            status="Open",
            priority="Normal",
            estimated_time=4.00,
            created_by=admin_user.id,
            user_id=admin_user.id
        )
        db.session.add(admin_ticket)
        db.session.commit()
        return db.session.get(Ticket, admin_ticket.id)    