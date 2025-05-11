import os
from app import create_app
from app.config import Config
import logging

app = create_app()
app.logger.setLevel(logging.DEBUG)
app.config.from_object(Config)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
