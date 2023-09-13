import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'images'

def save_image(image, city, district):
    # Create directories if they don't exist
    city_directory = os.path.join(UPLOAD_FOLDER, city)
    district_directory = os.path.join(city_directory, district)
    os.makedirs(city_directory, exist_ok=True)
    os.makedirs(district_directory, exist_ok=True)

    # Save image with a unique filename
    filename = secure_filename(image.filename)
    filepath = os.path.join(district_directory, filename)
    image.save(filepath)

    return filepath