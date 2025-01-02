from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configure the database URI, you need to set DATABASE_URL as an environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # or replace with your PostgreSQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable a feature not needed

db = SQLAlchemy(app)

class Blogpost(db.Model):
    __tablename__ = 'blogpost'  # Specify the table name here

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
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

    if post:
        db.session.delete(post)
        db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create the database schema
    with app.app_context():
        db.create_all()  # Create all tables if they don't exist
        print("Database schema created.")
    app.run(debug=True)
