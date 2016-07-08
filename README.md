# DORIS ePayments Site
ePayments site for the Department of Records and Information Services

## Setup Instructions
Clone the git repository:

    git clone https://brandontang@bitbucket.org/nycrecordswebdev/epayments.git

Create a virtual environment and install the requirements:

    virtualenv epayments
    source epayments/bin/activate
    pip install -r requirements.txt

Install gulp and initialize node_modules folder within the root directory with the following commands:

    sudo npm install gulp -g
    npm install

Install postgresql with the following command:

    sudo apt-get install postgresql

Initialize the database by entering the following in the psql line:

    psql
        username=# create database epayments;

Locally run the intranet by entering the following in the command line:

    python manage.py runserver

Run gulp in another tab to detect file changes:

    gulp