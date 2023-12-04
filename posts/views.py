from flask import flash, redirect, render_template, url_for, make_response, request
from flask_login import current_user, login_required

from app import db
from .models import Post

from .forms import CreatePost
from .forms import EditPostForm

from .saver import save_picture

from . import posts


@posts.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePost()

    image_file = None

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


@posts.route("/post/<int:id>/edit", methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    form = EditPostForm() 

    if form.validate_on_submit():
        if form.title.data != post.title or form.text.data != post.text or form.type.data != post.type:
            post.title = form.title.data
            post.text = form.text.data
            post.type = form.type.data
            db.session.commit()

            flash("Post has been updated", "success")
            return redirect(url_for('posts.post', id=post.id))
        
        if form.image_file.data:
            post.image_file = save_picture(form.image_file.data)
            db.session.commit()

            flash("Post has been updated", "success")
            return redirect(url_for('posts.post', id=post.id))
        
        else:
            flash('No changes were made to your post.', 'info')
            return redirect(url_for('posts.post', id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
        form.type.data = post.type

    return render_template('edit.html', post=post, form=form)


@posts.route("/post/<int:id>/delete")
def delete(id):
    post = Post.query.filter_by(id=id).first_or_404()
        
    db.session.delete(post)
    db.session.commit()
    flash("Post has been deleted", "success")
    return redirect(url_for('posts.all_posts'))

