from email_validator import validate_email, EmailNotValidError
import re

# This function validates all fields on the registration page (register.html).

name_regex = re.compile(r"^[A-Za-z][A-Za-z\s'-]*$")

def validate_registration_form(forename, surname, email, password, password_confirm, account_type, user):
    if not forename or len(forename.strip()) < 1:
        return 'Forename cannot be blank.'
    if not name_regex.fullmatch(forename.strip()):
        return 'Forename can only contain letters, spaces, hyphens or apostrophes.'
    if len(forename.strip()) > 50:
        return 'Forename cannot exceed 25 characters.'
    if not surname or len(surname.strip()) < 1:
        return 'Surname cannot be blank.'
    if not name_regex.fullmatch(surname.strip()):
        return 'Surname can only contain letters, spaces, hyphens or apostrophes.'
    if len(surname.strip()) > 50:
        return 'Surname cannot exceed 50 characters.'
    if not email or len(email.strip()) < 1:
        return 'Email cannot be blank.'
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        return str(e)
    if user is not None:
        return 'The email you have provided is already associated with an account.'
    if not password or len(password) < 8:
        return 'Password must be at least 8 characters long.'
    if len(password.strip()) > 20:
        return 'Password cannot exceed 20 characters.'
    if password != password_confirm:
        return 'Your passwords do not match.'
    if not account_type:
        return 'You must select an account type.'
    if account_type not in ('Customer Account', 'Eclipse Staff Account'):
        return 'Invalid account type selected.'
    return None