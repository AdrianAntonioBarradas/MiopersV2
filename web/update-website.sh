#!/bin/sh

cd /home/adrian/Miopers/web
npm run build
sudo service nginx reload
