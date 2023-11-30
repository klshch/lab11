#!/usr/bin/python3

from flask import flash, redirect, render_template, url_for, request

from app import db
from .models import Feedback
from .forms import FeedbackForm

from . import control

@control.route('/reviews', methods=["GET", "POST"])
def reviews():
    
    reviews = FeedbackForm()

    if request.method == 'POST' and reviews.validate_on_submit():
        name = reviews.name.data
        content = reviews.content.data
        feedback_entry = Feedback(name=name, content=content)
        db.session.add(feedback_entry)
        db.session.commit()
        flash('Ваш відгук було успішно збережено', 'success')
        return redirect(url_for('control.reviews'))

    feedback_entries = Feedback.query.all() 

    return render_template('reviews.html', reviews=reviews, feedback_entries=feedback_entries)

