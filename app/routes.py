from flask import render_template, request, flash, redirect, url_for
from app import app
import re
import logging

logger = logging.getLogger("my_app")


def is_valid_email(email):
    # простая проверка формата email регулярным выражением
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    logger.info("Проверка формата email завершена.")
    return re.match(regex,email)


@app.route('/')
def index():
    """
    Отображает главную страницу с формой для заполнения.

    :return: str: Отрендеренный HTML-шаблон 'index.html.'
    """
    logger.info("Пользователь зашел на главную страницу")
    return render_template('index.html')


@app.route('/about')
def about():
    """
    Отображает страницу с информацией о проекте.

    :return: str: Отрендеренный HTML-шаблон 'about.html.'
    """
    logger.info("Пользователь зашел на страницу 'О нас'(about).")
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Обрабатывает страницу контактов и отправку формы обратной связи.

    При GET-запросе: Возвращает страницу с пустой формой.
    При POST-запросе: Собирает данные из формы, валидирует их (проверка на пустоту и корректность email).
    В случае успеха перенаправляет на ту же страницу с уведомлением, в случае ошибки - выводит предупреждение.

    :return: str: Отрендеренный HTML-шаблон 'contact.html' или перенаправление.
    """
    if request.method == "POST":
        # Получаем имя из формы
        name = request.form.get("name")
        # Получаем email из формы
        email = request.form.get("email")
        # Получаем текст сообщения из формы
        message = request.form.get("message")

        # Валидация
        if not name or name.strip() == "" or not email or not message:
            logger.warning("Пользователь не заполнил все обязательные поля.")
            flash("Пожалуйста, заполните все поля!", "error")
        elif not is_valid_email(email):
            logger.warning(f'Некорректные данные эл. почты: {email}')
            flash("Некорректный формат email!", "error")
        else:
            flash(f"Спасибо, {name}! Ваше сообщение успешно отправлено.", "success")
            logger.info(f"Сообщение {name} {email} успешно принято.")
            return redirect(url_for("contact"))

    return render_template("contact.html")


@app.errorhandler(404)
def page_for_found(e):
    """
    Обработчик ошибки 404 (Страница не найдена).

    Логирует путь, по которому пытался перейти пользователь,
    и выводит страницу ошибки.

    :param e: Exception: Объект ошибки.
    :return: tuple: Шаблон ошибки и HTTP-статус 404.
    """
    logger.error(f"Ошибка 404: Пользователь пытался перейти на {request.path}")
    return render_template("error.html", message="Упс! Страница потерялась в космосе."), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    Обработчик ошибки 500 (Внутренняя ошибка сервера).

    Логирует критическую ошибку с полной трассировкой стека (traceback)
    и выводит страницу ошибки.

    :param e: Exception: Объект ошибки.
    :return: tuple: Шаблон ошибки и HTTP-статус 500.
    """
    logger.critical(f"ОШИБКА 500: {str(e)}", exc_info=True)
    return render_template("error.html", message="Наш сервер приуныл."), 500
