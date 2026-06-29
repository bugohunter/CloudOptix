from flask import render_template
from flask_login import login_required
from . import uploads


@uploads.route("/uploads")
@login_required
def upload():

    return render_template(
        "uploads/upload.html"
    )