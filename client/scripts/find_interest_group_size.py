import logging
import math
import os
import time
import utils

from PIL import Image
import pytesseract


output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)

PUBLISHER_SCREENSHOT = os.path.join(output_path, 'publisher.png')
IG_NAME = 'success'
BID = 1
counter = 0
left = 0
right = 2 * 1024 * 1024
auction_worked = False

while left != right:
    payload_size = math.ceil((left + right) / 2)

    browser = utils.get_browser()
    browser.get(f"https://advertiser/dynamic?name={IG_NAME}&bid={BID}&payloadSize={payload_size}")

    browser.get('https://publisher/')
    logging.info('visited publisher before join')
    time.sleep(0.5)
    browser.save_screenshot(PUBLISHER_SCREENSHOT)
    page_text = pytesseract.image_to_string(Image.open(PUBLISHER_SCREENSHOT))

    auction_worked = IG_NAME in page_text
    logging.info(f"payload_size {payload_size} (step {counter}) => {auction_worked}")

    if not auction_worked:
        right = payload_size - 1
    else:
        left = payload_size

    counter += 1
    browser.quit()

print(f"Done: {__file__}")
