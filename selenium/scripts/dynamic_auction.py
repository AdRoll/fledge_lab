import logging
import os
import time
import utils


output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)
browser = utils.get_browser()


browser.get('https://publisher/')
logging.info('visited publisher before join')
time.sleep(1)
browser.save_screenshot(os.path.join(output_path, 'publisher_before_join.png'))

for i in [1, 3, 2]:
    browser.get(f"https://advertiser/dynamic?name=ig-{i}&bid={i}")
    logging.info(f"visited advertiser (join dynamic IG with bid {i})")

browser.get('https://publisher/')
logging.info('visited publisher after join')
time.sleep(1)
browser.save_screenshot(os.path.join(output_path, 'publisher_after_join.png'))

browser.quit()
print(f"Done: {__file__}")
