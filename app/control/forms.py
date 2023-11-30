from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    name = StringField("Username:", 
                           validators=[DataRequired("Це поле обовʼязкове")],
                           render_kw={"class": "form-control"})
    content = TextAreaField("Responde:", 
                           validators=[DataRequired("Це поле обовʼязкове")],
                           render_kw={"class": "form-control"})
    submit_feedback = SubmitField("Confirm", 
                         render_kw={"class": "btn btn-primary"})