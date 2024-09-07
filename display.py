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
    Himage = Image.open(image_path)

    # Create a white background image
    background = Image.new('RGB', (epd.width, epd.height), (255, 255, 255))

    # Calculate position to paste the original image
    paste_x = (epd.width - Himage.width) // 2
    paste_y = (epd.height - Himage.height) // 2

    # Paste the original image onto the white background
    background.paste(Himage, (paste_x, paste_y))

    # Convert the image to RGB mode if it's not already
    background = background.convert('RGB')

    epd.display(epd.getbuffer(background))

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

