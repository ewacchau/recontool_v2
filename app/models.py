from datetime import datetime
from .extensions import db

class ScanRun(db.Model):
    __tablename__ = "scan_runs"
    id          = db.Column(db.Integer, primary_key=True)
    domain      = db.Column(db.String(255), nullable=False)
    target      = db.Column(db.String(255), nullable=True)
    status      = db.Column(db.String(32), default="pending")
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime)
    result      = db.Column(db.JSON)
