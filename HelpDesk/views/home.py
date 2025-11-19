from datetime import datetime, timedelta
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..models import Ticket, User
from .. import db

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Ticket.query

    # Filters tickets based on user role. Administrators see all tickets, users see only their own.
    if current_user.is_admin == False:
        query = query.filter_by(user_id=current_user.id)

    filters = {}
    if current_user.is_admin == False:
        filters['user_id'] = current_user.id

    open_tickets = Ticket.query.filter_by(**filters, status='Open').count()
    in_progress_tickets = Ticket.query.filter_by(**filters, status='In Progress').count()
    on_hold_pending_tickets = Ticket.query.filter_by(**filters, status='On Hold / Pending').count()
    resolved_tickets = Ticket.query.filter_by(**filters, status='Resolved').count()
    closed_tickets = Ticket.query.filter_by(**filters, status='Closed').count()

    # Filter parameters
    ticket_type_filter = request.args.get('ticket_type')
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    assignee_filter = request.args.get('assignee')
    date_filter = request.args.get('date_created')

    # Filtering logic
    if ticket_type_filter:
        query = query.filter_by(ticket_type=ticket_type_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)

    # Assignee filter including Unassigned tickets
    if assignee_filter:
        if assignee_filter.lower() == 'unassigned':
            query = query.filter(Ticket.assignee_id.is_(None))
        else:
            try:
                assignee_id = int(assignee_filter)
                query = query.filter(Ticket.assignee_id == assignee_id)
            except ValueError:
                pass
         
    # Date range filters (i.e. Tickets created today, last 7 days, or this month)
    now = datetime.now()
    if date_filter == 'Today':
        query = query.filter(db.func.date(Ticket.date_created) == now.date())
    elif date_filter == 'Last 7 Days':
        start = now - timedelta(days=7)
        query = query.filter(Ticket.date_created >= start)
    elif date_filter == 'This Month':
        start = now.replace(day=1)
        query = query.filter(Ticket.date_created >= start)

    # Determine if any filters are applied
    filters_applied = any([
    ticket_type_filter and ticket_type_filter != "",
    status_filter and status_filter != "",
    priority_filter and priority_filter != "",
    assignee_filter and assignee_filter != "",
    date_filter and date_filter != ""
    ])

    # Pagination
    tickets = query.order_by(Ticket.id.desc()).paginate(page=page, per_page=per_page)

    # Only show assignees who have tickets assigned. 
    assignees = (
        db.session.query(User)
        .join(Ticket, Ticket.assignee_id == User.id)
        .filter(Ticket.assignee_id.isnot(None))
        .distinct()
        .all()
    )

    return render_template(
        "home.html",
        user=current_user,
        tickets=tickets,
        assignees=assignees,
        open_tickets=open_tickets,
        in_progress_tickets=in_progress_tickets,
        on_hold_pending_tickets=on_hold_pending_tickets,
        resolved_tickets=resolved_tickets,
        closed_tickets=closed_tickets,
        filter_assignee=assignee_filter,
        filter_ticket_type=ticket_type_filter,
        filter_status=status_filter,
        filter_priority=priority_filter,
        filter_date=date_filter,
        filters_applied=filters_applied,
        datetime=datetime
    )