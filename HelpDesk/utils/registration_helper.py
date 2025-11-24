from email_validator import validate_email, EmailNotValidError
import re

# This function validates all fields on the registration page (register.html).
# Regex patterns were adapted from: https://stackoverflow.com/questions/2049502/regex-for-first-and-last-name
# An upper limit of 50 characters for forename and surname was chosen to accommodate longer names while preventing excessively long inputs. 
# I was advised to not put an upper limit on these fields by the lead developer at Eclipse Software. 
# However, for practical purposes and database constraints, a limit is necessary.

name_regex = re.compile(r"^[A-Za-z][A-Za-z\s'-]*$")
password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$")

def validate_registration_form(forename, surname, email, password, password_confirm, user):
    if not forename or len(forename.strip()) < 1:
        return 'Forename cannot be blank.'
    if len(forename.strip()) > 50:
        return 'Forename cannot exceed 50 characters.'
    if not name_regex.fullmatch(forename.strip()):
        return 'Forename can only contain letters, spaces, hyphens or apostrophes.'
    if not surname or len(surname.strip()) < 1:
        return 'Surname cannot be blank.'
    if len(surname.strip()) > 50:
        return 'Surname cannot exceed 50 characters.'
    if not name_regex.fullmatch(surname.strip()):
        return 'Surname can only contain letters, spaces, hyphens or apostrophes.'
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
    if len(password.strip()) > 16:
        return 'Password cannot exceed 16 characters.'
    if not password_regex.fullmatch(password):
        return 'Password must include at least one uppercase letter, one lowercase letter, one number, and one special character (@$!%*#?&).'
    if password != password_confirm:
        return 'Your passwords do not match.'
    return None