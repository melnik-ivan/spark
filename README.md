# Spark

A simple messenger based on WebSockets

## Getting Started

### Requirements

To run the project you will need:
* Python 3.5.2 or later
* Tornado 4.5.2
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

## Running
Preparatory actions:
* In the file `spark_app.py` change the variables HOST and PORT in accordance with the settings of your host
* In the file `static/scripts/main.js` also change the variables HOST and PORT

Run server:
```bash
python PROJECT_PATH/spark_app.py
```
For check, go to the address `YOUR_HOST:YOUR_PORT` in your browser on several tabs and try to send yourself a message

## Built With

* [Tornado](http://www.tornadoweb.org/en/stable/) - The non-blocking web server and web application framework

## Authors

* **Melnik Ivan** - [github profile](https://github.com/melnik-ivan)
