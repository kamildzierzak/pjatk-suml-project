import numpy as np
import logging

from PIL import Image
from ml.ml_config import MLConfig

logger = logging.getLogger(__name__)


def preprocess_image(file):
    """
    Preprocess an image file to fit the model input requirements.
    """
    try:
        img = Image.open(file).convert("RGB")
        img = img.resize((MLConfig.IMG_SIZE, MLConfig.IMG_SIZE))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        return None
