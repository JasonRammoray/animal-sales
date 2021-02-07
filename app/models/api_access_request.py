from datetime import datetime

from app import db


class ApiAccessRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    center_id = db.Column(
        db.Integer,
        db.ForeignKey('animal_center.id', ondelete='CASCADE'),
        nullable=False
    )
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
