import logging
import os

# Check environment (default to "production")
ENV = os.getenv("ENV", "production").lower()

# Configure basic format
log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
handlers = [logging.StreamHandler()]  # Always log to terminal/console

# Add file logging only in local dev mode
if ENV == "local":
    handlers.append(logging.FileHandler("app.log"))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if ENV == "local" else logging.INFO,
    format=log_format,
    handlers=handlers
)

logger = logging.getLogger("EmailClassifier")
