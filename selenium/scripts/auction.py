import time
import os
import logging
import utils


output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w', level=logging.DEBUG, format=utils.LOGGING_FORMAT)
browser = utils.get_browser()
logging.info(f"Chromium version: {browser.capabilities['browserVersion']}")


URLS_IMAGES = [
    (None, 'publisher_before_join.png'),
    ('https://advertiser', 'publisher_after_general_join.png'),
    ('https://advertiser/shoe-a', 'publisher_after_shoe_a_join.png'),
    ('https://advertiser/shoe-b', 'publisher_after_shoe_b_join.png'),
]

for url_advertiser, image_name in URLS_IMAGES:
    if url_advertiser:
        browser.get(url_advertiser)  # join the IG
    browser.get('https://publisher/')  # trigger auction & show winning ad
    time.sleep(0.5)  # wait a little to make sure we screenshot after completion
    browser.save_screenshot(os.path.join(output_path, image_name)) 


browser.quit()
print(f"Done: {__file__}")
