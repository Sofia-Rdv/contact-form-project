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


@app.errorhandler(404)
def page_for_found(e):
    """
    Обработчик ошибки 404 (Страница не найдена).

    Логирует путь, по которому пытался перейти пользователь,
    и выводит кастомную страницу ошибки.

    :param e: Exception: Объект ошибки.
    :return: tuple: Шаблон ошибки и HTTP-статус 404.
    """
    #logger.error(f"Ошибка 404: Пользователь пытался перейти на {request.path}")
    return render_template("error.html", message="Упс! Страница потерялась в космосе."), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    Обработчик ошибки 500 (Внутренняя ошибка сервера).

    Логирует критическую ошибку с полной трассировкой стека (traceback)
    и выводит кастомную страницу ошибки.

    :param e: Exception: Объект ошибки.
    :return: tuple: Шаблон ошибки и HTTP-статус 500.
    """
    #logger.critical(f"ОШИБКА 500: {str(e)}", exc_info=True)
    return render_template("error.html", message="Наш сервер приуныл.")