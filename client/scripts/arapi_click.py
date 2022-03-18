import logging
import os
import time
import utils

from selenium.webdriver.common.by import By


output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)
browser = utils.get_browser()


browser.get('chrome://conversion-internals/')
logging.info('dashboard before click')
time.sleep(3)
browser.save_screenshot(os.path.join(output_path, 'dashboard_before_click.png'))

browser.get('https://advertiser/ads/dynamic-attribution-reporting-ad?text=test')
logging.info('visited ad')
time.sleep(1)
browser.save_screenshot(os.path.join(output_path, 'ad.png'))

ad = browser.find_element(By.ID, 'ad')
ad.click()
logging.info('clicked on ad')
time.sleep(1)
browser.save_screenshot(os.path.join(output_path, 'after_click.png'))

browser.get('chrome://conversion-internals/')
logging.info('dashboard after click')
time.sleep(3)
browser.save_screenshot(os.path.join(output_path, 'dashboard_after_click.png'))

browser.quit()
print(f"Done: {__file__}")
