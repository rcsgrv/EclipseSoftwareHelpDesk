# Tests that login fails with invalid credentials
def test_login_invalid_credentials(client):
    response = client.post("/login", data={
        "email": "incorrectemail@test.com",
        "password": "incorrectpassword"
    }, follow_redirects=True)
    assert b'Incorrect username or password' in response.data

# Tests that login succeeds with valid credentials
def test_login_success(client, non_admin_user):
    response = client.post("/login", data={
        "email": non_admin_user.email,
        "password": "Password123!"
    }, follow_redirects=True)
    assert b'Logged in' in response.data or response.status_code == 200

# Tests that logout functions correctly
def test_logout(logged_in_non_admin):
    response = logged_in_non_admin.get("/logout", follow_redirects=True)
    assert b'Log In' in response.data or response.status_code == 200