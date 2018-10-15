#!/usr/bin/env bash
# 1. Install java
yum -y install java-1.8.0-openjdk

# 2. Download Elastic Search
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.1.rpm -P /tmp

# 3. Install Elastic Search
rpm -ivh /tmp/elasticsearch-6.3.1.rpm

# 4. Autostart Elastic Search
sudo chkconfig --add elasticsearch

# 5. Configure Elastic Search
mv /etc/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml.orig
# TODO: make this sudoedit because symlink no longer works
ln -s /vagrant/build_scripts/es_setup/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

mkdir -p /data/es_logs
chown -R vagrant:vagrant /data
chmod 777 -R /data

# 6. Start Elastic Search
sudo /etc/init.d/elasticsearch start
