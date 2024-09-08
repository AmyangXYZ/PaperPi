#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image
import logging
import epd7in3f
import sys

logging.basicConfig(level=logging.INFO)

try:
    # Check if image path is provided as command line argument
    if len(sys.argv) < 2:
        print("Usage: python pi0_e_paper.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    logging.info("epd7in3f display")

    epd = epd7in3f.EPD()
    logging.info("init")
    epd.init()

    # Display your own image
    logging.info(f"Displaying image from: {image_path}")
    original_image = Image.open(image_path)

    # Crop the center part of the image
    def crop_center(img, target_width, target_height):
        img_width, img_height = img.size
        left = (img_width - target_width) // 2
        top = (img_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        return img.crop((left, top, right, bottom))

    # Crop the image to fit the display dimensions
    cropped_image = crop_center(original_image, epd.width, epd.height)

    # Convert the image to RGB mode if it's not already
    cropped_image = cropped_image.convert('RGB')

    epd.display(epd.getbuffer(cropped_image))

    logging.info("Image displayed successfully")

    logging.info("Goto Sleep...")
    epd.sleep()

    sys.exit(0)
except IOError as e:
    logging.info(e)
    sys.exit(1)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in3f.epdconfig.module_exit(cleanup=True)
    sys.exit(1)
