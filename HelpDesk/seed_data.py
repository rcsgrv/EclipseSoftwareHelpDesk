import random
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from .extensions import db
from .models import User, Ticket, Agency

def populate_seed_data():
    if User.query.first():
        print("Seed data already exists.")
        return
    
    # Agencies
    agency_names = [
        'Eclipse Software',
        'Purple Yeti Recruitment',
        'Aspire Talent Group',
        'Summit Staffing Solutions',
        'BrightPath Recruitment',
        'TechSure Recruitment',
        'Innovate Hire',
        'FutureForce Staffing',
        'Lighthouse Talent Group',
        'Pinnacle Placement Services'
    ]

    agency_objects = []
    for name in agency_names:
        agency_objects.append(Agency(name=name))
        
    db.session.add_all(agency_objects)
    db.session.commit()

    agencies = Agency.query.all()

    eclipse_agency = Agency.query.filter_by(name='Eclipse Software').first()

    # Users
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
            email=f"user{i+1}@test.com",
            password=generate_password_hash(f"password{i+1}"),
            account_type="Administrator" if is_admin else "User",
            agency_id=eclipse_agency.id if is_admin else agencies[i].id,
            totp_secret=None,
            is_2fa_enabled=False
        )

        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    users = User.query.all()

    # Tickets
    subjects = [...]
    descriptions = [...]

    statuses = ['Open', 'In Progress', 'On Hold / Pending', 'Resolved', 'Closed']
    priorities = ['Low', 'Normal', 'High']
    estimated_times = [1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]

    random.shuffle(statuses)
    random.shuffle(priorities)
    random.shuffle(estimated_times)

    admins = [u for u in users if u.account_type == 'Administrator']
    non_admins = [u for u in users if u.account_type != 'Administrator']

    tickets = []
    for i in range(10):
        creator = random.choice(non_admins)
        assignee = random.choice(admins)

        ticket = Ticket(
            subject=subjects[i],
            description=descriptions[i],
            status=statuses[i % len(statuses)],
            priority=priorities[i % len(priorities)],
            estimated_time=estimated_times[i % len(estimated_times)],
            created_by=f"{creator.forename} {creator.surname}",
            updated_by=None,
            date_created=datetime.now(timezone.utc),
            date_updated=None,
            user_id=creator.id,
            assignee_id=assignee.id
        )
        tickets.append(ticket)

    db.session.add_all(tickets)
    db.session.commit()

    print("Seeded agencies, users, and tickets.")