from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField, URLField    
from wtforms.validators import DataRequired, Length
 

class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1 , max=20)])
    image = URLField("Image URL", validators=[DataRequired(), Length(min=5, max=255)])    
    description= StringField("Description", validators=[DataRequired(), Length(min=2, max=200)])
    publish_date = DateField("Publish Date", format='%Y-%m-%d', validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    appropriateness = SelectField("Appropriateness", choices=["Under 8", "8-15", "Adults"], validators=[DataRequired()])
    author_id = SelectField("Author", coerce=int, validators=[DataRequired()]) #drop down
    submit = SubmitField("Add Book")    
 
class AuthorForm(FlaskForm):
    Name= StringField("Author_Name", validators=[DataRequired(), Length(min=2)])
    submit = SubmitField("Add Author")


