from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import User, Ticket, Comment
from ..extensions import db
from flask_login import login_required, current_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        flash("You do not have permission to view this page.", "error")
        return redirect(url_for('home.home'))

    # Build user data dynamically
    non_administrator_data = []
    administrator_data = []

    users = User.query.all()
    for u in users:
        reported_tickets = Ticket.query.filter(Ticket.user_id == u.id).count()
        assigned_tickets = Ticket.query.filter(Ticket.assignee_id == u.id).count()

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

    user_id = request.form.get('user_id')
    if not user_id:
        flash("User not specified.", "error")
        return redirect(url_for('users.users'))

    user = User.query.get_or_404(user_id)

    # This will prevent self-demotion, even though the checkbox will not be shown for the current user
    if user.id == current_user.id:
        flash("You cannot change your own admin status.", "error")
        return redirect(url_for('users.users'))
    
    # This determines the new admin status based on the checkbox
    new_is_admin = True if request.form.get('is_admin') == 'on' else False

    # If demoting from admin to non-admin, unassign their tickets
    if user.is_admin and not new_is_admin:
        Ticket.query.filter_by(assignee_id=user.id).update({'assignee_id': None})
        db.session.commit()

    user.is_admin = new_is_admin
    db.session.commit()
    flash(f"{user.forename} {user.surname} has had their admin status updated.", "success")
    return redirect(url_for('users.users'))


@users_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("You do not have permission to delete users.", "error")
        return redirect(url_for('users.users'))

    user = User.query.get_or_404(user_id)

    Ticket.query.filter_by(user_id=user.id).update({'user_id': None})
    Ticket.query.filter_by(assignee_id=user.id).update({'assignee_id': None})
    Comment.query.filter_by(user_id=user.id).update({'user_id': None})

    db.session.delete(user)
    db.session.commit()
    flash(f"{user.forename} {user.surname} has been deleted.", "success")
    return redirect(url_for('users.users'))