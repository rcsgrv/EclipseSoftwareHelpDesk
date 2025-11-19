def test_home_loads_for_user(logged_in_non_admin):
    response = logged_in_non_admin.get("/", follow_redirects=True)
    assert b'Ticket' in response.data or response.status_code == 200

def test_home_filters_only_user_tickets(logged_in_non_admin, non_admin_ticket):
    response = logged_in_non_admin.get("/", follow_redirects=True)
    assert b'Test Ticket' in response.data