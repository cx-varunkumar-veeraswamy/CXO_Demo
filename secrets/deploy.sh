#!/bin/bash
# FAKE CREDENTIALS - demo only
export GITLAB_TOKEN="glpat-abcdefghij0123456789"
export DOCKERHUB_PASSWORD="dckr_pat_abcdefghijklmnopqrstuvwxyz1"
curl -u admin:admin123 http://internal.example.com/deploy
mysql -uroot -pRootPass123 -e "select 1"
sshpass -p 'S3rverPass!' ssh root@10.0.0.5 "reboot"
