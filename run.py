from app import create_app
from app.config import Config
import logging

app = create_app()
app.logger.setLevel(logging.DEBUG)
app.config.from_object(Config)

if __name__ == '__main__':
    app.run(debug=True)