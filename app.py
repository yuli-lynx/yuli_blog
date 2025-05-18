from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__, instance_relative_config=True)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'static',
    'uploads'
)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'blog.db')
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    hashtags = db.Column(db.String(200))
    image_filename = db.Column(db.String(100))

def delete_image_file(filename):
    """
    Remove an image file from disk if it exists.
    """
    if not filename:
        return
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

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
        
        image = request.files.get("image")
        filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # pillow resize
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = Image.open(img_path)
            img.thumbnail((800, 800))
            img.save(img_path)

        new_post = BlogPost(
            title=title,
            content=content,
            hashtags=hashtags,
            image_filename=filename
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    
    return render_template("create.html")

@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    admin_password = "Password5813!"
    post = BlogPost.query.get_or_404(post_id)

    if request.method == "POST":
        if request.form.get("password") != admin_password:
            flash("!wrongue passwordue!")
            return redirect(url_for("edit_post", post_id=post.id))

        post.title = request.form["title"]
        post.content = request.form["content"]
        post.hashtags = request.form.get("hashtags")

        image = request.files.get("image")
        if image and image.filename:
            delete_image_file(post.image_filename)

            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            with Image.open(image_path) as img:
                img.thumbnail((800, 800))
                img.save(image_path)

            post.image_filename = filename
        
        db.session.commit()
        return redirect(url_for("post", post_id=post.id))
    
    return render_template("edit.html", post=post)

@app.route("/post/<int:post_id>/delete>", methods=["POST"])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    delete_image_file(post.image_filename)

    db.session.delete(post)
    db.session.commit()

    flash("postue deletede!!")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)