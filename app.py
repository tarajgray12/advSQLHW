import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start_date><br/>"
        f"/api/v1.0/temp/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp). \
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    stationdata = list(np.ravel(results))
    return jsonify(stationdata)

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tempdata = session.query(Measurement.date, Measurement.tobs). \
        filter(Measurement.date >= prev_year).all()
    tobsdata = list(np.ravel(tempdata))
    return jsonify(tobsdata)

app.route("/api/v1.0/temp/<start_date>")
def start_date(start_date):
    start = session.query("select station, min(tobs), max(tobs), avg(tobs) from Measurement where date >= ? group by(station)", (start_date,)).fetchall()
    return jsonify(start)

@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start_date, end_date):
    dates = session.query("select station, min(tobs), max(tobs), avg(tobs) from Measurement where date >= ? and date <= ? group by(station)", (start_date,end_date,)).fetchall()
    return jsonify(dates)

if __name__ == "__main__":
    app.run(debug=True)
