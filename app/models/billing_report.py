from datetime import datetime
from app import db


class BillingReport(db.Model):

    __tablename__ = "billing_reports"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(255), nullable=False)

    total_cost = db.Column(db.Float, nullable=False)

    total_services = db.Column(db.Integer, nullable=False)

    highest_service = db.Column(db.String(100), nullable=False)

    highest_cost = db.Column(db.Float, nullable=False)

    average_cost = db.Column(db.Float, nullable=False)

    estimated_savings = db.Column(db.Float, nullable=False)

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )