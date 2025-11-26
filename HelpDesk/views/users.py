from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import User, Ticket, Comment
from ..extensions import db
from flask_login import login_required, current_user

# Route logic was informed by a tutorial by Tech With Tim (Tech With Tim, 2021).

# This Blueprint handles user management functionality including viewing, updating, and deleting users.
# It enforces administrator-only access to ensure only authorised users can manage user accounts.

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        flash("You do not have permission to view this page.", "error")
        return redirect(url_for('home.home'))

    non_administrator_data = []
    administrator_data = []

    users = db.session.query(User).all()
    for u in users:
        reported_tickets = db.session.query(Ticket).filter(Ticket.user_id == u.id).count()
        assigned_tickets = db.session.query(Ticket).filter(Ticket.assignee_id == u.id).count()

        data = {
            'id': u.id,
            'forename': u.forename,
            'surname': u.surname,
            'ticket_count': reported_tickets if not u.is_admin else assigned_tickets,
            'is_admin': u.is_admin
        }

        if u.is_admin:
            administrator_data.append(data)
        else:
            non_administrator_data.append(data)

    return render_template(
        'users.html',
        non_administrator_data=non_administrator_data,
        administrator_data=administrator_data
    )

@users_bp.route('/update_admin', methods=['POST'])
@login_required
def update_admin():
    if not current_user.is_admin:
        flash("You do not have permission to update user roles.", "error")
        return redirect(url_for('users.users'))

    # Get all user Ids
    user_ids = request.form.getlist('user_ids')  

    if not user_ids:
        flash("You have not selected any users to update.", "error")
        return redirect(url_for('users.users'))

    promoted_users = []
    demoted_users = []

    for uid in user_ids:
        user = db.session.query(User).get(uid)
        if not user or user.id == current_user.id:
            continue  

        # This will check the checkbox value for the user
        new_is_admin = True if request.form.get(f'is_admin_{uid}') == 'on' else False

        if user.is_admin != new_is_admin:
            if user.is_admin and not new_is_admin:
                # Demotion
                db.session.query(Ticket).filter_by(assignee_id=user.id).update({'assignee_id': None})
                demoted_users.append(f"{user.forename} {user.surname}")
            elif not user.is_admin and new_is_admin:
                # Promotion
                promoted_users.append(f"{user.forename} {user.surname}")

            user.is_admin = new_is_admin

    db.session.commit()

    # Prepare flash messages
    role_messages = []
    if promoted_users:
        role_messages.append(f"The following users have been promoted to administrators: {', '.join(promoted_users)}")
    if demoted_users:
        role_messages.append(f"The following users have been demoted from administrators: {', '.join(demoted_users)}")

    if role_messages:
        flash("<br>".join(role_messages), "success")
    else:
        flash("No changes have been made.", "info")

    return redirect(url_for('users.users'))

@users_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("You do not have permission to delete users.", "error")
        return redirect(url_for('users.users'))

    user = db.session.query(User).get_or_404(user_id)

    db.session.query(Ticket).filter_by(user_id=user.id).update({'user_id': None})
    db.session.query(Ticket).filter_by(assignee_id=user.id).update({'assignee_id': None})
    db.session.query(Comment).filter_by(user_id=user.id).update({'user_id': None})

    db.session.delete(user)
    db.session.commit()
    flash(f"{user.forename} {user.surname} has been deleted.", "success")
    return redirect(url_for('users.users'))