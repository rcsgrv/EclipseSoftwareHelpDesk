import random
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from .extensions import db
from .models import User, Ticket

def populate_seed_data():
    if User.query.first():
        print("Seed data already exists.")
        return
    
    # 10 Users
    forenames = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Hannah', 'Ian', 'Judy']
    surnames   = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']

    random.shuffle(forenames)
    random.shuffle(surnames)

    users = []
    for i in range(10):
        is_admin = i < 2  # first two users are admins
       
        user = User(
            forename=forenames[i],
            surname=surnames[i],
            email=f"user{i+1}@test.com",
            password=generate_password_hash(f"password{i+1}"),
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
        'Candidate schedule tab slow',
        'Overlapping export template fields',
        'System Mailbox naming confusion',
        'Email attachments lost',
        'Duplicate shortlist record issue',
        'Adjusted timesheets error',
        'Placement bookings log incorrect',
        'Error deleting booking',
        'Client contact logs not linking',
        'Users cannot login'
    ]

    descriptions = [
        'Schedule tab is very slow when candidate has many placements.',
        'Fields overlap on export template form.',
        'Form "System Mailbox" should be renamed to avoid confusion.',
        'Attachments disappear after merging emails.',
        'System allowed adding duplicate shortlist record.',
        'Error when marking adjusted timesheets as Rejected.',
        'Requirements Added logs created incorrectly on placement bookings.',
        'Error occurs when deleting a booking from placement record.',
        'Client Contact logs do not link to the client record.',
        'Multiple users report login failures this morning.'
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
    print("Seeded 10 users and 10 tickets.")