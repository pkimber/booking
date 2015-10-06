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

  py.test -x && \
      touch temp.db && rm temp.db && \
      django-admin migrate --noinput && \
      django-admin demo_data_login && \
      django-admin demo_data_booking && \
      django-admin runserver

Release
=======

https://www.pkimber.net/open/
