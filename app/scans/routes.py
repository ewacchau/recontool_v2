from flask import render_template, redirect, url_for, flash
from . import scans_bp
from .forms import ScanForm
from ..extensions import db, limiter
from ..models import ScanRun
from ..tasks import run_full_scan

@scans_bp.route("/", methods=["GET", "POST"])
@limiter.limit("10/minute")
def index():
    form = ScanForm()
    if form.validate_on_submit():
        scan = ScanRun(domain=form.domain.data, target=form.target.data or None)
        db.session.add(scan)
        db.session.commit()
        run_full_scan.delay(scan.id)
        flash("Scan queued!", "success")
        return redirect(url_for("scans.status", scan_id=scan.id))
    return render_template("index.html", form=form)

@scans_bp.route("/status/<int:scan_id>")
def status(scan_id):
    scan = ScanRun.query.get_or_404(scan_id)
    return render_template("status.html", scan=scan)

@scans_bp.route("/results/<int:scan_id>")
def results(scan_id):
    scan = ScanRun.query.get_or_404(scan_id)
    if scan.status != "finished":
        return redirect(url_for("scans.status", scan_id=scan.id))
    return render_template("results.html", scan=scan)
