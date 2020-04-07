#!/usr/bin/env bash

#from https://www.techrepublic.com/article/how-to-easily-add-an-ssh-fingerprint-to-your-knownhosts-file-in-linux/
#ssh-keyscan -H 192.168.1.162 >> ~/.ssh/known_hosts

scp -o "StrictHostKeyChecking=no" ./build/dofin.tgz bitnami@18.197.40.62:/opt/bitnami/nginx/html/
#ssh -o "StrictHostKeyChecking=no" bitnami@18.197.40.62  < ./src/deploy.sh;
#cd /opt/bitnami/nginx/html/
#tar -xzvf dofin.tgz -C ./dofin/
