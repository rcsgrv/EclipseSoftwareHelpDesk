import pytest
from HelpDesk import db
from HelpDesk.models import Ticket

def test_homepage_greeting(logged_in_non_admin, non_admin_user):
    response = logged_in_non_admin.get("/", follow_redirects=True)
    html = response.data.decode()

    assert response.status_code == 200
    assert non_admin_user.forename in html
    assert b"Here's a summary of your tickets and activity." in response.data

def test_ticket_display_non_admin(logged_in_non_admin, non_admin_ticket):
    response = logged_in_non_admin.get("/", follow_redirects=True)
    html = response.data.decode()

    assert non_admin_ticket.subject in html
    assert non_admin_ticket.description in html
    assert non_admin_ticket.ticket_type in html
    assert non_admin_ticket.status in html
    assert non_admin_ticket.priority in html

    assert "Administrator" not in html

def test_ticket_display_admin(logged_in_admin, admin_ticket, non_admin_ticket):
    response = logged_in_admin.get("/", follow_redirects=True)
    html = response.data.decode()

    assert admin_ticket.subject in html
    assert admin_ticket.description in html
    assert admin_ticket.ticket_type in html
    assert admin_ticket.status in html
    assert admin_ticket.priority in html

    assert non_admin_ticket.subject in html
    assert non_admin_ticket.description in html
    assert non_admin_ticket.ticket_type in html
    assert non_admin_ticket.status in html
    assert non_admin_ticket.priority in html

    assert "summary of all tickets" in html


def test_homepage_filters(logged_in_non_admin, non_admin_user, app):
    """Test filtering by ticket_type, status, priority, and date."""
    client = logged_in_non_admin
    with app.app_context():
        ticket1 = Ticket(
            ticket_type="Support Request",
            subject="Support Ticket",
            description="Support Description",
            status="Open",
            priority="High",
            estimated_time=2,
            created_by=non_admin_user.id,
            user_id=non_admin_user.id
        )
        ticket2 = Ticket(
            ticket_type="Bug Report",
            subject="Bug Ticket",
            description="Bug Description",
            status="Closed",
            priority="Low",
            estimated_time=1,
            created_by=non_admin_user.id,
            user_id=non_admin_user.id
        )
        db.session.add_all([ticket1, ticket2])
        db.session.commit()

    # Filter by ticket_type
    response = client.get("/?ticket_type=Support Request", follow_redirects=True)
    html = response.data.decode()
    assert "Support Ticket" in html
    assert "Bug Ticket" not in html

    # Filter by status
    response = client.get("/?status=Closed", follow_redirects=True)
    html = response.data.decode()
    assert "Bug Ticket" in html
    assert "Support Ticket" not in html

    # Filter by priority
    response = client.get("/?priority=High", follow_redirects=True)
    html = response.data.decode()
    assert "Support Ticket" in html
    assert "Bug Ticket" not in html

    # Filter by date (today)
    response = client.get("/?date_created=Today", follow_redirects=True)
    html = response.data.decode()
    assert "Support Ticket" in html
    assert "Bug Ticket" in html


def test_no_tickets_message(logged_in_non_admin, app):
    """Test the message when no tickets exist."""
    with app.app_context():
        # Delete all tickets for non-admin
        Ticket.query.delete()
        db.session.commit()

    response = logged_in_non_admin.get("/", follow_redirects=True)
    html = response.data.decode()

    assert "You have not raised any tickets yet" in html


def test_pagination(logged_in_non_admin, app, non_admin_user):
    per_page = 10
    with app.app_context():
        for i in range(15):
            ticket = Ticket(
                ticket_type="Feature Request",
                subject=f"Ticket {i}",
                description="Pagination test",
                status="Open",
                priority="Normal",
                estimated_time=1,
                created_by=non_admin_user.id,
                user_id=non_admin_user.id
            )
            db.session.add(ticket)
        db.session.commit()

    response = logged_in_non_admin.get("/", follow_redirects=True)
    html = response.data.decode()

    assert "Page 1 of 2" in html or "Next" in html  # Pagination should be present
