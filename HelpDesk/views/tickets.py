from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Comment, Ticket, User
from ..utils.ticket_helper import validate_ticket_form, render_ticket_form
from ..extensions import db

# This Blueprint handles ticket management functionality including creating, viewing, editing,and deleting tickets.
# This Blueprint enforces user authentication and access control, allowing only ticket owners to view their own tickets.
# Administrators are able to view and edit tickets regardless of ownership.
# Form validation is used to ensure data integrity before database operations are performed, and appropriate user feedback is provided via flash messages. 

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        subject = request.form.get('subject')
        description = request.form.get('description')
        status = request.form.get('status')
        priority = request.form.get('priority')
        estimated_time = request.form.get('estimated_time')

        error = validate_ticket_form(subject, description, status, priority, estimated_time)
        if error:
            return render_ticket_form(
                'create_ticket.html',
                error=error,
                user=current_user,
                subject=subject,
                description=description,
                status=status,
                priority=priority,
                estimated_time=estimated_time
            )

        new_ticket = Ticket(
            subject=subject,
            description=description,
            status=status,
            priority=priority,
            estimated_time=float(estimated_time),
            created_by=f"{current_user.forename} {current_user.surname}",
            updated_by=None,
            date_updated=None,
            date_created=datetime.now(),
            user_id=current_user.id
        )
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket created successfully!', category='success')
        return redirect(url_for('home.home'))

    return render_template('create_ticket.html', user=current_user)

@tickets_bp.route('/ticket_details/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_details(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    admin_users = User.query.filter_by(account_type='Administrator').all()

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('home.home'))

    if ticket.user_id != current_user.id and current_user.account_type != 'Administrator':
        flash('You do not have permission to view this ticket.', category='error')
        return redirect(url_for('home.home'))

    if request.method == 'POST' and 'subject' in request.form:
        subject = request.form.get('subject')
        description = request.form.get('description')
        status = request.form.get('status')
        priority = request.form.get('priority')
        estimated_time = request.form.get('estimated_time')
        created_by = request.form.get('created_by')
        updated_by = request.form.get('updated_by')
        date_created = request.form.get('date_created')
        date_updated = request.form.get('date_updated')
        assignee_id = request.form.get('assignee_id')
        assignee = request.form.get('assignee')

        error = validate_ticket_form(subject, description, status, priority, estimated_time)
        if error:
            flash(error, 'error')
        else:
            ticket.subject = subject
            ticket.description = description
            ticket.status = status
            ticket.priority = priority
            ticket.estimated_time = float(estimated_time)
            ticket.created_by = created_by
            ticket.updated_by = updated_by
            ticket.date_created = date_created  
            ticket.date_updated = datetime.now()
            ticket.assignee_id = assignee_id
            ticket.assignee = assignee

            db.session.commit()
            flash('Ticket updated successfully.', category='success')
            return redirect(url_for('tickets.ticket_details', ticket_id=ticket.id))
        
    if request.method == 'POST' and 'comment_text' in request.form:
        comment_text = request.form.get('comment_text').strip()
        if comment_text:
            new_comment = Comment(
                comment_text=comment_text,
                author_fullname=f"{current_user.forename} {current_user.surname}",
                user_id=current_user.id,
                ticket_id=ticket.id
            )
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added successfully.', 'success')
            return redirect(url_for('tickets.ticket_details', ticket_id=ticket.id))
        else:
            flash('Comment cannot be empty.', 'error')
    
    if current_user.account_type == 'Administrator':
        comments = Comment.query.filter_by(ticket_id=ticket.id).order_by(Comment.date_created.asc()).all()
    else:
        comments = Comment.query.filter_by(ticket_id=ticket.id, user_id=current_user.id).order_by(Comment.date_created.asc()).all()

    return render_template('ticket_details.html', ticket=ticket, comments=comments, admin_users=admin_users)

@tickets_bp.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('home.home'))

    if current_user.account_type != 'Administrator':
        flash('You do not have permission to delete this ticket.', category='error')
        return redirect(url_for('tickets.ticket_details', ticket_id=ticket.id))
    
    db.session.query(Comment).filter_by(ticket_id=ticket.id).delete()
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully.', category='success')
    return redirect(url_for('home.home'))