import os
import random
import subprocess
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Directory containing the images
IMAGE_DIR = "../images"

# Time interval between image changes (in seconds)
INTERVAL = 3600  # 1 hour


def get_random_image():
    """Randomly select an image from the IMAGE_DIR."""
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not images:
        logging.error(f"No images found in {IMAGE_DIR}")
        return None
    return os.path.join(IMAGE_DIR, random.choice(images))


def main():
    while True:
        image_path = get_random_image()
        if image_path:
            logging.info(f"Displaying image: {image_path}")
            subprocess.run(["python", "display.py", image_path])
        else:
            logging.error("No image selected. Waiting before trying again.")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
