from flask_login import login_required, logout_user
from app.models import Book , Author
from app import db
from app.main.forms import AuthorForm, BookForm
from flask import redirect , url_for
from flask import Blueprint
from flask import render_template

main_blueprint = Blueprint('main', __name__ , url_prefix='/') # any thing defined under blueprint will be prefixed with /

@main_blueprint.route('' , endpoint='home')
@login_required
def index():
    books = Book.query.all()
    return render_template('home.html', books=books)

@main_blueprint.route('/addbooks' , endpoint="add_books" , methods=['GET' , 'POST'])
@login_required
def add_book():
    form = BookForm() #book from 
    authors = Author.query.all()
    if not authors :
        return redirect(url_for('main.add_author'))
    form.author_id.choices = [
         (author.id , author.name)
         for author in authors 
    ]
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            image = form.image.data,
            description = form.description.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            appropriate=form.appropriateness.data,
            author_id=form.author_id.data
        )
        book.save_to_db()
        return redirect(url_for('main.home'))
    return render_template('add_book.html' ,form = form)
@main_blueprint.route('/add_author',methods=['GET' , 'POST'])
@login_required
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author( name = form.Name.data)
        author.save_to_db()
        return redirect(url_for('main.author_details' ,id=author.id  ))
    return render_template('add_author.html', form = form)
@main_blueprint.route('/authors' , endpoint='all_authors')
@login_required
def all_authors():
     authors = Author.query.all()
     return render_template('authors.html', authors= authors )
@main_blueprint.route('/author_details/<int:id>' , endpoint="author_details" ,methods=['GET' ])
@login_required
def author_details(id):
        
        author = Author.query.get(id)
        if author :
             
             return render_template('author_details.html' , author = author  )
        return render_template ("404.html"), 404
@main_blueprint.route('/book/<int:id>',endpoint='book_detail' , methods=["GET"] )
@login_required
def book_detail(id):
        book = Book.query.get(id)
        if book:
             author = book.author
             return render_template('book_details.html', book=book , author=author)
        return render_template ("404.html"), 404
@main_blueprint.route('/delete_book/<int:id>', endpoint='delete_book')
@login_required
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template ("404.html"), 404
@main_blueprint.route('/delete_author/<int:id>', endpoint='delete_author')
@login_required
def delete_author(id):
    author = Author.query.get(id)
    if author:
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for('main.all_authors'))
    return render_template ("404.html"), 404


@main_blueprint.route('/edit_book/<int:id>', endpoint='edit_book', methods=['GET', 'POST'])
@login_required
def edit_book(id):        
    book = Book.query.get(id)
    form = BookForm(obj=book)
    authors = Author.query.all()
    if not authors :
        return redirect(url_for('main.add_author')) 
    form.author_id.choices = [
         (author.id , author.name)
         for author in authors
    ]   
    if form.validate_on_submit():
        book.title = form.title.data
        book.image = form.image.data
        book.description = form.description.data
        book.publish_date = form.publish_date.data
        book.price = form.price.data
        book.appropriate = form.appropriateness.data
        book.author_id = form.author_id.data
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('add_book.html', form=form)
@main_blueprint.route('/edit_author/<int:id>', endpoint='edit_author', methods=['GET', 'POST'])
@login_required
def edit_author(id):
    author = Author.query.get(id)
    form = AuthorForm(obj=author)
    if form.validate_on_submit():
        author.name = form.Name.data
        db.session.commit()
        return redirect(url_for('main.all_authors'))
    return render_template('edit_author.html', form=form)

@main_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template ('404.html')
@main_blueprint.errorhandler(500)
def page_not_found(e):
    return render_template ('500.html')

@main_blueprint.route('/logout' , endpoint='logout', methods=['GET', 'POST']) 
def logout():
    logout_user()
    return redirect(url_for('logib'))