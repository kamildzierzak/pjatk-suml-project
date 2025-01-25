import numpy as np

from tensorflow.keras.preprocessing import image

def preprocess_image(raw_img):
    img = raw_img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

