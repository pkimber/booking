#!/bin/bash
# exit immediately if a command exits with a nonzero exit status.
set -e
# treat unset variables as an error when substituting.
set -u

py.test -x
touch temp.db && rm temp.db
django-admin migrate --noinput
django-admin demo_data_login
django-admin demo_data_booking
django-admin runserver
