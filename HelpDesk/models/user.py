from ..extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    agency = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20))
    account_type = db.Column(db.String(20), nullable=False)
    totp_secret = db.Column(db.String(16))
    is_2fa_enabled = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
    
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id', ondelete='SET NULL'), nullable=True)

    agency = db.relationship('Agency', back_populates='users')
    assigned_tickets = relationship('Ticket', backref='assignee', foreign_keys='Ticket.assignee_id')
    tickets = relationship('Ticket', backref='user', foreign_keys='Ticket.user_id')
    user_comments = relationship('Comment', backref='user', foreign_keys='Comment.user_id')