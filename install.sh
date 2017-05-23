#pros'ba vvesti parol
#!/bin/bash
apt-get install apache2 -y
/etc/init.d/apache2 stop
apt-get install nginx -y
apt-get install sysstat -y
apt-get install bc -y
mkdir /var/www/html/sysinfo
cp ./index.cgi /var/www/html/sysinfo/index.cgi
chmod 755 /var/www/html/sysinfo/index.cgi
cp ./nginx-sysinfo.conf  /etc/nginx/sites-available/default
ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
echo "ServerName balinux.local" >> /etc/apache2/apache2.conf
cp ./ports.conf /etc/apache2/ports.conf
cp ./apache2-sysinfo.conf /etc/apache2/sites-available/000-default.conf
a2ensite 000-default.conf
a2enmod cgi
systemctl restart apache2
systemctl restart nginx
touch /var/log/mpstat.log  /var/log/iostat.log  /var/log/tcp.log /var/log/udp.log /var/log/df.log /var/log/network.log
crontab cron.bak

