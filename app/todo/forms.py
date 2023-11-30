from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    title = StringField("Enter a task here: ", 
                         validators=[DataRequired("This field is required.")],
                         render_kw={"class": "form-control me-sm-2"})
    submit_todo = SubmitField("Save",
                         render_kw={"class": "btn btn-primary my-2 my-sm-0"})
    