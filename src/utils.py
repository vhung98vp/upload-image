import base64
import os
from datetime import datetime
from fastapi import HTTPException
from PIL import Image
from io import BytesIO
from config import get_logger, IMAGE_DIR, ERROR_FILE
from db_client import save_data

logger = get_logger(__name__)


def decode_base64_image(image_b64: str) -> bytes:
    try:
        return base64.b64decode(image_b64, validate=True)
    except Exception as e:
        logger.error(f"Invalid base64 decode: {e}")
        raise HTTPException(status_code=400, detail="Invalid base64")

def verify_image(img_bytes: bytes):
    try:
        Image.open(BytesIO(img_bytes)).verify()
        return True
    except Exception as e:
        logger.error(f"Image verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid image data")

def save_file(user_id: str, img_bytes: bytes) -> str:
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    date_str = timestamp[:8]
    os.makedirs(f"{IMAGE_DIR}/{date_str}", exist_ok=True)
    save_path = f"{IMAGE_DIR}/{date_str}/{user_id}_{timestamp}.png"
    try:
        with open(save_path, "wb") as f:
            f.write(img_bytes)
    except Exception as e:
        logger.error(f"Failed to save file for key={user_id}: {e}")
        raise HTTPException(status_code=500, detail="File save failed")

    logger.info(f"Saved file: {save_path}")
    return save_path


def process_image(user_id: str, image_b64: str) -> str:
    logger.info(f"Processing upload for key={user_id}")
    try:
        img_bytes = decode_base64_image(image_b64)
        verify_image(img_bytes)
        saved_path = save_file(user_id, img_bytes)
        save_data(user_id, saved_path)
    except HTTPException as he:
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        with open(ERROR_FILE, "a") as f:
            f.write(f"{timestamp}, {user_id}, {image_b64}\n")
        raise he

    logger.info(f"Completed processing for key={user_id}")
    return saved_path