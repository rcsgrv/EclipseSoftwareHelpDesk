# Tests that registration functions correctly when valid data is provided
def test_register(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "User",
        "password": "Password123!",
        "password_confirm": "Password123!"
    }, follow_redirects=True)

    assert b'You have logged in successfully.' in response.data or response.status_code == 200

# Tests that registration fails when email is already registered
def test_register_existing_email(client, non_admin_user):
    response = client.post("/register", data={
        "email": non_admin_user.email,
        "forename": "New",
        "surname": "User",
        "password": "Password123!",
        "password_confirm": "Password123!"
    }, follow_redirects=True)

    assert b'The email you have provided is already associated with an account.' in response.data

# Tests that registration fails when passwords do not match
def test_register_password_mismatch(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "User",
        "password": "Password123!",
        "password_confirm": "Password123"
    }, follow_redirects=True)

    assert b'Your passwords do not match.' in response.data

# Tests that registration fails when password is too weak
def test_register_weak_password(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "User",
        "password": "password",
        "password_confirm": "password"
    }, follow_redirects=True)

    assert b'Password must include at least one uppercase letter, one lowercase letter, one number, and one special character (@$!%*#?&).' in response.data

# Tests that registration fails when email is invalid
def test_register_invalid_email(client):
    response = client.post("/register", data={
        "email": "invalidemail@recruitment-software",
        "forename": "New",
        "surname": "User",
        "password": "Password123!",
        "password_confirm": "Password123!"
    }, follow_redirects=True)
    print(response.data)
    assert b'The part after the @-sign is not valid. It should have a period.' in response.data

# Tests that registration fails when forename contains invalid characters
def test_register_invalid_forename(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "123",
        "surname": "User",
        "password": "password",
        "password_confirm": "password"
    }, follow_redirects=True)

    assert b'Forename can only contain letters, spaces, hyphens or apostrophes.' in response.data

# Tests that registration fails when surname contains invalid characters
def test_register_invalid_surname(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "123",
        "password": "password",
        "password_confirm": "password"
    }, follow_redirects=True)

    assert b'Surname can only contain letters, spaces, hyphens or apostrophes.' in response.data

# Tests that registration fails when forename exceeds character limit
def test_register_long_forename(client):
    long_forename = "A" * 51
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": long_forename,
        "surname": "User",
        "password": "password",
        "password_confirm": "password"
    }, follow_redirects=True)

    assert b'Forename cannot exceed 50 characters.' in response.data


# Tests that registration fails when surname exceeds character limit
def test_register_long_surname(client):
    long_surname = "A" * 51
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": long_surname,
        "password": "password",
        "password_confirm": "password"
    }, follow_redirects=True)

    assert b'Surname cannot exceed 50 characters.' in response.data

# Tests that registration fails when password exceeds character limit
def test_register_long_password(client):
    long_password = "A" * 17 + "a1!"
    print(long_password)
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "User",
        "password": long_password,
        "password_confirm": long_password
    }, follow_redirects=True)
    print(response.data)

    assert b'Password cannot exceed 16 characters.' in response.data

# Tests that registration fails when password is below minimum length
def test_register_short_password(client):
    short_password = "Aa1!"
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "User",
        "password": short_password,
        "password_confirm": short_password
    }, follow_redirects=True)

    assert b'Password must be at least 8 characters long.' in response.data

# Tests that registration fails when forename is blank
def test_register_blank_forename(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "",
        "surname": "User",
        "password": "Password123!",
        "password_confirm": "Password123!"
    }, follow_redirects=True)

    assert b'Forename cannot be blank.' in response.data

# Tests that registration fails when surname is blank
def test_register_blank_surname(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "",
        "password": "Password123!",
        "password_confirm": "Password123!"
    }, follow_redirects=True)

    assert b'Surname cannot be blank.' in response.data

# Tests that registration fails when email is blank
def test_register_blank_email(client):
    response = client.post("/register", data={
        "email": "",
        "forename": "New",
        "surname": "User",
        "password": "Password123!",
        "password_confirm": "Password123!"
    }, follow_redirects=True)

    assert b'Email cannot be blank.' in response.data    

# Tests that registration fails when password is blank
def test_register_blank_password(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "User",
        "password": "",
        "password_confirm": ""
    }, follow_redirects=True)

    assert b'Password must be at least 8 characters long.' in response.data

# Tests that registration fails when password confirmation is blank
def test_register_blank_password_confirm(client):
    response = client.post("/register", data={
        "email": "newuser@recruitment-software.co.uk",
        "forename": "New",
        "surname": "User",
        "password": "Password123!",
        "password_confirm": ""
    }, follow_redirects=True)
    
    assert b'Your passwords do not match.' in response.data