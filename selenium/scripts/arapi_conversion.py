import time
import os
import logging
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

browser.get('https://advertiser/arapi-event?type=add-to-cart')
logging.info('add to cart')
time.sleep(1)

browser.get('https://advertiser/arapi-event?type=checkout')
logging.info('add to cart')
time.sleep(1)

browser.get('chrome://conversion-internals/')
logging.info('dashboard after click and conversions')
time.sleep(3)
browser.save_screenshot(os.path.join(output_path, 'dashboard_after_click_and_conversions.png'))

# we force the browser to send the reports instead of waiting for the scheduled time
checkboxes = browser.find_element(By.XPATH, "//input[@type='checkbox']")
checkboxes.click()
send_reports_button = browser.find_element(By.ID, 'send-reports')
send_reports_button.click()
time.sleep(1)

browser.quit()
print(f"Done: {__file__}")
