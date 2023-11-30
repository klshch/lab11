from flask import flash, redirect, render_template, url_for

from app import db
from .models import Todo
from .forms import TodoForm

from . import todo

@todo.route('/todo', methods=['GET', 'POST'])
def todos():

    form = TodoForm()

    todo_list = Todo.query.all()

    return render_template("todo.html", form=form, todo_list=todo_list)


@todo.route('/add', methods=["POST"])
def add():

    form = TodoForm()

    if form.validate_on_submit():
        title = form.title.data
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()

        flash('Додано.', 'success')
    else:
        flash('Не додано.', 'danger')

    return redirect(url_for("todo.todos"))


@todo.route('/update/<int:todo_id>')
def update(todo_id):

    todo = db.get_or_404(Todo, todo_id)
    todo.complete = not todo.complete
    db.session.commit()

    flash('Оновлено.', 'success')

    return redirect(url_for('todo.todos'))


@todo.route('/delete/<int:todo_id>')
def delete(todo_id):

    todo = db.get_or_404(Todo, todo_id)
    db.session.delete(todo)
    db.session.commit()

    flash('Видалено.', 'success')

    return redirect(url_for('todo.todos'))

