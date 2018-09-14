# Spark

A simple messenger based on WebSockets

## Getting Started

### Implementation Notes

Spark relies on the support provided by the default S2I builder for deploying a WSGI application using the ``gunicorn`` WSGI server. The requirements which need to be satisfied for this to work are:

* The WSGI application code file needs to be named ``wsgi.py``.
* The WSGI application entry point within the code file needs to be named ``application``.
* The ``gunicorn`` package must be listed in the ``requirements.txt`` file for ``pip``.

In addition, the ``.s2i/environment`` file has been created to allow environment variables to be set to override the behaviour of the default S2I builder for Python.

* The environment variable ``APP_CONFIG`` has been set to declare the name of the config file for ``gunicorn``.
* The environment variable ``GUNICORN_CMD_ARGS`` has been set worker_class to ``tornado`` for ``gunicorn``.

### Requirements

To run the project you will need:
* Python 3.5.2 or later
* Tornado 4.5.2
* Gunicorn 19.7.1
* virtualenv - optional

#### Setting up a virtual environment:

Creating a virtual environment:

```bash
virtualenv -p python3 ~/envs/env #choose a suitable place for a new environment
```

Activation of the virtual environment:

```bash
source ~/envs/env/bin/activate
```
#### Requirements installation:
```bash
cd PROJECT_PATH
pip install -r requirements.txt
```

## Running development server
Preparatory actions:
* In the file `spark_app.py` change the variable HOST to `http://127.0.0.1:8000`
* In the file `static/scripts/main.js` also change the variable wsHOST to `ws://127.0.0.1:8000/ws`

Run development server:
```bash
cd PROJECT_PATH
gunicorn -k tornado wsgi:application
```
For check, go to the address `http://127.0.0.1:8000` in your browser on several tabs and try to send yourself a message

## Deployment Steps (OpenShift)

To deploy from the OpenShift web console, you should select ``python:3.5`` or ``python:latest``, when using _Add to project_. Use of ``python:latest`` is the same as having selected the most up to date Python version available, which at this time is ``python:3.5``.

The HTTPS URL of this code repository which should be supplied to the _Git Repository URL_ field when using _Add to project_ is:

* https://github.com/melnik-ivan/spark.git

If using the ``oc`` command line tool instead of the OpenShift web console, to deploy, you can run:

```
oc new-app https://github.com/melnik-ivan/spark.git
```

In this case, because no language type was specified, OpenShift will determine the language by inspecting the code repository. Because the code repository contains a ``requirements.txt``, it will subsequently be interpreted as including a Python application. When such automatic detection is used, ``python:latest`` will be used.

If needing to select a specific Python version when using ``oc new-app``, you should instead use the form:

```
oc new-app python:3.5~https://github.com/melnik-ivan/spark.git
```

See more:
* [os-sample-python](https://github.com/OpenShiftDemos/os-sample-python)
* [nodejs-ex](https://github.com/openshift/nodejs-ex)

## Built With

* [Tornado](http://www.tornadoweb.org/en/stable/) - The non-blocking web server and web application framework

## Authors

* **Melnik Ivan** - [github profile](https://github.com/melnik-ivan)
