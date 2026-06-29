from io import BytesIO

from flask import send_file, redirect, url_for
from flask_login import login_required, current_user

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from . import reports
from app.models.billing_report import BillingReport
from app import db


# ======================================================
# DOWNLOAD PDF REPORT
# ======================================================

@reports.route("/download-report")
@login_required
def download_report():

    report = (
        BillingReport.query
        .filter_by(user_id=current_user.id)
        .order_by(BillingReport.uploaded_at.desc())
        .first()
    )

    if not report:
        return redirect(url_for("dashboard.dashboard_home"))

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>CloudOptix AI Executive Report</b>", styles["Title"])
    )

    story.append(
        Paragraph(f"User: {current_user.full_name}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Total Cloud Cost: ₹{report.total_cost}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Highest Service: {report.highest_service}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Highest Cost: ₹{report.highest_cost}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Average Cost: ₹{report.average_cost}", styles["Normal"])
    )

    story.append(
        Paragraph(
            f"Estimated Savings: ₹{report.estimated_savings}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph("<br/><b>AI Recommendation</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"""
            {report.highest_service} is currently your highest
            cloud expenditure.

            Recommended Actions:

            • Use Reserved Instances

            • Enable Auto Scaling

            • Remove idle resources

            • Monitor cloud usage regularly

            Estimated Monthly Savings:
            ₹{report.estimated_savings}
            """,
            styles["Normal"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="CloudOptix_Report.pdf",
        mimetype="application/pdf"
    )


# ======================================================
# DELETE REPORT
# ======================================================

@reports.route("/delete-report/<int:report_id>")
@login_required
def delete_report(report_id):

    report = BillingReport.query.filter_by(
        id=report_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(report)
    db.session.commit()

    return redirect(url_for("dashboard.dashboard_home"))