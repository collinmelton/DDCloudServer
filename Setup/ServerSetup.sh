#! /bin/bash

# install the server
yum -y update yum
yum -y install httpd
yum -y install mod_wsgi
yum -y install httpd-devel
yum -y install gcc
yum -y install mod_ssl
yum -y install git

# install the ddserver software
cd /var/
git clone https://github.com/collinmelton/DDCloudServer.git

# install mod proxy add on to forward to port
cd ~/
curl -O https://raw.githubusercontent.com/unbit/uwsgi/master/apache2/mod_proxy_uwsgi.c
apxs -i -c mod_proxy_uwsgi.c

# write the httpd conf files
cp /var/DDCloudServer/Setup/uwsgi_forward.conf /etc/httpd/conf.d/uwsgi_forward.conf
serverip=`/sbin/ifconfig eth0 | grep "inet" | awk '{print $2}' | awk 'NR==1' | cut -d':' -f2`
sed -i -- "s/ServerName 146.148.39.167/ServerName $serverip/g" /etc/httpd/conf.d/uwsgi_forward.conf
rm -f /etc/httpd/conf.d/wsgi.conf
rm -f /etc/httpd/conf.d/ssl.conf

# install ssl add on 
openssl req -new -x509 -days 365 -sha1 -newkey rsa:1024 -nodes -keyout server.key -out server.crt -subj "/O=Stanford/OU=Genetics/CN=$serverip"
chown root:root server.key
chmod 700 server.key
chown root:root server.crt 
chmod 700 server.crt 
cp -f server.key /etc/pki/tls/private/localhost.key
cp -f server.crt /etc/pki/tls/certs/localhost.crt

# install python2.7, pip, virtualenv, and python ddserver dependencies
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel
cd /opt
wget --no-check-certificate https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
tar xf Python-2.7.6.tar.xz
cd Python-2.7.6
./configure --prefix=/usr/local
make && make altinstall
wget https://bootstrap.pypa.io/get-pip.py
/usr/local/bin/python2.7 get-pip.py
/usr/local/bin/pip2.7 install virtualenv
/usr/local/bin/virtualenv venv -p /usr/local/bin/python2.7
source venv/bin/activate
/opt/Python-2.7.6/venv/bin/pip install flask
/opt/Python-2.7.6/venv/bin/pip install sqlalchemy
/opt/Python-2.7.6/venv/bin/pip install pattern
/opt/Python-2.7.6/venv/bin/pip install apache-libcloud
/opt/Python-2.7.6/venv/bin/pip install flask_bootstrap
/opt/Python-2.7.6/venv/bin/pip install uwsgi
/opt/Python-2.7.6/venv/bin/pip install psutil
/opt/Python-2.7.6/venv/bin/pip install flask_oauthlib
/opt/Python-2.7.6/venv/bin/pip install PyCrypto
/opt/Python-2.7.6/venv/bin/pip install backports.ssl_match_hostname
/opt/Python-2.7.6/venv/bin/pip install celery

# turn off selinux to allow port forwarding? would be great to not have to do this
setenforce 0

# install rabbitmq
wget https://github.com/rabbitmq/erlang-rpm/releases/download/v1.4.9/erlang-19.1.6-1.el6.x86_64.rpm
rpm -Uvh erlang-19.1.6-1.el6.x86_64.rpm
wget https://forensics.cert.org/cert-forensics-tools-release-el6.rpm
rpm -Uvh cert-forensics-tools-release*rpm
yum -y --enablerepo=forensics install socat
wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.6/rabbitmq-server-3.6.6-1.el6.noarch.rpm
rpm -Uvh rabbitmq-server-3.6.6-1.el6.noarch.rpm
chkconfig rabbitmq-server on
/sbin/service rabbitmq-server start

# start the server
service httpd start
mkdir /var/DDCloudServer/PemFiles
cd /var/DDCloudServer/DDServerApp/FlaskApp/

celery -A CeleryApp worker --loglevel=info&
uwsgi --socket 127.0.0.1:8081 --wsgi-file WSGI.py --callable app --processes 1 --threads 1 --stats 127.0.0.1:9191

