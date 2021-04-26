#!/bin/sh

# https://www.stavros.io/posts/deploy-django-dokku/

randpw(){ < /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-64};echo;}

if [ $# -ne 2 ];
    then echo "Usage:\n    mkproject <appname> <naked domain>"
    exit 1
fi

sudo dokku apps:create $1
sudo dokku postgres:create $1-db
sudo dokku redis:create $1-redis

sudo dokku postgres:link $1-db $1
sudo dokku redis:link $1-redis $1

sudo dokku config:set --no-restart $1 NODEBUG=1
sudo dokku config:set --no-restart $1 SECRET_KEY=`randpw`

read -p "Now push your code to Dokku, wait for it to deploy successfully and press any key here." mainmenuinput

sudo dokku domains:add $1 $2 www.$2
sudo dokku letsencrypt $1
sudo dokku redirect:set $1 $2 www.$2