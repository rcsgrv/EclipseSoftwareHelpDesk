# Tests that users are able to create tickets
def test_create_ticket(logged_in_non_admin):
    response = logged_in_non_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "New Ticket",
        "description": "New Description",
        "status": "In Progress",
        "priority": "Low",
        "estimated_time": 2.00
    }, follow_redirects=True)
    assert b'Ticket created successfully' in response.data

# Tests that users are able to edit tickets
def test_edit_ticket(logged_in_non_admin, non_admin_ticket):
    response = logged_in_non_admin.post(f"/ticket_details/{non_admin_ticket.id}", data={
        "ticket_type": "Feature Request",
        "subject": "Updated Ticket",
        "description": "Updated Description",
        "status": "Open",
        "priority": "High",
        "estimated_time": 5.00
    }, follow_redirects=True)
    assert b'Ticket updated successfully' in response.data

# Tests that users are able to add comments to tickets
def test_add_comment(logged_in_non_admin, non_admin_ticket):
    response = logged_in_non_admin.post(f"/ticket_details/{non_admin_ticket.id}", data={
        "comment_text": "Test comment"
    }, follow_redirects=True)
    assert b'Comment added successfully' in response.data

# Tests that admin users are able to delete tickets
def test_delete_ticket(logged_in_admin, admin_ticket):
    response = logged_in_admin.post(f"/delete_ticket/{admin_ticket.id}", follow_redirects=True)
    assert b'Ticket deleted successfully.' in response.data

# Tests that non-admin users cannot access other users' tickets
def test_non_admin_ticket_access_control(logged_in_non_admin, admin_ticket):
    response = logged_in_non_admin.get(f"/ticket_details/{admin_ticket.id}", follow_redirects=True)
    assert b'You do not have permission to view this ticket.' in response.data    

# Tests that non-admin users cannot delete tickets
def test_non_admin_cannot_delete_ticket(logged_in_non_admin, non_admin_ticket):
    response = logged_in_non_admin.post(f"/delete_ticket/{non_admin_ticket.id}", follow_redirects=True)
    assert b'You do not have permission to delete this ticket.' in response.data