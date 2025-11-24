# Tests that ticket creation fails when ticket_type is missing
def test_create_ticket_missing_ticket_type(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "",
        "subject": "Test subject",
        "description": "This is a test description.",
        "status": "Open",
        "priority": "Medium",
        "estimated_time": 5.00
    }, follow_redirects=True)

    assert b'You must select a ticket type.' in response.data

# Tests that ticket creation fails when subject is blank
def test_create_ticket_blank_subject(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "",
        "description": "This is a test description.",
        "status": "Open",
        "priority": "Medium",
        "estimated_time": 5.00
    }, follow_redirects=True)

    assert b'Subject cannot be blank.' in response.data

def test_create_ticket_long_subject(logged_in_admin):
    long_subject = "A" * 101
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": long_subject,
        "description": "This is a test description.",
        "status": "Open",
        "priority": "Medium",
        "estimated_time": 5.00
    }, follow_redirects=True)

    assert b'Subject must not exceed 100 characters.' in response.data

def test_create_ticket_blank_description(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "Test Subject",
        "description": "",
        "status": "Open",
        "priority": "Medium",
        "estimated_time": 5.00
    }, follow_redirects=True)

    assert b'Description cannot be blank.' in response.data

def test_create_ticket_long_description(logged_in_admin):
    long_description = "A" * 501
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug",
        "subject": "Valid subject",
        "description": long_description,
        "status": "Open",
        "priority": "Medium",
        "estimated_time": 5.00
    }, follow_redirects=True)

    assert b'Description must not exceed 500 characters.' in response.data

def test_create_ticket_missing_status(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "Test Subject",
        "description": "This is a test description.",
        "status": "",
        "priority": "Medium",
        "estimated_time": 5.00
    }, follow_redirects=True)

    assert b'You must select a status.' in response.data

def test_create_ticket_missing_priority(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "Test Subject",
        "description": "This is a test description.",
        "status": "Open",
        "priority": "",
        "estimated_time": 5.00
    }, follow_redirects=True)

    assert b'You must select a priority.' in response.data

def test_create_ticket_invalid_estimated_time(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "Test Subject",
        "description": "This is a test description.",
        "status": "Open",
        "priority": "Medium",
        "estimated_time": "abc"
    }, follow_redirects=True)

    assert b'Estimated time must be a valid number.' in response.data

def test_create_ticket_estimated_time_too_small(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "Test subject",
        "description": "This is a test description.",
        "status": "Open",
        "priority": "Medium",
        "estimated_time": "0.5"
    }, follow_redirects=True)

    assert b'Estimated time cannot be less than 1 hour.' in response.data

def test_create_ticket_estimated_time_too_large(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "Test subject",
        "description": "This is a test description.",
        "status": "Open",
        "priority": "Medium",
        "estimated_time": 41.00
    }, follow_redirects=True)

    assert b'Estimated time cannot be more than 40 hours.' in response.data

def test_create_ticket_too_many_decimal_places(logged_in_admin):
    response = logged_in_admin.post("/create_ticket", data={
        "ticket_type": "Bug Report",
        "subject": "Test subject",
        "description": "This is a test description.",
        "status": "Open",
        "priority": "Medium",
        "estimated_time": 5.123
    }, follow_redirects=True)

    assert b'Estimated time cannot have more than 2 decimal places.' in response.data