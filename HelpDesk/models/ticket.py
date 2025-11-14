from ..extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(500), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    estimated_time = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    updated_by = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
    date_updated = db.Column(db.DateTime(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)