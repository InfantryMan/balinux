#!/bin/bash
sudo apt-get install apache2 -y
sudo /etc/init.d/apache2 stop
sudo apt-get install nginx -y
sudo apt-get install sysstat -y
sudo apt-get install bc -y
sudo mkdir /var/www/html/sysinfo
sudo cp ./index.cgi /var/www/html/sysinfo/index.cgi
sudo chmod 755 /var/www/html/sysinfo/index.cgi
sudo cp ./nginx-sysinfo.conf  /etc/nginx/sites-available/default
sudo cp ./apache2.conf /etc/apache2/apache2.conf
sudo cp ./ports.conf /etc/apache2/ports.conf
sudo cp ./apache2-sysinfo.conf /etc/apache2/sites-available/000-default.conf
sudo a2ensite 000-default.conf
sudo a2enmod cgi
sudo systemctl start apache2
sudo systemctl restart apache2
sudo systemctl restart nginx
sudo touch /var/log/mpstat.log  /var/log/iostat.log  /var/log/tcp.log /var/log/udp.log /var/log/df.log /var/log/network.log
sudo crontab cron.bak

