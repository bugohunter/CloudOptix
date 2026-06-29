from flask import render_template
from flask_login import login_required, current_user
from . import dashboard


@dashboard.route("/dashboard")
@login_required
def home():

    return render_template(
        "dashboard/dashboard.html",
        user=current_user
    )