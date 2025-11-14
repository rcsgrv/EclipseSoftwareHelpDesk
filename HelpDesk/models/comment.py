from datetime import datetime
from ..extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text(500), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
    author_fullname = db.Column(db.String(100), nullable=False)
    
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id', ondelete='SET NULL'), nullable=True)
    ticket = relationship('ticket', backref='ticket_comments')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)