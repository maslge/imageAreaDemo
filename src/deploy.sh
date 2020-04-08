#!/usr/bin/env bash

#from https://www.techrepublic.com/article/how-to-easily-add-an-ssh-fingerprint-to-your-knownhosts-file-in-linux/
#ssh-keyscan -H 192.168.1.162 >> ~/.ssh/known_hosts
scp -o "StrictHostKeyChecking=no" ./build/dofin.tgz bitnami@18.197.40.62:/opt/bitnami/nginx/html/

#from https://unix.stackexchange.com/questions/349425/ssh-command-and-non-interactive-non-login-shell
ssh -o "StrictHostKeyChecking=no" bitnami@18.197.40.62  < ./src/deployOnRemoteHost.sh;
