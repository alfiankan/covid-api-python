from flask.app import Flask
import flask_unittest
import pytest
from http_server import app

def testGetGeneralInformation():
    flask_app = app()

    response = flask_app.get('/')


    assert 1 == 4
