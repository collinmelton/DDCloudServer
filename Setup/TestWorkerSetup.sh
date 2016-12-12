# Install project specific dependencies
sudo yum -y install libevent-devel python-devel
sudo yum -y groupinstall "Development tools"
curl -o get-pip.py https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
sudo python get-pip.py
sudo pip install apache-libcloud
sudo pip install PyCrypto
sudo pip install httplib2
sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar xvzf Python-2.7.6.tgz
sudo yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel
cd Python-2.7.6
sudo ./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
sudo make && sudo make altinstall
wget https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py
sudo /usr/local/bin/python2.7 ez_setup.py
sudo /usr/local/bin/easy_install-2.7 pip
sudo /usr/local/bin/pip2.7 install apache-libcloud
sudo /usr/local/bin/pip2.7 install PyCrypto
sudo /usr/local/bin/pip2.7 install httplib2
sudo /usr/local/bin/pip2.7 install psutil
sudo /usr/local/bin/pip2.7 install -U https://github.com/google/google-visualization-python/zipball/master
sudo /usr/local/bin/pip --no-cache-dir install werkzeug
sudo /usr/local/bin/pipinstall requests
sudo /usr/local/bin/pip install requests_oauthlib
sudo /usr/local/bin/pip install sqlalchemy
sudo /usr/local/bin/pip --no-cache-dir install pattern
sudo /usr/local/bin/pip --no-cache-dir install apache-libcloud==1.2.1
sudo /usr/local/bin/pip --no-cache-dir install backports.ssl_match_hostname
sudo /usr/local/bin/pip --no-cache-dir install gcloud
sudo cp /usr/bin/gcloud /usr/local/bin/gcloud

