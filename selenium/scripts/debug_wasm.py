# simple script to help with debugging WASM.
# 1. It opens a browser with devtools open.
# 2. It joins an interest group for which the bidder will use WASM.
# 3. It triggers an auction by visiting the publisher.
# 4. It sleeps for a while so the person debugging can use VNC to manually
#    explore the browser.
import logging
import os
import time
import utils

output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)
# open devtools console automatically
browser = utils.get_browser(extra_args=['--auto-open-devtools-for-tabs'])

browser.get('https://advertiser/dynamic?name=wasm&bid=29&biddingLogicName=bidding_logic_wasm')
time.sleep(2)
browser.get('https://publisher')
time.sleep(60 * 60 * 4)

browser.quit()
print(f"Done: {__file__}")
