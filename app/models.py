from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hashed = db.Column(db.String(60), nullable=False)
   
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hashed = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hashed, password)
    def save_to_db(self):
        db.session.add(self)            
        db.session.commit()
class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    books = db.relationship('Book', backref='author', lazy=True)
    def save_to_db(self):
        db.session.add(self)            
        db.session.commit()
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)   
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    price = db.Column(db.Float, nullable=False)
    appropriate = db.Column(db.String(20), nullable=False)
    def save_to_db(self):
        db.session.add(self)            
        db.session.commit()

@login_manager.user_loader #decorator
def load_user(user_id):
    return User.query.get(int(user_id))

