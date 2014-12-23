Booking
*******

Django application for booking

Install
=======

Virtual Environment
-------------------

::

  pyvenv-3.4 --without-pip venv-booking
  source venv-booking/bin/activate
  wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
  python get-pip.py

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
