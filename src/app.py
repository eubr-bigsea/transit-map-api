#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from flask import Flask

from flask.ext.cors import CORS
import json
from bigsea.transitmap import model

from bigsea.transitmap import dbutil

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/<hh_mm>')
def index(hh_mm):
    hh_mm = hh_mm if hh_mm else datetime.datetime.now().strftime("%H%M")
    trips = model.get_trips_by_minute(hh_mm)

    return json.dumps(trips, indent=4)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
