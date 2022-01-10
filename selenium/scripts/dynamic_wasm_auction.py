import time
import os
import logging
import utils


output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w', level=logging.DEBUG, format=utils.LOGGING_FORMAT)
browser = utils.get_browser(extra_args=['--auto-open-devtools-for-tabs'])


browser.get('https://publisher/')
logging.info('visited publisher before join')
time.sleep(1)
browser.save_screenshot(os.path.join(output_path, 'publisher_before_join.png'))

browser.get('https://advertiser/dynamic?name=ig-1&bid=1')
logging.info('visited advertiser (join dynamic IG with bid 1)')

# should win IF WASM works
# biddingLogicName=bidding_logic_wasm means the IG will fetch bidding_logic_wasm.js at auction time
browser.get('https://advertiser/dynamic?name=ig-3-wasm&bid=3&biddingLogicName=bidding_logic_wasm')
logging.info('visited advertiser (join dynamic IG with bid 3)')
browser.save_screenshot(os.path.join(output_path, 'advertiser_join_3_wasm.png'))

browser.get('https://advertiser/dynamic?name=ig-2&bid=2')
logging.info('visited advertiser (join dynamic IG with bid 2)')

browser.get('https://publisher/')
logging.info('visited publisher after join')
time.sleep(1)
browser.save_screenshot(os.path.join(output_path, 'publisher_after_join.png'))


browser.quit()
print(f"Done: {__file__}")
