from ..extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    totp_secret = db.Column(db.String(64))
    is_2fa_enabled = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())

    assigned_tickets = relationship('Ticket', backref='assignee', foreign_keys='Ticket.assignee_id')
    tickets = relationship('Ticket', backref='user', foreign_keys='Ticket.user_id')
    user_comments = relationship('Comment', backref='user', foreign_keys='Comment.user_id')