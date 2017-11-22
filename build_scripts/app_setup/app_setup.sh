#!/usr/bin/env bash

# 1. Install Python 3.5
yum -y install rh-python35

# 2. Install Redis 3.2
yum -y install rh-redis32

# 3. Setup /etc/profile.d/python.sh
bash -c "printf '#\!/bin/bash\nsource /opt/rh/rh-python35/enable\n' > /etc/profile.d/python35.sh"

# 4. Install Postgres Python Package (psycopg2) and Postgres Developer Package
yum -y install rh-postgresql95-postgresql-devel
yum -y install rh-python35-python-psycopg2
yum -y install openssl-devel
yum -y install libffi-devel
yum -y install libjpeg-devel

# 5. Install Developer Tools "Development Tools"
yum -y groupinstall "Development Tools"

# 6. Install Required pip Packages
source /opt/rh/rh-python35/enable
pip install virtualenv
mkdir /home/vagrant/.virtualenvs
virtualenv --system-site-packages /home/vagrant/.virtualenvs/epayments
chown -R vagrant:vagrant /home/vagrant
source /home/vagrant/.virtualenvs/epayments/bin/activate
pip install -r /vagrant/requirements.txt --no-binary :all:

# 7. Install telnet-server
yum -y install telnet-server

# 8. Install telnet
yum -y install telnet

# 9. Automatically Use Virtualenv
echo "source /home/vagrant/.virtualenvs/epayments/bin/activate" >> /home/vagrant/.bash_profile
