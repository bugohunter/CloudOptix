import os
import pandas as pd

from flask import (
    render_template,
    request,
    flash,
    current_app
)

from flask_login import current_user
from app import db
from app.models.billing_report import BillingReport
from app.services.analytics_service import AnalyticsService
from flask_login import login_required
from werkzeug.utils import secure_filename

from . import uploads


@uploads.route("/uploads", methods=["GET", "POST"])
@login_required
def upload():

    table = None

    if request.method == "POST":

        file = request.files.get("billing_file")

        if file and file.filename.endswith(".csv"):

            filename = secure_filename(file.filename)

            upload_folder = os.path.join(
                current_app.root_path,
                "..",
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)

            file.save(filepath)

            flash("CSV uploaded successfully!", "success")

            summary = AnalyticsService.analyze_csv(filepath)
            report = BillingReport(
                filename=filename,
                total_cost=summary["total_cost"],
                total_services=summary["total_services"],
                highest_service=summary["highest_service"],
                highest_cost=summary["highest_cost"],
                average_cost=summary["average_cost"],
                estimated_savings=summary["estimated_savings"],
                user_id=current_user.id
            )

            db.session.add(report)
            db.session.commit()
            
            print(summary)

            df = pd.read_csv(filepath)

            table = df.head(10).to_html(
                classes="table table-bordered table-striped",
                index=False
            )

        else:

            flash("Please upload a valid CSV file.", "danger")

    return render_template(
        "uploads/upload.html",
        table=table
    )