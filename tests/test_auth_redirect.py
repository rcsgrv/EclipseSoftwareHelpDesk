# Tests that accessing the register page when already logged in redirects to home page
def test_register_redirect_when_logged_in(logged_in_non_admin):
    response = logged_in_non_admin.get("/register", follow_redirects=True)

    assert b'You already have a registered account.' in response.data   

# Tests that accessing the login page when already logged in redirects to home page
def test_login_redirect_when_logged_in(logged_in_non_admin):
    response = logged_in_non_admin.get("/login", follow_redirects=True)

    assert b'You are already logged in.' in response.data

# Tests that accessing the login_2fa page when already logged in redirects to home page
def test_login_2fa_redirect_when_logged_in(logged_in_non_admin):
    response = logged_in_non_admin.get("/login_2fa", follow_redirects=True)

    assert b'You are already logged in.' in response.data

# Tests that accessing the setup_2fa page when already logged in redirects to home page
def test_setup_2fa_redirect_when_logged_in(logged_in_non_admin):
    response = logged_in_non_admin.get("/setup_2fa", follow_redirects=True)

    assert b'Your account already has 2FA setup.' in response.data   

# Tests that accessing the logout page requires a logged in user and redirects to login page when not authenticated
def test_logout_redirect_when_not_logged_in(client):
    response = client.get("/logout", follow_redirects=True)

    assert b'Please log in to access this page.' in response.data

# Tests that accessing the create_ticket page requires a logged in user and redirects to login page when not authenticated
def test_create_ticket_page_requires_login(client):
    response = client.get("/create_ticket", follow_redirects=True)

    assert b'Please log in to access this page.' in response.data

# Tests that accressing the ticket_details page requires a logged in user and redirects to login page when not authenticated
def test_ticket_details_page_requires_login(client, non_admin_ticket):
    response = client.get(f"/ticket_details/{non_admin_ticket.id}", follow_redirects=True)

    assert b'Please log in to access this page.' in response.data

 # Tests that accessing the setup_2fa page requires a logged in user and redirects to login page when not authenticated
def test_setup_2fa_page_requires_login(client):
    response = client.get("/setup_2fa", follow_redirects=True)

    assert b'No pending registration or login found.' in response.data

# Tests that accessing the login_2fa page requires a logged in user and redirects to login page when not authenticated
def test_login_2fa_page_requires_login(client):
    response = client.get("/login_2fa", follow_redirects=True)

    assert b'No pending login found.' in response.data

# Tests that accessing an admin-only page redirects to login page when not authenticated
def test_admin_page_requires_login(client):
    response = client.get("/users", follow_redirects=True)

    assert b'Please log in to access this page.' in response.data

# Tests that accessing an admin-only page redirects to home page when logged in as non-admin
def test_admin_page_requires_admin(logged_in_non_admin):
    response = logged_in_non_admin.get("/users", follow_redirects=True)

    assert b'You do not have permission to view this page.' in response.data
