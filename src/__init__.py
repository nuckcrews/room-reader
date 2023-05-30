import os
import openai
import logging
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if not openai.api_key:
    logger.critical("OPENAI_API_KEY not found in environment variables.")
else:
    logger.info("OPENAI_API_KEY successfully loaded.")