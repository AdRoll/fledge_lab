#!/bin/bash

# launch VNC Server so the container has a display in order to run Chromium in
# headful mode as headless mode does not run auctions
# first remove these 2 lock files as vnc they are not properly cleared if the
# is killed and will prevent future launches
rm -f /tmp/.X0-lock /tmp/.X11-unix/X0
vncserver -localhost no -passwd ~/.vnc/passwd :0 -geometry 1440x900 &

# add the Chromium installation to PATH
export PATH="$PATH:/opt/chrome-linux"

# print Chromium version
chrome --version

##################################################
# selenium scripts to run:
##################################################

cd scripts

python auction.py
python dynamic_auction.py
python dynamic_auction_multi_dsp.py
python wasm_outside_worklet.py
python dynamic_wasm_auction.py

python find_interest_group_size.py
python test_interest_group_amount.py --n-IGs 10 --n-samples-before-maintenance 3 --n-samples-after-maintenance 3
python denial_of_service.py --n-total 10 --n-samples 8 --n-dsp 1

python arapi_click.py


# remain idle (useful for using VNC)
sleep 24h
