import pytest
from bs4 import BeautifulSoup
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
def logged_in_non_admin(client, non_admin_user):
    with client:
        client.post("/login", data={"email": non_admin_user.email, "password": "Password123!"
        }, follow_redirects=True)
        yield client


@pytest.fixture
def logged_in_admin(client, admin_user):
    with client:
        client.post("/login", data={"email": admin_user.email, "password": "Password123!"
        }, follow_redirects=True)
        yield client

@pytest.fixture
def non_admin_ticket(app, non_admin_user):
    with app.app_context():
        non_admin_ticket = Ticket(
            ticket_type="Support Request",
            subject="Non_Admin Subject",
            description="Non_Admin Description",
            status="Open",
            priority="High",
            estimated_time=8.00,
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
            subject="Admin Subject",
            description="Admin Description",
            status="In Progress",
            priority="Low",
            estimated_time=4.00,
            created_by=admin_user.id,
            user_id=admin_user.id
        )
        db.session.add(admin_ticket)
        db.session.commit()
        return db.session.get(Ticket, admin_ticket.id) 
    
@pytest.fixture
def tickets_for_filtering(app, non_admin_user):
    with app.app_context():
        supportRequestTicket = Ticket(
            ticket_type="Support Request",
            subject="Support Ticket",
            description="Support Description",
            status="Open",
            priority="High",
            estimated_time=2.00,
            created_by=non_admin_user.id,
            user_id=non_admin_user.id
        )
        bugReportTicket = Ticket(
            ticket_type="Bug Report",
            subject="Bug Ticket",
            description="Bug Description",
            status="Closed",
            priority="Low",
            estimated_time=1.50,
            created_by=non_admin_user.id,
            user_id=non_admin_user.id
        )
        db.session.add_all([supportRequestTicket, bugReportTicket])
        db.session.commit()
        return [supportRequestTicket, bugReportTicket]    
    
# For the following fixtures, BeautifulSoup is used to parse HTML responses.
# This allows tests to verify specific content within the HTML structure.
# For example, extracting table rows or body content for validation. 
# This is required due to the HTML in home.html containing drop downs and other elements that interfere with simple string matching 
# (i.e. the priority filter drop down contains the word "Low" within it, therefore when testing filter functionality as non_admin_user tests were failing when asserting that 'Low' was not in response.data
# because 'Low' was in the response_data due to the drop down).   
@pytest.fixture
def parse_ticket_table_body():
    def _parse(response):
        soup = BeautifulSoup(response.data, "html.parser")
        tbody = soup.find("tbody")
        return tbody.text if tbody else ""
    return _parse    

@pytest.fixture
def parse_ticket_table_rows():
    def _parse(response):
        soup = BeautifulSoup(response.get_data(as_text=True), "html.parser")

        table = soup.find("table")
        if not table:
            return [] # Return empty list if table is not found

        rows = table.find_all("tr")[1:]  # Ignore the header row

        parsed_rows = [] # Extract text from each cell in the rows
        for row in rows:
            cols = row.find_all("td") # Get all columns in the row that are <td> elements
            parsed_rows.append([col.get_text(strip=True) for col in cols]) # Append the text content of each column to parsed_rows

        return parsed_rows # Return the list of parsed rows

    return _parse
