from flask import Flask, render_template, request, redirect, flash, url_for
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

@app.route("/post/<int:post_id>")
def post(post_id):
    blog_post = BlogPost.query.get_or_404(post_id)
    return render_template("post.html", post=blog_post)

@app.route("/create", methods=["GET", "POST"])
def create_post():
    admin_password = "Password5813!"

    if request.method == "POST":
        if request.form.get("password") != admin_password:
            flash("!!!wrongue passwordue!!!")
            return redirect(url_for("create_post"))
        
        title = request.form["title"]
        content = request.form["content"]
        hashtags = request.form.get("hashtags")

        if not title or not content:
            flash("no no no, titullo und contento should be presento!!!")
            return redirect(url_for("create_post"))
        
        new_post = BlogPost(title=title, content=content, hashtags=hashtags)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    
    return render_template("create.html")

@app.route("/test-base")
def test_base():
    return render_template("test_base.html")

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    hashtags = db.Column(db.String(200))

if __name__ == "__main__":
    app.run(debug=True)