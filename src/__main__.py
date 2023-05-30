import logging
import src.app as app

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        app.main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")