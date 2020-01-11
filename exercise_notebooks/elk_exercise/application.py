from app.flask_app import create_app
import logging
import pathlib

ROOT = pathlib.Path(__file__).parent

#logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
# logging.config.fileConfig(
#     ROOT / 'gunicorn_logging.conf', disable_existing_loggers=False)
application = create_app()

if __name__ == '__main__':
    application.run()
