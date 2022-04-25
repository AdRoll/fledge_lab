#!/bin/bash


# add the Chromium installation to PATH
export PATH="$PATH:/opt/chrome-linux"

# print Chromium version
chrome --version

##################################################
# selenium scripts to run:
##################################################

cd scripts

date

python auction.py
python dynamic_auction.py
python dynamic_auction_multi_dsp.py
python wasm_outside_worklet.py
python dynamic_wasm_auction.py

python find_interest_group_size.py
python test_interest_group_amount.py --n-IGs 10 --n-samples-before-maintenance 3 --n-samples-after-maintenance 3
python denial_of_service.py --n-total 10 --n-samples 8 --n-dsp 1

python arapi_click.py
python arapi_conversion.py

date
echo "Done."
