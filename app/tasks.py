import datetime, shodan
from .extensions import celery, db
from .models import ScanRun
from .utils import run_cmd
from flask import current_app

@celery.task(bind=True)
def run_full_scan(self, scan_id: int):
    scan = ScanRun.query.get(scan_id)
    if not scan: return
    scan.status = "running"
    db.session.commit()

    results = {}
    domain = scan.domain
    target = scan.target

    results["sublist3r"] = run_cmd(["sublist3r", "-d", domain, "-o", "-"], timeout=300)
    results["amass"] = run_cmd(["amass", "enum", "-d", domain, "-json", "-"], timeout=600)
    results["theHarvester"] = run_cmd(["theHarvester", "-d", domain, "-b", "all"], timeout=300)

    if target:
        results["nmap"] = run_cmd(["nmap", "-sV", "-T4", "-oX", "-", target], timeout=600)

    api_key = current_app.config.get("SHODAN_API_KEY")
    if api_key and target:
        try:
            api = shodan.Shodan(api_key)
            results["shodan"] = api.host(target)
        except shodan.APIError as e:
            results["shodan_error"] = str(e)

    scan.result = results
    scan.status = "finished"
    scan.finished_at = datetime.datetime.utcnow()
    db.session.commit()
    return "completed"
