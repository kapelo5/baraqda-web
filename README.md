# baraqda-web

First step is clone repo baraqda-lib from Github to main directory:

> git clone https://github.com/ADS-Studio-Deloitte/baraqda-lib.git

To start app we must use:

> pip install -r requirements.txt

The last step is import Flask and library to the application through addition two lines of code at the beginning of index.py file:
from flask import Flask oraz
import bar

To run app simply execute below command when being inside main directory:

> python "index.py"

If everything goes right, you can visit app on:
http://127.0.0.1:5000/

## Create container with Docker

To containerize application you must follow steps below.

1. Download repository from github.
   Change username and token for your own credentials.
   > git clone https://username:token@github.com/ADS-Studio-Deloitte/baraqda-web.git
2. Change directory to baraqda-web
   > cd baraqda-web
3. Open requirements.txt and change username and token for your own.
4. Build Docker image
   > docker build --tag baraqda-web .
5. Run Docker image
   > docker run baraqda-web
