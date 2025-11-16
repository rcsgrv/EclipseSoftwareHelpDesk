from flask import Blueprint, render_template, redirect, url_for, flash
from ..models import User, Ticket, Comment
from ..extensions import db
from flask_login import login_required, current_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@login_required
def users():
    if current_user.account_type != 'Administrator':
        flash("You do not have permission to view this page.", "error")
        return redirect(url_for('home.home'))

    non_administrator_users = User.query.filter(User.account_type == 'User').all()
    non_administrator_user_data = []
    for u in non_administrator_users:
        reported_tickets = Ticket.query.filter(Ticket.user_id == u.id).count()
        non_administrator_user_data.append({
            'id': u.id,
            'forename': u.forename,
            'surname': u.surname,
            'agency': u.agency,
            'ticket_count': reported_tickets
        })

    administrator_users = User.query.filter(User.account_type == 'Administrator').all()
    administrator_user_data = []
    for u in administrator_users:
        assigned_tickets = Ticket.query.filter(Ticket.assignee_id == u.id).count()
        administrator_user_data.append({
            'id': u.id,
            'forename': u.forename,
            'surname': u.surname,
            'agency': u.agency,
            'ticket_count': assigned_tickets
        })

    return render_template('users.html', non_administrator_users=non_administrator_user_data, administrator_users=administrator_user_data)


@users_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.account_type != 'Administrator':
        flash("You do not have permission to delete users.", "error")
        return redirect(url_for('users.users'))

    user = User.query.get_or_404(user_id)

    Ticket.query.filter_by(user_id=user.id).update({'user_id': None})
    Ticket.query.filter_by(assignee_id=user.id).update({'assignee_id': None})
    Ticket.query.filter_by(assignee=user).update({'assignee': None})
    Comment.query.filter_by(user_id=user.id).update({'user_id': None})

    db.session.delete(user)
    db.session.commit()
    flash(f"{user.forename} {user.surname} has been deleted.", "success")
    return redirect(url_for('users.users'))
