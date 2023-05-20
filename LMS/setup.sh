#!/bin/bash
python manage.py migrate --no-input
python manage.py createsuperuser --no-input --username=admin --password=admin
