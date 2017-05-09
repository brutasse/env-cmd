Env-cmd
=======

A simple wrapper for executing virtualenv commands and passing them environment variables via a config file.

Use case
--------

Let's say you deploy a Django site named "example.com". You follow all
the best practices and deploy it as a Python package, installed in an
isolated virtualenv at ``/usr/share/python/example-com`` (as `dh_virtualenv
<https://github.com/spotify/dh-virtualenv>`_ would do).

Configuration is read from environment variables in the Django settings.

When you want to run a Django management command on your server, you would
type::

    ENV_VAR_1=value ENV_VAR_2=other … /usr/share/python/example-com/bin/django-admin <command>

You could use `envdir <https://cr.yp.to/daemontools/envdir.html>`_ or bash's
``source`` command to expose your environment variables, but **Env-cmd** eases
that further. It allows you to read a configuration file, expose values in
the environment and run a command simply by adding a setuptools entry point
in your ``setup.py``. With the entry point symlinked to ``/usr/bin``, your
command becomes::

    example-com django-admin <command>

Env-cmd:

* Reads a configuration file using the default location provided, or an
  override.
* Exposes configuration values as environment variables.
* Resolves the path of your virtualenv.
* Shells out to the virtualenv command.

Installation
------------

::

    pip install env-cmd

Usage
-----

In ``<yourproject>/cli.py``:

.. code-block:: python

    import env_cmd

    read_environ = env_cmd.read_environ(
        'PRCONFIG',  # name of the env var that allows overriding of the
                     # config path.
        '/etc/yourproject.conf', # default config path.
        {'SOME_ENV_VARIABLE': 'DEFAULT_VALUE', # Some default environment
         'OTHER_VARIABLE': 'OTHER VALUE'},     # variables.
    )
    main = env_cmd.main(read_environ)

In your ``setup.py``:

.. code-block:: python

    setup(
        …
        entry_points={'console_scripts': ['yourproject=yourproject.cli:main']},
    )

Then symlink ``/path/to/virtualenv/bin/yourproject`` to
``/usr/bin/yourproject``.

You can run a command from your virtualenv with::

    yourproject <command>

Override the default config path with::

    PRCONFIG=/path/to/config.conf yourproject <command>

Configuration syntax is the following::

    KEY=value
    OTHER=some other value
    QUOTED="quotes are stripped."
    ALSO='single quotes too'
    WHITESPACE=    is stripped as well.
    # comments work like this

    # empty lines are skipped

If you run a web server with `Gunicorn <http://gunicorn.org/>`_, you can
use the ``on_reload`` hook to read configuration on server reload, allowing
zero-downtime configuration updates:

.. code-block:: python

    # gunicorn.conf.py
    import os

    from yourproject import read_environ

    def on_reload(server):
        server.log.info("Reading environ")
        os.environ = read_environ()
        server.log.info(os.environ)
