# DDCloudServer
This software is designed to run genomics workflows on the Google Compute Engine. The distinguishing characteristic of this software is that it is designed to automatically mount and unmount disk storage as needed during the course of the workflow. This is in contrast to NFS storage or saving intermediate results to cloud storage. In certain use cases this strategy more closely approaches optimal resource utilization.

# Contents
- [Get Setup with GCE](#get-setup-with-gce)
- [Configure GCE Image](#configure-gce-image)
- [Get Service Account Authentication Info](#get-service-account-authentication-info) 
- [Using the Webserver](#using-the-webserver)

# Get Setup with GCE
Get a GCE Account and setup a Google Cloud Storage bucket. URI should look something like this gs://bucketname/

# Configure GCE Image
In this section we will configure a GCE Image for use as the OS on both the Master and Worker instances. 

## Boot GCE Instance
From the GCE developers console boot a new instance. I've chosen CENTOS6.6 as the base image, but if you use a different base you may need to modify the software installation below. Make sure to enable full access to storage during setup. This is important because you will save you image to your Google Cloud Storage bucket. 

## Install Software (for CENTOS6.6)
1. SSH into the new instance. 

2. Install Git

	sudo yum install git
	
3. Clone this project and note project location

	git clone git@github.com:collinmelton/DDCloudServer.git
	
4. Install project specific dependencies

	** install development tools **
	
	sudo yum install libevent-devel python-devel
	
	sudo yum groupinstall "Development tools"
	
	** install pip, apache-libcloud, PyCrypto, and httplib2 **
	
	curl -o get-pip.py https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
	
	sudo python get-pip.py
	 
	sudo pip install apache-libcloud
	
	sudo pip install PyCrypto
	
	sudo pip install httplib2
	
	** a bunch of crap to install python2.7, easyinstall, pip, and get PyCrypto etc **
	
	sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
	 
	wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
	
	tar xvzf Python-2.7.6.tgz
	
	sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel
	
	cd Python-2.7.6
	
	sudo ./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
	
	sudo make && sudo make altinstall
	
	wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
	
	sudo /usr/local/bin/python2.7 ez_setup.py
	
	sudo /usr/local/bin/easy_install-2.7 pip
	
	sudo /usr/local/bin/pip2.7 install apache-libcloud
	
	sudo /usr/local/bin/pip2.7 install PyCrypto
	
	sudo /usr/local/bin/pip2.7 install httplib2

	sudo /usr/local/bin/pip2.7 install psutil

	sudo /usr/local/bin/pip2.7 install -U https://github.com/google/google-visualization-python/zipball/master

## Create Image and Save to Cloud Storage

	sudo gcimagebundle -d /dev/sda -o /tmp/ --log_file=/tmp/abc.log
	
	** check to see name of the image file from output of above command and edit commands below with this name **
	
	gsutil cp /tmp/imagename.image.tar.gz gs://yourbucketname/
	
	** below you can name your image, I've name the image cloudtest2, I think this can also be done with gcloud ** 
	
	~/google-cloud-sdk/bin/gcutil --project "your_project_name" addimage cloudtest2 gs://yourbucketname/imagename.image.tar.gz
	or 
	gcloud compute images create cloudtest2 --source-uri gs://yourbucketname/imagename.image.tar.gz


# Get Service Account Authentication Info
In order to run the software you need to get a service account email address and a pem file. See instructions here: https://cloud.google.com/storage/docs/authentication#service_accounts

You should make a pem file and note your service account email address in the format: numbersandletters@developer.gserviceaccount.com


# Launch Webserver
Launch a new GCE instance on Centos6.6 with the following startup script. Make sure to enable https.
```
#! /bin/bash

# install the server
yum -y update yum
yum -y install httpd
yum -y install mod_wsgi
yum -y install httpd-devel
yum -y install gcc
yum -y install mod_ssl

# install mod proxy add on to forward to port
curl -O https://raw.githubusercontent.com/unbit/uwsgi/master/apache2/mod_proxy_uwsgi.c
apxs -i -c mod_proxy_uwsgi.c

# write the httpd conf files
/usr/local/bin/gsutil cp gs://gbsc-gcp-lab-snyder-users-cmelton/DDServerStartup/uwsgi_forward.conf /etc/httpd/conf.d/uwsgi_forward.conf
serverip=`/sbin/ifconfig eth0 | grep "inet" | awk '{print $2}' | awk 'NR==1' | cut -d':' -f2`
sed -i -- "s/ServerName 146.148.39.167/ServerName $serverip/g" /etc/httpd/conf.d/uwsgi_forward.conf
rm /etc/httpd/conf.d/wsgi.conf
rm /etc/httpd/conf.d/ssl.conf

# install ssl add on 
openssl req -new -x509 -days 365 -sha1 -newkey rsa:1024 -nodes -keyout server.key -out server.crt -subj "/O=Stanford/OU=Genetics/CN=$serverip"
chown root:root server.key
chmod 700 server.key
chown root:root server.crt 
chmod 700 server.crt 
cp server.key /etc/pki/tls/private/localhost.key
cp server.crt /etc/pki/tls/certs/localhost.crt

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

# install the ddserver software
/usr/local/bin/gsutil -m cp -r gs://gbsc-gcp-lab-snyder-users-cmelton/DDServerStartup/DDCloudServer/ /var/

# turn off selinux to allow port forwarding? would be great to not have to do this
setenforce 0

# start the server
service httpd start
cd /var/DDCloudServer/DDServerApp/FlaskApp/
uwsgi --socket 127.0.0.1:8081 --wsgi-file WSGI.py --callable app --processes 1 --threads 1 --stats 127.0.0.1:9191
```

# Using the Webserver
First navigate your webbrowser to the public ip address of the webserver using https so https://your-servers-ip-address/. 

## Sign In or login
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Login_login.png "Login")

## Setup a New Workflow

### Name Your Workflow and Describe Workflow Variables
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_workflows.png "New Workflow")

### Add Your Credentials
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_credentials.png "Add Credentials")

### Add an Image
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_images.png "Add Image")

### Specify Disks
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_disks.png "Add Disks")

### Specify Instances
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_instances.png "Add Instances")

### Specify Commands
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_commands.png "Add Commands")
	
# Web Server Version
I am developing an updated version of the software that runs a webserver (link coming soon). This version allows the user to generate a workflow, launch a workflow, and view progress and performance of the workflow as it runs.
