import logging
import os
import utils


output_path = utils.prepare_output_path(__file__)
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)
browser = utils.get_browser()
logging.info(f"Chromium version: {browser.capabilities['browserVersion']}")


browser.get('https://dsp/wasm?bid=10')
browser.save_screenshot(os.path.join(output_path, 'screenshot_10.png'))

browser.get('https://dsp/wasm?bid=42')
browser.save_screenshot(os.path.join(output_path, 'screenshot_42.png'))

# dump console log from browser, we can do this given this is outside of the worklet
# this saves us from having to manually go and open the console every time
logging.info('Dumping console log...')
for console_log in browser.get_log('browser'):
    logging.info(console_log)


browser.quit()
print(f"Done: {__file__}")
