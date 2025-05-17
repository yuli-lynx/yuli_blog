from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__, instance_relative_config=True)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'blog.db')
db = SQLAlchemy(app)

@app.route("/")
def home():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    hashtags = db.Column(db.String(200))

if __name__ == "__main__":
    app.run(debug=True)