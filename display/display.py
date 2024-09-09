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
        print("Usage: python display.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    logging.info("epd7in3f display")

    epd = epd7in3f.EPD()
    logging.info("init")
    epd.init()

    # Display your own image
    logging.info(f"Displaying image from: {image_path}")
    image = Image.open(image_path)

    # Ensure the image is in RGB mode
    image = image.convert('RGB')

    # Resize the image to fit the display dimensions if necessary
    if image.size != (epd.width, epd.height):
        image = image.resize((epd.width, epd.height), Image.LANCZOS)

    epd.display(epd.getbuffer(image))

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
