import pytest
from HelpDesk import db
from HelpDesk.models import Ticket

# Test for homepage greeting when logged in as non-admin user
def test_homepage_greeting_non_admin(logged_in_non_admin, non_admin_user):
    response = logged_in_non_admin.get("/", follow_redirects=True)

    assert response.status_code == 200
    assert non_admin_user.forename.encode() in response.data
    assert b"Here's a summary of your tickets and activity." in response.data

# Test for homepage greeting when logged in as admin user
def test_homepage_greeting_admin(logged_in_admin, admin_user):
    response = logged_in_admin.get("/", follow_redirects=True)

    assert response.status_code == 200
    assert admin_user.forename.encode() in response.data
    assert b"Here's a summary of all tickets and user activity in the system." in response.data    

# Test that non-admin users only see their own tickets on their homepage
def test_ticket_display_non_admin(logged_in_non_admin, non_admin_ticket, admin_ticket, parse_ticket_table_rows):
    response = logged_in_non_admin.get("/", follow_redirects=True)

    rows = parse_ticket_table_rows(response)
    assert rows, "Tickets table not found or empty."

    # Extract columns by index
    ticket_types      = [row[0] for row in rows]
    subjects          = [row[1] for row in rows]
    descriptions      = [row[2] for row in rows]
    statuses          = [row[4] for row in rows]
    priorities        = [row[5] for row in rows]
    estimated_times   = [row[6] for row in rows]

    # non-admin ticket should appear
    assert non_admin_ticket.subject in subjects
    assert non_admin_ticket.ticket_type in ticket_types
    assert non_admin_ticket.description in descriptions
    assert non_admin_ticket.status in statuses
    assert non_admin_ticket.priority in priorities
    assert f"{non_admin_ticket.estimated_time:.2f}" in estimated_times

    # admin ticket should not appear
    assert admin_ticket.subject not in subjects
    assert admin_ticket.ticket_type not in ticket_types
    assert admin_ticket.description not in descriptions
    assert admin_ticket.status not in statuses
    assert admin_ticket.priority not in priorities
    assert f"{admin_ticket.estimated_time:.2f}" not in estimated_times

# Test that admin users see all tickets on their homepage
def test_ticket_display_admin(logged_in_admin, admin_ticket, non_admin_ticket, parse_ticket_table_rows):
    response = logged_in_admin.get("/", follow_redirects=True)

    rows = parse_ticket_table_rows(response)
    assert rows, "Tickets table not found or empty."

    # Extract columns by index
    ticket_types      = [row[0] for row in rows]
    subjects          = [row[1] for row in rows]
    descriptions      = [row[2] for row in rows]
    statuses          = [row[4] for row in rows]
    priorities        = [row[5] for row in rows]
    estimated_times   = [row[6] for row in rows]

    # non-admin ticket should appear
    assert non_admin_ticket.subject in subjects
    assert non_admin_ticket.ticket_type in ticket_types
    assert non_admin_ticket.description in descriptions
    assert non_admin_ticket.status in statuses
    assert non_admin_ticket.priority in priorities
    assert f"{non_admin_ticket.estimated_time:.2f}" in estimated_times

    # admin ticket should appear
    assert admin_ticket.subject in subjects
    assert admin_ticket.ticket_type in ticket_types
    assert admin_ticket.description in descriptions
    assert admin_ticket.status in statuses
    assert admin_ticket.priority in priorities
    assert f"{admin_ticket.estimated_time:.2f}" in estimated_times

# Tests that users can filter tickets on the homepage
def test_homepage_filters(logged_in_non_admin, tickets_for_filtering, parse_ticket_table_body):

    # Verify filtering by ticket type = Support Request returns Support Request ticket
    response = logged_in_non_admin.get("/?ticket_type=Support+Request", follow_redirects=True)
    table_text = parse_ticket_table_body(response)
    assert "Support Request" in table_text
    assert "Bug Report" not in table_text

    # Verify filtering by ticket type = Bug Report returns Bug Report ticket
    response = logged_in_non_admin.get("/?ticket_type=Bug+Report", follow_redirects=True)
    table_text = parse_ticket_table_body(response)
    assert "Bug Report" in table_text
    assert "Support Request" not in table_text

    # Verify filter by status = Open returns Open ticket
    response = logged_in_non_admin.get("/?status=Open", follow_redirects=True)
    table_text = parse_ticket_table_body(response)
    assert "Open" in table_text
    assert "Closed" not in table_text

    # Verify filter by status = Closed returns Closed ticket
    response = logged_in_non_admin.get("/?status=Closed", follow_redirects=True)
    table_text = parse_ticket_table_body(response)
    assert "Closed" in table_text
    assert "Open" not in table_text

    # Verify filter by priority = High returns High priority ticket
    response = logged_in_non_admin.get("/?priority=High", follow_redirects=True)
    table_text = parse_ticket_table_body(response)
    assert "High" in table_text
    assert "Low" not in table_text

    # Verify filter by priority = Low returns Low priority ticket
    response = logged_in_non_admin.get("/?priority=Low", follow_redirects=True)
    table_text = parse_ticket_table_body(response)
    assert "Low" in table_text
    assert "High" not in table_text

    # Verify filter by date created = Today returns both tickets
    response = logged_in_non_admin.get("/?date_created=Today", follow_redirects=True)
    table_text = parse_ticket_table_body(response)
    assert "Support Ticket" in table_text
    assert "Bug Ticket" in table_text

# Tests that a message is shown when a non-admin user has not raised any tickets
def test_no_tickets_message(logged_in_non_admin, app):
    with app.app_context():
        Ticket.query.delete()
        db.session.commit()
    response = logged_in_non_admin.get("/", follow_redirects=True)

    assert b"You have not raised any tickets yet" in response.data