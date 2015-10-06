Booking
*******

Django application for booking

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
