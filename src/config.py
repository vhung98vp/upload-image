import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()


IMAGE_DIR = os.getenv("IMAGE_DIR", "/images")
LOG_DIR = os.getenv("LOG_DIR", "/logs")
ERROR_DIR = os.getenv("ERROR_DIR", "/errors")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(f"{LOG_DIR}/service.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

DB = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "name": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

TABLE = {
    "name": "image_metadata",
    "fields": {
        "user_id": "VARCHAR(255) NOT NULL",
        "file_path": "TEXT NOT NULL"
    }
}
