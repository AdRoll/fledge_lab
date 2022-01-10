import os
import logging
import utils
import time

output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)
browser = utils.get_browser(extra_args=['--auto-open-devtools-for-tabs'])
logging.info(f"Chromium version: {browser.capabilities['browserVersion']}")


browser.get('https://advertiser/dynamic?name=wasm&bid=29&biddingLogicName=bidding_logic_wasm')
time.sleep(2)
browser.get('https://publisher')
time.sleep(60 * 60 * 4)

browser.quit()
print(f"Done: {__file__}")
