Getting Started.
================

Django Framework.
-----------------

LetLive uses the `Django framework`_ for the web application.
LetLive also uses `Django-REST framework`_ for its REST API.

There are also more plugins that are used to power LetLive 
and they are described in the requirements section below.

.. _Django framework: https://www.djangoproject.com/
.. _Django-REST framework: https://www.django-rest-framework.org/


Requirements.
-------------

- Python requirements (version 3.7).

The requirements are defined in the ``requirements.txt`` file.
The requrements can be installed using pip ``pip install -r requirements.txt``.

Once Installed `pipenv`_ should be available.
This enables to create a virtual python environment for development,
and keeps track of the dependancies.
There is a shipped ``Pipfile`` and ``Pipfile.lock`` that is used by pipenv.

Please refere to the `pipenv docs`_ on how to use pipenv.

.. _pipenv: https://github.com/pypa/pipenv/
.. _pipenv docs: https://docs.pipenv.org/


- Javascript requirements.

Javascript requirements are managed by `npm`_ 
and are defined in the ``package.json`` and ``package-lock.json`` files.

To install these dependancies run ``npm install`` command.

.. _npm: https://www.npmjs.com


Setup
------

To setup LetLive and to get started with the development of Letlive
start by copying ``settings.example`` file to ``settings.py``.
The ``settings.example`` should be shipped and should not be deleted.

Then uncomment the ``# SECRET_KEY = 'random-chars'`` 
variable in the ``setting.py`` file.

Run ``python manage.py djecrety -spd letlive`` comand to autogenerate and update
the ``SECRET_KEY``.

Since no migrations are shiped, run ``python manage.py makemigrations``
to make the available migrations then migrate them by ``python manage.py migrate``.

Then create a superuser ``python manage.py createsuperuser``.

On finishing the steps above, LetLive is ready to run ``python manage.py runserver``.


