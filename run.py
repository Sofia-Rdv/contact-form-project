from app import app
import logging

logger = logging.getLogger("my_app")

if __name__ == '__main__':
    logger.info('Программа "contact_form_project" запущена.')
    app.run(debug=True)