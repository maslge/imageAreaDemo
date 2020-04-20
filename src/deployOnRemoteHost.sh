#!/usr/bin/env bash

#from https://www.techrepublic.com/article/how-to-easily-add-an-ssh-fingerprint-to-your-knownhosts-file-in-linux/
cd /opt/bitnami/nginx/html/
rm -rf ./dofin/*
tar -xzvf dofin.tgz -C ./dofin/
