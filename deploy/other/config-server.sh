#!/bin/bash

# Solve 'sudo: unable to resolve host fiwareiot-orion-idas-mosquitto' error
# add hostname (shown in /etc/hostname) in line with 127.0.0.1 on /etc/hosts
# https://askubuntu.com/questions/59458/error-message-when-i-run-sudo-unable-to-resolve-host-none

# Docker installation
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# Get system arch: https://unix.stackexchange.com/questions/180726/easy-command-line-method-to-determine-specific-arm-architecture-string
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# sudo add-apt-repository "deb [arch=armhf] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# sudo add-apt-repository "deb [arch=s390x] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get -y install docker-ce
sudo apt-get -y install docker-compose
sudo usermod -aG docker ${USER}
sudo reboot
