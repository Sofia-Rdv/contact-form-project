from flask import render_template, request, flash, redirect, url_for
from app import app
import re


def is_valid_email(email):
    # простая проверка формата email регулярным выражением
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex,email)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        # Получаем имя из формы
        name = request.form.get("name")
        # Получаем email из формы
        email = request.form.get("email")
        # Получаем текст сообщения из формы
        message = request.form.get("message")

        # Валидация
        if not name or name.strip() == "" or not email or not message:
            flash("Пожалуйста, заполните все поля!", "error")
        elif not is_valid_email(email):
            flash("Некорректный формат email!", "error")
        else:
            flash(f"Спасибо, {name}! Ваше сообщение успешно отправлено.", "success")
            return redirect(url_for("contact"))

    return render_template("contact.html")