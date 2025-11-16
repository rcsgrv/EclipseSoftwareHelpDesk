# This function validates all fields on the edit ticket page and the create ticket page (create_ticket.html and edit_ticket.html).

def validate_ticket_form(subject, description, status, priority, estimated_time):
    if not subject or len(subject.strip()) < 1:
        return 'Subject cannot be blank.'
    if len(subject) > 100:
        return 'Subject must not exceed 100 characters.'
    if not description or len(description.strip()) < 1:
        return 'Description cannot be blank.'
    if len(description) > 500:
        return 'Description must not exceed 500 characters.'
    if not status:
        return 'You must select a status.'
    if not priority:
        return 'You must select a priority.'
    try:
        estimated_time_val = float(estimated_time)

        if estimated_time_val < 1:
            return 'Estimated time cannot be less than 1 hour.'
        if estimated_time_val > 40:
            return 'Estimated time cannot be more than 40 hours.'
        if '.' in str(estimated_time):
            decimal_part = str(estimated_time).split('.')[-1]
            if len(decimal_part) > 2:
                return 'Estimated time cannot have more than 2 decimal places.'
            
    except (ValueError, TypeError):
        return 'Estimated time must be a valid number.'
    return None 

def render_ticket_form(template, error, **context):
    from flask import flash, render_template
    flash(error, category='error')
    return render_template(template, **context)