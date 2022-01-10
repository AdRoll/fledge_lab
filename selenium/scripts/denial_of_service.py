import time
import os
import logging
import utils
from PIL import Image
import pytesseract
import time
import random
import argparse
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

N_DSP = 2

random.seed(1)

def get_dsp_to_use(i: int, out_of: int) -> str:
    """Get DSP to use.

    Gets the DSP URL param to pass given the number of the IG to join. It's just a
    simple way to alternate between DSPs.

    Args:
        i (int): number of IG to join (coming from a range).
        out_f (int): number of DSPs to use (max 64).

    Returns:
        str: URL param to pass as dsp.
    """
    mod_i = i % out_of
    return f"dsp{mod_i}"


parser = argparse.ArgumentParser(description='Test effect of computationally intensive bidders on auction')
parser.add_argument('--n-total', dest='n_total', type=int, default=100, help='How many bidders to have in total')
parser.add_argument('--n-samples', dest='n_samples', type=int, default=20, help='Number of samples to collect (on top of the base case with no malicious bidder)')
parser.add_argument('--n-dsp', dest='n_dsp', type=int, default=1, help='How many DSPs (buyers) to use (1 to 20)')
args = parser.parse_args()
assert args.n_total >= 2 and args.n_samples >= 8  # at least 8 samples needed for the regression module to work
assert 1 <= args.n_dsp <= 64


output_path = utils.prepare_output_path(__file__, suffix=f"{args.n_total}_{args.n_samples}_{args.n_dsp}")
PUBLISHER_SCREENSHOT_FILENAME = os.path.join(output_path, 'publisher.png')
logging.basicConfig(filename=os.path.join(output_path, 'log'), filemode='w', level=logging.DEBUG, format=utils.LOGGING_FORMAT)

# create list to determine how many malicious bidders we will be using and initialize a hashmap to record their respective times
MALICIOUS_COUNTS = [0] + [random.randint(0, args.n_total - 1) for _ in range(args.n_samples)]
timings = {x:[] for x in MALICIOUS_COUNTS}
highest_bid_won = {x:[] for x in MALICIOUS_COUNTS}

for n_malicious in MALICIOUS_COUNTS:
    n_normal = args.n_total - n_malicious
    normal_offset = n_malicious + 1
    # create a new browser (i.e. without IGs) to have a new environment for the run
    browser = utils.get_browser()

    # join "normal" IGs with simplistic pass-through bidding mechanism)
    for i in reversed(range(normal_offset, args.n_total + 1)):
        if args.n_dsp > 1:
            browser.get(f"https://advertiser/dynamic?name=success-{i}&bid={i}&dsp={get_dsp_to_use(i, args.n_dsp)}")
        else:
            browser.get(f"https://advertiser/dynamic?name=success-{i}&bid={i}")
    # join the "malicious" or computationally intensive IGs
    for i in range(n_malicious):
        if args.n_dsp > 1:
            browser.get(f"https://advertiser/dynamic?name=ig-{i}-malicious&biddingLogicName=infinite_loop&dsp={get_dsp_to_use(i, args.n_dsp)}")
        else:
            browser.get(f"https://advertiser/dynamic?name=ig-{i}-malicious&biddingLogicName=infinite_loop")

    # visit the publisher to start the auction
    browser.get('https://publisher/')
    # website had loaded but that does not mean the auction is done or rendered
    # to check for that we take a screenshot every 100ms and check if a normal IG (containing text "success")
    # is visible on the page, if so, we record the time and end the run. There is a maximum of 300 attempts.
    start_time = time.time()
    for screenshot_i in range(300):
        time.sleep(0.1)
        
        browser.save_screenshot(PUBLISHER_SCREENSHOT_FILENAME)
        page_text = pytesseract.image_to_string(Image.open(PUBLISHER_SCREENSHOT_FILENAME))
        if 'success' in page_text:
            timings[n_malicious].append(time.time() - start_time)
            highest_bid_won[n_malicious].append(f"success-{args.n_total}" in page_text)
            break

    # remove the screenshot so it does not affect the next run
    os.remove(PUBLISHER_SCREENSHOT_FILENAME)
    browser.quit()

logging.info(f"Timings: {timings}")
logging.info(f"Winning bid was the highest one: {highest_bid_won}")

# convert the data to long format to make it easier to create a chart
x = []
y = []
h = []
for n_malicious in timings.keys():
    for timing,highest_won in zip(timings[n_malicious], highest_bid_won[n_malicious]):
        x.append(n_malicious)
        y.append(timing)
        h.append(highest_won)
df = pd.DataFrame({'n malicious': x, 'time (seconds)': y, 'highest bidder won?': h})
df.to_csv(os.path.join(output_path, 'chart_data.csv'))

# create scatterplot of the data 
sns.set(rc = {'figure.figsize':(14,6)})
g = sns.scatterplot(data=df, x='n malicious', y='time (seconds)', hue='highest bidder won?')
g.set_title(f"Time taken to complete an auction and render the ad given n malicious bidders (from 0 to {args.n_total - 1})")
g.get_figure().savefig(os.path.join(output_path, 'chart.png'))

# fit simple linear regression to estimate the relationship between the number
# of malicious bidders and the time taken

X = [[1,a] for a in x]
reg = sm.OLS(y, X).fit()

with open(os.path.join(output_path, 'regression.txt'), 'w') as f:
    f.write(str(reg.summary()))

print(f"Done: {__file__}")
