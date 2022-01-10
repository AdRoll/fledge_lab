import time
import os
import logging
import utils


output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)


for i in range(64):
    browser = utils.get_browser()
    browser.get('https://advertiser/dynamic?name=ig-1&bid=1')
    browser.get(f"https://advertiser/dynamic?name=dsp{i}&bid=100&dsp=dsp{i}")  # should always win if custom DSP worked
    browser.get('https://advertiser/dynamic?name=ig-2&bid=2')

    browser.get('https://publisher/')
    time.sleep(0.7)
    browser.save_screenshot(os.path.join(output_path, f"publisher_after_join_dsp{i}.png"))

    browser.quit()
print(f"Done: {__file__}")
