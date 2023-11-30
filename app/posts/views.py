from flask import flash, redirect, render_template, url_for, make_response, request
from flask_login import current_user, login_required

from app import db
from .models import Post

from .forms import CreatePost

from .saver import save_picture

from . import posts


@posts.route("/create", methods=['GET', 'POST'])
@login_required
def create():

    form = CreatePost()

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        type = form.type.data
        user_id = current_user.id
 
        if form.image_file.data:
            image_file = save_picture(form.image_file.data)

        post = Post(title=title, text=text, image_file=image_file, type=type, user_id=user_id)

        db.session.add(post)
        db.session.commit()

        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.create'))
        

    return render_template('new_post.html', form=form)


@posts.route('/post', methods=['GET'])
def all_posts():
    posts = Post.query.filter_by(enabled=True).all()

    return render_template('all_posts.html', posts=posts)


@posts.route("/post/<int:id>")
def post(id):
    post = Post.query.filter_by(id=id).first_or_404()

    return render_template("post.html", post=post, current_user=current_user)