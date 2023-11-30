from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileAllowed


class CreatePost(FlaskForm):
    title = StringField('Title:',
                        validators=[DataRequired("This field is required.")],
                        render_kw={"class": "form-control"})
    text = TextAreaField('Write your post:', 
                         validators=[DataRequired("This field is required.")],
                         render_kw={"class": "form-control"})
    type = SelectField("Post type:", 
                       validators=[DataRequired("Select a type.")],
                       choices=[("news", "News"), ("publication", "Publication"), ("other", "Other")],
                       render_kw={"class": "form-control", "multiple": True})
    image_file = FileField('Add image:', 
                           validators=[FileAllowed(['jpg', 'png'])],
                           render_kw={"class": "form-control"})
    submit = SubmitField('Create',
                         render_kw={"class": "btn btn-primary"})  
    