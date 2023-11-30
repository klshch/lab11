#!/usr/bin/python3

from flask import flash, redirect, render_template, url_for, make_response, request, session

import os
import json

from .forms import LoginForm
from .forms import ChangePassword

from . import cookies


json_file_path = os.path.join(os.path.dirname(__file__), '../static', 'json', 'users.json')
with open(json_file_path, 'r') as users_file:
    users = json.load(users_file)

@cookies.route('/form', methods=["GET", "POST"])
def form():
    
    form = LoginForm()  

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        if name in users and users[name] == password:
            if form.remember.data == True:
                flash("Вхід виконано. Інформація збережена.", category="success")
                session["username"] = name

                return redirect(url_for("cookies.info"))
                
            else:
                flash("Вхід виконано. Інформація не збережена", category="success")

                return redirect(url_for("portfolio.home"))

        else:
            flash("Вхід не виконано", category="warning")
            return redirect(url_for("cookies.form"))

    return render_template('form.html', form=form)



@cookies.route('/info', methods=["GET", "POST"])
def info():

    form = ChangePassword()

    if session.get("username"):
        cookies = get_cookies_data()
        if request.method == "POST":
 
            cookie_key = request.form.get("cookie_key")
            cookie_value = request.form.get("cookie_value")
            cookie_expiry = request.form.get("cookie_expiry")
            delete_cookie_key = request.form.get("delete_cookie_key")

            if cookie_key and cookie_value and cookie_expiry:
                add_cookie(cookie_key, cookie_value, int(cookie_expiry))
            if delete_cookie_key:
                delete_cookie(delete_cookie_key)

            cookies = get_cookies_data()  
        return render_template('info.html', cookies=cookies, form=form)
    else:
        return redirect(url_for('cookies.form'))


def get_cookies_data():
    cookies = []
    for key, value in request.cookies.items():
        expiry = request.cookies.get(key + "_expires")
        created = request.cookies.get(key + "_created")

        cookies.append((key, value, expiry, created))
    return cookies

@cookies.route('/clear_session', methods=["GET"])
def clear_session():
    session.pop("username", None)
    return redirect(url_for("cookies.form"))

@cookies.route('/add_cookie', methods=["POST"])
def add_cookie():
    if session.get("username"):
        cookie_key = request.form.get("cookie_key")
        cookie_value = request.form.get("cookie_value")
        cookie_expiry = request.form.get("cookie_expiry")

        response = make_response(redirect(url_for("cookies.info")))
        response.set_cookie(cookie_key, cookie_value, max_age=int(cookie_expiry) * 3600) 
        flash("Куки додано.", category="success")
        return response
    else:
        return redirect(url_for('cookies.form'))

@cookies.route('/delete_cookie', methods=["POST"])
def delete_cookie():
    if session.get("username"):
        cookie_key_to_delete = request.form.get("cookie_key_to_delete")
        response = make_response(redirect(url_for("cookies.info")))
        response.delete_cookie(cookie_key_to_delete)
        flash("Куки видалено.", category="success")
        return response
    else:
        return redirect(url_for('cookies.form'))

@cookies.route('/delete_all_cookies', methods=["POST"])
def delete_all_cookies():
    if session.get("username"):
        response = make_response(redirect(url_for("cookies.info")))
        for key in request.cookies:
            response.delete_cookie(key)
        flash("Куки видалено.", category="success")
        return response
    else:
        flash("Куки не видалено.", category="warning")
        return redirect(url_for('cookies.form'))


@cookies.route('/change_password', methods=["POST"])
def change_password():

    form = ChangePassword()

    if form.validate_on_submit():

        if session.get("username"):
            current_password = form.current_password.data
            new_password = form.new_password.data
            username = session["username"]

            json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'json', 'users.json')

            with open(json_file_path, 'r') as users_file:
                users = json.load(users_file)

            if users.get(username) == current_password:
                users[username] = new_password

                with open(json_file_path, 'w') as users_file:
                    json.dump(users, users_file)

                flash("Пароль змінено.", category="success")
                
                return redirect(url_for("cookies.info"))
            
            else:
                flash("Пароль не змінено.", category="warning")

                return redirect(url_for("cookies.info"))
        
        else:
            return redirect(url_for('cookies.form'))
        
    return render_template('info.html', form=form)
