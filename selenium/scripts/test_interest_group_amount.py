import time
import os
import logging
import argparse
import utils
from PIL import Image
import pytesseract

parser = argparse.ArgumentParser(description='Test how many IGs we can join')
parser.add_argument('-n', '--n-IGs', dest='n_ig', type=int,
                    help='How many IGs to join for test')
parser.add_argument('-b', '--n-samples-before-maintenance', dest='n_samples_before_maintenance',
                    type=int, default=1, help='Number of samples to collect before maintenance')
parser.add_argument('-a', '--n-samples-after-maintenance', dest='n_samples_after_maintenance',
                    type=int, default=1, help='Number of samples to collect after maintenance')
args = parser.parse_args()
assert args.n_ig > 0 and args.n_samples_after_maintenance > 0

output_path = utils.prepare_output_path(__file__, suffix=f"_{args.n_ig}")
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w',
                    level=logging.DEBUG, format=utils.LOGGING_FORMAT)
browser = utils.get_browser()


browser.get('https://publisher/')
logging.info('visited publisher before join')
time.sleep(1)
browser.save_screenshot(os.path.join(output_path, 'publisher_before_join.png'))

# Join all IGs with bids/names in decreasing order so that the oldest ones are also the ones
# with the highest bids. This ensures that when the oldest ones (in insertion terms) are
# evicted, the winner will be the oldest one that was not evicted and thus it should give
# us an idea of how many were actually evicted (barring timeouts...)
for i in reversed(range(1, args.n_ig + 1)):
    browser.get(f"https://advertiser/dynamic?name=success-ig-{i}&bid={i}")
    logging.info(f"visited advertiser (join dynamic IG with bid {i})")

for sample_i in range(args.n_samples_before_maintenance + args.n_samples_after_maintenance):
    if sample_i == args.n_samples_before_maintenance:
        logging.info('Starting 40s wait to trigger maintenance')
        time.sleep(40)

    publisher_screenshot = os.path.join(output_path, f"publisher_after_join__{sample_i}.png")
    logging.info(f"Going into auction: {sample_i}")
    browser.get('https://publisher/')
    logging.info('visited publisher after join')
    for screenshot_i in range(60):
        time.sleep(1)
        logging.info('Capturing screenshot...')
        browser.save_screenshot(publisher_screenshot)
        page_text = pytesseract.image_to_string(Image.open(publisher_screenshot))
        if 'success' in page_text:
            logging.info(f"Auction succeeded after {screenshot_i+1} tries")
            logging.info(page_text)
            break

browser.quit()
print(f"Done: {__file__}")

utils.produce_before_after_maintenance_chart(output_path)
