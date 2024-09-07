import os
import time
import subprocess

IMAGE_FOLDER = "../images"
DISPLAY_DURATION = 7200  # 2 hours in seconds


def cycle_images():
    while True:
        for image in os.listdir(IMAGE_FOLDER):
            if image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                image_path = os.path.join(IMAGE_FOLDER, image)
                subprocess.run(["python", "display.py", image_path])
                time.sleep(DISPLAY_DURATION)


if __name__ == "__main__":
    cycle_images()

