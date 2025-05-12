from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, IPAddress, Regexp

class ScanForm(FlaskForm):
    domain  = StringField("Domain", validators=[DataRequired(), Regexp(r"^[A-Za-z0-9.-]+$", message="Invalid domain")])
    target  = StringField("Target IP (optional)", validators=[Optional(), IPAddress()])
    submit  = SubmitField("Start Scan")
