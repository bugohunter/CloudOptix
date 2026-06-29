from app import db


class BillingItem(db.Model):

    __tablename__ = "billing_items"

    id = db.Column(db.Integer, primary_key=True)

    service = db.Column(db.String(100), nullable=False)

    region = db.Column(db.String(100), nullable=False)

    cost = db.Column(db.Float, nullable=False)

    report_id = db.Column(
        db.Integer,
        db.ForeignKey("billing_reports.id"),
        nullable=False
    )