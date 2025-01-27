# Import the dependencies.
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)
# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"            
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date are in the format MMDDYYYY.</p>"
        )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #precipitation data for the last year
    #Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #Query precipitation from the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
@app.route("/api/v1.0/tobs")
def temp():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
@app.route("/api/v1.0/temp/<start>")
def temp_start(start):
    return f"Temperature data for start date: {start}"

@app.route("/api/v1.0/temp/<start>/<end>")
def temp_start_end(start, end):
    return f"Temperature data for start date: {start} and end date: {end}"

if __name__ == '__main__':
    app.run()