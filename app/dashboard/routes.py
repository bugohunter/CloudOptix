from flask import render_template
from flask import render_template
from flask_login import login_required, current_user

from . import dashboard
from app.models.billing_report import BillingReport
from app.services.gemini_service import GeminiService


@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    latest_report = (
        BillingReport.query
        .filter_by(user_id=current_user.id)
        .order_by(BillingReport.uploaded_at.desc())
        .first()
    )

    reports = (
        BillingReport.query
        .filter_by(user_id=current_user.id)
        .order_by(BillingReport.uploaded_at.desc())
        .all()
    )

    report_count = (
        BillingReport.query
        .filter_by(user_id=current_user.id)
        .count()
    )

    all_reports = BillingReport.query.filter_by(
        user_id=current_user.id
    ).all()

    lifetime_cost = sum(r.total_cost for r in all_reports)

    average_cost = (
        round(lifetime_cost / report_count, 2)
        if report_count else 0
    )

    last_upload = (
        latest_report.uploaded_at.strftime("%d %b %Y")
        if latest_report else "N/A"
    )

    chart_labels = []
    chart_values = []

    if latest_report:
        chart_labels = [latest_report.highest_service]
        chart_values = [latest_report.highest_cost]

    # -----------------------------
    # Gemini AI Recommendation
    # -----------------------------

    ai_recommendation = ""

    if latest_report:

        try:

            ai_recommendation = GeminiService.generate_recommendation(
                latest_report
            )

        except Exception as e:

            print(e)

            ai_recommendation = (
                "AI recommendation is temporarily unavailable."
            )

    return render_template(
        "dashboard/dashboard.html",
        user=current_user,
        report=latest_report,
        reports=reports,
        report_count=report_count,
        chart_labels=chart_labels,
        chart_values=chart_values,
        lifetime_cost=lifetime_cost,
        average_monthly_cost=average_cost,
        last_upload=last_upload,
        ai_recommendation=ai_recommendation
    )