import argparse
import logging
import os
import time
import utils

from PIL import Image
import pytesseract

parser = argparse.ArgumentParser(description='Test how many IGs we can join')
parser.add_argument('-n', '--n-IGs', dest='n_ig', type=int,
                    help='How many IGs to join for test')
parser.add_argument('-w', '--wait', dest='wait', type=int, default=0,
                    help='How many seconds to wait before starting to collect samples')
parser.add_argument('-s', '--n-samples', dest='n_samples', type=int, default=1,
                    help='Number of samples to collect')
args = parser.parse_args()
assert args.n_ig > 0 and args.wait >= 0 and args.n_samples > 0

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

# update the IG with the top bid so it is no longer the oldest one
browser.get(f"https://advertiser/dynamic?name=success-ig-{args.n_ig}&bid={args.n_ig}")
logging.info(f"visited advertiser (join dynamic IG with bid {args.n_ig})")

logging.info(f"Waiting {args.wait}")
time.sleep(args.wait)

for sample_i in range(args.n_samples):
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
