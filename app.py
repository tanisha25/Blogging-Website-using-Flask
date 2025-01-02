from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# PostgreSQL configuration using environment variables
DB_SERVER = os.getenv('DB_SERVER')  # e.g., your-db-instance.xxxxxxx.us-west-2.rds.amazonaws.com
DB_NAME = os.getenv('DB_NAME')  # e.g., your_database_name
DB_USER = os.getenv('DB_USER')  # e.g., your_db_user
DB_PASSWORD = os.getenv('DB_PASSWORD')  # e.g., your_db_password

# Update to PostgreSQL URL
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
db = SQLAlchemy(app)

class Blogpost(db.Model):
    __tablename__ = 'blogpost'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/delete')
def delete():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('delete.html', posts=posts)

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletepost', methods=['POST'])
def deletepost():
    post_id = request.form.get("post_id")

    post = Blogpost.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index'))

# Instead of using before_first_request, create the tables directly here
with app.app_context():
    db.create_all()  # Creates tables if they do not exist

if __name__ == '__main__':
    app.run(debug=True)
