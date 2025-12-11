import random
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from .extensions import db
from .models import User, Ticket

def populate_seed_data():
    if User.query.first():
        print("Seed data already exists within the database.")
        return
    
    # 10 Users
    forenames = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Hannah', 'Ian', 'Judy']
    surnames   = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']

    random.shuffle(forenames)
    random.shuffle(surnames)

    users = []
    for i in range(10):
        is_admin = i < 2  # first two users are administrators
       
        user = User(
            forename=forenames[i],
            surname=surnames[i],
            email=f"user{i+1}@recruitment-software.co.uk",
            password=generate_password_hash(f"Password{i+1}!"),
            is_admin= True if is_admin else False,
            totp_secret=None,
            is_2fa_enabled=False
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    users = User.query.all()

    administrator = [u for u in users if u.is_admin]
    non_administrators = [u for u in users if not u.is_admin]

    # 10 Tickets
    subjects = [
        'The candidate schedule tab is very slow to load',
        'There are overlapping fields on the Back Office Export Template form!',
        'Why is the System Mailbox form named that way?',
        'Where are the email attachments gone after merging?',
        'I have added the same shortlist record multiple times and I thought duplicates were not allowed?',
        'Adjusted timesheets are erroring when I update them to Rejected status. This is business critical!',
        'When adding bookings to a placement, Requirements Added logs are being created incorrectly. This is confusing for auditors.',
        'I am getting an error when trying to delete bookings from a placement record.',
        'Client Contact Record Opened logs do not link to the client record.',
        'IMMEDIATE ISSUE: I have had users report that they cannot login to Eclipse this morning!'
    ]

    descriptions = [
        'The schedule tab takes forever to load when a candidate has a lot of placements. It can take 20-30 seconds each time, which really slows down my workflow.',
        'Some fields overlap on the export template form, making it hard to see everything properly when creating a new template.',
        'Why have you named the form that contains Mailbox Scanner Rulsets \'System Mailbox\'?. Please can you rename this form? I think it should be renamed to \'Mailbox Scanner Ruleset\' to avoid confusion.',
        'After merging an email, all attachments disappeared. I can\'t find any of the files and I\'m worried that they might be lost.',
        'I added the same shortlist record more than once and the system didn\'t stop me or give a warning. I thought duplicates weren\'t allowed. Is this a bug? The record I did this with is CAN-3451.',
        'When I try to mark adjusted timesheets as Rejected, I get an error. This is causing major problems for payroll and is urgent.',
        'Every time I add bookings to placement records, it creates \'Requirements Added\' logs incorrectly. Auditors get confused because the logs don\'t match what actually happened.',
        'I tried deleting a booking from a placement record (PLC-34087), but an error pops up every time. I can\'t remove the booking, which is holding up my work.',
        'The logs that show when a client contact record is opened don\'t link to the client properly. This makes it really hard to track client activity or follow up',
        'Several users reported that they cannot login to Eclipse at all this morning. Everyone is locked out and it\'s affecting the whole team\'s ability to work'
    ]
    
    ticket_type = ['Support Request', 'Feature Request', 'Bug Report']
    statuses = ['Open', 'In Progress', 'On Hold / Pending', 'Resolved', 'Closed']
    priorities = ['Low', 'Normal', 'High']
    estimated_times = [1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]

    tickets = []
    for i in range(10):
        creator = non_administrators[i % len(non_administrators)]
        assignee = random.choice(administrator)

        ticket = Ticket(
            ticket_type=random.choice(ticket_type),
            subject=subjects[i],
            description=descriptions[i],
            status=random.choice(statuses),
            priority=random.choice(priorities),
            estimated_time=random.choice(estimated_times),
            created_by=f"{creator.forename} {creator.surname}",
            updated_by=None,
            date_created=datetime.now(),
            date_updated=None,
            user_id=creator.id,
            assignee_id=assignee.id
        )
        tickets.append(ticket)

    db.session.add_all(tickets)
    db.session.commit()
    print("10 users and 10 tickets have been created within the database.")