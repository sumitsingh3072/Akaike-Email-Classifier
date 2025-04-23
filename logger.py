import logging
import os


ENV = os.getenv("ENV", "production").lower()

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
HANDLERS = [logging.StreamHandler()]  # Always log to terminal/console

# Add file logging only in local dev mode
if ENV == "local":
    HANDLERS.append(logging.FileHandler("app.log"))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if ENV == "local" else logging.INFO,
    format=LOG_FORMAT,
    handlers=HANDLERS,
)

logger = logging.getLogger("EmailClassifier")
