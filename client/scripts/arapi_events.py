import logging
import os
import time
import utils

from selenium.webdriver.common.by import By


output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)
browser = utils.get_browser()


browser.get('chrome://attribution-internals/')
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
logging.info('checkout')
time.sleep(1)

browser.get('chrome://attribution-internals/')
logging.info('dashboard after events')
time.sleep(3)
browser.save_screenshot(os.path.join(output_path, 'dashboard_sources_after_events.png'))

# switch to the event-level reports tag
browser.find_element(By.ID, 'event-level-reports-tab').click()
time.sleep(2)
browser.save_screenshot(os.path.join(output_path, 'dashboard_event_level_reports_after_events.png'))

# we force the browser to send the reports instead of waiting for the scheduled time
browser.execute_script(
    "return document.getElementById('reportTable').shadowRoot.querySelector('table > thead > tr > th > input')"
).click()
time.sleep(1)
send_reports_button = browser.find_element(By.ID, 'send-reports').click()
time.sleep(2)

browser.quit()
print(f"Done: {__file__}")
