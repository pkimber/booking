Booking
*******

Django application for booking

Work in Progress
================

Model for room has been added to allow rooms to be specified in a location

 - Create and Update views have been added
 - Need to add views to manage room bookings

Install
=======

Virtual Environment
-------------------

::

  virtualenv --python=python3.4 venv-booking
  source venv-booking/bin/activate
  pip install --upgrade pip

  pip install -r requirements/local.txt

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

::

 ../init_dev.sh

Release
=======

https://www.pkimber.net/open/
