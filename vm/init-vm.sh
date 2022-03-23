#!/bin/bash

ADDITIONAL_PACKAGES="zsh vim-enhanced nano mc perl-core man man-pages sysstat zip unzip nc wget screen tmux git epel-release"
DEFAULT_USER="centos"

### OS setup

sudo yum -yq update
sudo yum -y install $ADDITIONAL_PACKAGES
sudo yum-config-manager --enable epel

sudo cp /etc/skel/.zshrc /etc/skel/.zshrc.orig
sudo wget -O /etc/skel/.zshrc http://git.grml.org/f/grml-etc-core/etc/zsh/zshrc

sudo usermod -s /bin/zsh $DEFAULT_USER
sudo cp /etc/skel/.zshrc /home/$DEFAULT_USER
sudo chown $DEFAULT_USER /home/$DEFAULT_USER/.zshrc

sudo usermod -s /bin/zsh root
sudo cp /etc/skel/.zshrc /root

### Python

sudo yum -y install python-pip python-virtualenv python-setuptools Cython

### Build system

sudo yum -y install gcc gcc-c++ autoconf autoconf-archive automake libtool perl-ExtUtils-PkgConfig

### Frog

sudo yum -y install libxml2-devel libicu-devel libcurl-devel

function pkg_install {
  git clone https://github.com/LanguageMachines/$1
  cd $1
  sh bootstrap.sh
  env PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure
  make
  sudo make install
  cd ..
}

# ticcutils
pkg_install ticcutils

# libfolia
pkg_install libfolia

# ucto
pkg_install ucto

# timbl
pkg_install timbl

# mbt
pkg_install mbt

# frogdata
pkg_install frogdata

# frog
pkg_install frog

sudo sh -c "echo "/usr/local/lib" >> /etc/ld.so.conf"
sudo ldconfig -v

# python-frog
git clone https://github.com/proycon/python-frog
cd python-frog
sudo python setup.py install
cd ..

### Nginx install

sudo yum -y install nginx
sudo mv /etc/nginx /etc/nginx.orig

sudo mkdir -p /etc/nginx
sudo cp /etc/nginx.orig/mime.types /etc/nginx/mime.types
sudo mv nginx.conf /etc/nginx

sudo mv server.key /etc/pki/tls/certs
sudo mv server.crt /etc/pki/tls/certs

# http://stackoverflow.com/questions/25995060/nginx-cannot-connect-to-jenkins-on-centos-7
sudo setsebool -P httpd_can_network_connect 1

# https://www.centos.org/forums/viewtopic.php?f=13&t=49280
sudo restorecon -r /etc/nginx
sudo restorecon -r /etc/pki/tls/certs

sudo systemctl enable nginx.service
sudo systemctl start nginx.service
sudo systemctl status nginx.service

### Redis

sudo yum install -y redis

sudo cp /etc/redis.conf /etc/redis.conf.orig
sudo mv redis.conf /etc/redis.conf
sudo restorecon /etc/redis.conf

sudo systemctl enable redis.service
sudo systemctl start redis.service
sudo systemctl status redis.service
