# Some minimal RPC examples in python

## Contents
- `synchronous`: Synchronous RPC example
- `asynchronous`: Asynchronous RPC example using callbacks (aka "deferred synchronous RPC")

## Running the examples
The only requirement is the rpyc library. Better create a virtual environment, install rpyc and execute the server and the client as follows.
```
virtualenv -p python3 venv
. venv/bin/activate
pip install rpyc
python server.py
python client.py
```
Please note that IP addresses and port numbers are hardcoded, and it is assumed that both the client and the server run on the same machine. You need to edit the source to change these settings.

