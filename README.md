#  Software Underground - Visualisations of log data quality (swung_viz_log) 

This repository contains code used for the visualisation hackathon for subsurface data. The code is written for Python 3.x.

# Get code
From the command line in a terminal, in a location (folder) where you want to store this code, execute:

git clone https://github.com/laurafroelich/swung_viz_log.git

# Git for windows

To use git in windows, you can google git for windows and choose one of the results. One of the results https://git-scm.com/download/win, which will download software to use git on windows.

# Setting up environment
Make sure you are using python3, check with

´python --version´

To install the required packages, run

´pip install -r requirements.txt´

from the folder swung_viz_log.


# Running on AWS
To serve this app from AWS, do the following:

1. Log in to you EC2 instance
2. Make sure the code is there (use git clone as described above)
3. Make sure data is there in the structure expected by the code (relative to code, data should be in ../data/EAGE2018/ in appropriate folders)
4. From the code directory, execute
´python app.py´
5. From the code directory, execute
´bokeh serve bokeh serve holoMagic.py --allow-websocket-origin=ec2-18-222-85-3.us-east-2.compute.amazonaws.com:5006´
6. In a browser, open the appropriate AWS url (e.g. http://ec2-18-222-85-3.us-east-2.compute.amazonaws.com:5000/)




