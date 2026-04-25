import pytest
from app import app
from app.routes import is_valid_email # Импортируем функцию валидации для тестов


@pytest.fixture
def client():
    """Фикстура для создания тестового клиента Flask."""
    app.config['TESTING'] = True
    # Отключаем защиту CSRF в тестах, если она включена
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

# --- Тесты вспомогательных функций ---


def test_email_validation():
    """Проверяет функцию валидации email."""
    assert is_valid_email("test@example.com") is not None
    assert is_valid_email("user.name@domain.ru") is not None
    assert is_valid_email("invalid-email") is None
    assert is_valid_email("test@.com") is None

# --- Тесты маршрутов (GET) ---


def test_home_page(client):
    """Проверяет доступность главной страницы."""
    response = client.get('/')
    assert response.status_code == 200
    assert "Добро" in response.data.decode('utf-8')


def test_about_page(client):
    """Проверяет доступность страницы 'О проекте'."""
    response = client.get('/about')
    assert response.status_code == 200
    assert "О проекте" in response.data.decode('utf-8')


def test_contact_page_get(client):
    """Проверяет доступность страницы контактов."""
    response = client.get('/contact')
    assert response.status_code == 200
    assert "Свяжитесь с нами" in response.data.decode('utf-8')

# --- Тесты формы контактов (POST) ---


def test_contact_post_success(client):
    """Проверяет успешную отправку формы."""
    data = {
        "name": "Иван",
        "email": "ivan@test.com",
        "message": "Привет, это тестовое сообщение!"
    }
    # Используем follow_redirects=True, чтобы проверить сообщение после редиректа
    response = client.post('/contact', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "Спасибо, Иван! Ваше сообщение успешно отправлено." in response.data.decode('utf-8')


def test_contact_post_empty_fields(client):
    """Проверяет попытку отправки пустой формы."""
    data = {"name": "", "email": "", "message": ""}
    response = client.post('/contact', data=data)
    # Статус 200, так как мы остаемся на странице с формой и ошибкой
    assert response.status_code == 200
    assert "Пожалуйста, заполните все поля!" in response.data.decode('utf-8')


def test_contact_post_invalid_email(client):
    """Проверяет отправку формы с некорректным email."""
    data = {
        "name": "Иван",
        "email": "плохой-email",
        "message": "Текст сообщения"
    }
    response = client.post('/contact', data=data)
    assert "Некорректный формат email!" in response.data.decode('utf-8')

# --- Тесты ошибок ---


def test_page_not_found(client):
    """Проверяет обработку 404 ошибки."""
    response = client.get('/some_non_existent_page')
    assert response.status_code == 404
    assert "Страница потерялась в космосе" in response.data.decode('utf-8')