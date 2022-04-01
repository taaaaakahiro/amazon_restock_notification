#!/bin/sh

cd /home/ec2-user/amazonRestockNotification
docker-compose exec -T web python /usr/src/app/python/search_amazon_item.py
