from fastapi import FastAPI
from .api.routes import router
from .core.logging_config import setup_logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
logger = setup_logging(debug_mode)

app = FastAPI(title="Evo Concierge Agent")

app.include_router(router, prefix="/agent")

# Log application startup
logger.info("Evo Concierge Agent starting up")
if debug_mode:
    logger.debug("Debug mode enabled") 