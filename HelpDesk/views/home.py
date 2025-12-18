from datetime import datetime, timedelta
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..models import Ticket, User
from ..extensions import db

# Route logic was informed by a tutorial by Tech With Tim (Tech With Tim, 2021).

# This Blueprint handles the home page functionality, including displaying tickets with filtering options.
# It enforces user authentication to ensure only logged-in users can access the home page.

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Base query
    base_query = Ticket.query

    # If non-admin, only show their own tickets
    if not current_user.is_admin:
        base_query = base_query.filter(Ticket.user_id == current_user.id)

    query = base_query

    # Apply filters from request args
    ticket_type_filter = request.args.get('ticket_type')
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    assignee_filter = request.args.get('assignee')
    date_filter = request.args.get('date_created')

    if ticket_type_filter:
        query = query.filter(Ticket.ticket_type == ticket_type_filter)
    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    if priority_filter:
        query = query.filter(Ticket.priority == priority_filter)
    if assignee_filter:
        if assignee_filter.lower() == 'unassigned':
            query = query.filter(Ticket.assignee_id.is_(None))
        else:
            try:
                assignee_id = int(assignee_filter)
                query = query.filter(Ticket.assignee_id == assignee_id)
            except ValueError:
                pass
    if date_filter:
        now = datetime.now()
        if date_filter == 'Today':
            query = query.filter(db.func.date(Ticket.date_created) == now.date())
        elif date_filter == 'Last 7 Days':
            query = query.filter(Ticket.date_created >= now - timedelta(days=7))
        elif date_filter == 'This Month':
            query = query.filter(Ticket.date_created >= now.replace(day=1))

    tickets = query.order_by(Ticket.id.desc()).paginate(page=page, per_page=per_page)

    # Counts for dashboard widgets
    open_tickets = base_query.filter(Ticket.status == 'Open').count()
    in_progress_tickets = base_query.filter(Ticket.status == 'In Progress').count()
    on_hold_pending_tickets = base_query.filter(Ticket.status == 'On Hold / Pending').count()
    resolved_tickets = base_query.filter(Ticket.status == 'Resolved').count()
    closed_tickets = base_query.filter(Ticket.status == 'Closed').count()
    
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
        filters_applied=any([ticket_type_filter, status_filter, priority_filter, assignee_filter, date_filter]),
        datetime=datetime
    )