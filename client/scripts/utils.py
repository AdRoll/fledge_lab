import os
from typing import List

import pandas as pd
from PIL import Image
import pytesseract
import seaborn as sns
from selenium import webdriver

OUTPUT_DIR = '/opt/output'
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def get_browser(extra_args: List[str] = []):
    """Gets new browser instance (with clean memory/cache).

    Args:
        extra_args (List[str], optional): Any extra arguments to pass to Chromium
                                          (e.g. ['--auto-open-devtools-for-tabs']).

    Returns:
        webdriver.Chrome: Chromium instance controlled with the Selenium driver.
    """
    chrome_args_unwrapped = os.environ['CHROME_ARGS'].split(' ')
    args = chrome_args_unwrapped + [os.environ['PRIVACY_SANDBOX_FLAGS']] + extra_args
    options = webdriver.ChromeOptions()
    for arg in args:
        options.add_argument(arg)
    return webdriver.Chrome(options=options)


def prepare_output_path(filename: str, suffix: str = '') -> str:
    """Prepares the output path for the script.

    Args:
        filename (str): Script's filename.
        suffix (str, optional): Any suffix you may want to add. One use case could be
                                anywhere you run the same script with different parameters.

    Returns:
        str: output path created for the script.
    """
    base_path = os.path.basename(filename)
    base_filename = os.path.splitext(base_path)[0] + suffix
    target_path = os.path.join(OUTPUT_DIR, base_filename)

    os.makedirs(target_path, exist_ok=True)

    return target_path


def produce_before_after_maintenance_chart(path: str):
    """Produce chart of before/after maintenance.

    Very specific function to parse the logs of test_interest_group_amount.py
    and produce the distribution charts for the winning bids before and after
    the Chromium interest group maintenance.

    Args:
        path (str): Log file to use for chart creation.
    """
    relevant_lines = []
    after_maintenance = False

    with open(os.path.join(path, 'log'), 'r') as f:
        for line in f:
            if 'trigger maintenance' in line:
                after_maintenance = True
            if 'Dynamic Ad:' in line:
                relevant_lines.append((after_maintenance, line))

    maintenance = [a for a, _ in relevant_lines]
    bids = [int(b.split('-')[-1].replace('\n', '')) for _, b in relevant_lines]

    n_diff_bids = len(set(bids))
    df = pd.DataFrame({'After Maintenance?': maintenance, 'Winning Bid': bids})

    sns.set(rc={'figure.figsize': (14, 6)})
    g = sns.histplot(data=df, x='Winning Bid', hue='After Maintenance?', bins=n_diff_bids, discrete=True)
    g.set_title('Number of Winning Bids per Price, Before and After Maintenance')
    g.get_figure().savefig(os.path.join(path, '_winning_bids.png'))


def save_image_text(image_filename: str, text_filename: str):
    """Saves text from image file using OCR.

    Args:
        image_filename (str): filename of image to read text from.
        text_filename (str): filename for text output.
    """
    try:
        img = Image.open(image_filename)
        page_text = pytesseract.image_to_string(img)
    except FileNotFoundError as e:
        page_text = e
    finally:
        with open(text_filename, 'w') as f:
            f.write(page_text)
