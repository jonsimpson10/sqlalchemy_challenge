from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

app = Flask(__name__)

#Database set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route('/')
def index():
    return (
        f"This is the home page.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<br/>"
        f"/api/v1.0/range/"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precip = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        precip.append(prcp_dict)

    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    stations = []
    for station, name, latitude, longitude, elevation in results:
        stn_dict = {}
        stn_dict['station'] = station
        stn_dict['name'] = name
        stn_dict['latitude'] = latitude
        stn_dict['longitude'] = longitude
        stn_dict['elevation'] = elevation
        stations.append(stn_dict)

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    session = Session(engine)
    data = [Measurement.date, Measurement.tobs]
    results = session.query(*data).\
        filter(Measurement.date >= last_year).\
        filter(Measurement.station == 'USC00519281')
    session.close()

    temps = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['temp'] = tobs
        temps.append(temp_dict)

    return jsonify(temps)

@app.route('/api/v1.0/start/')
def start():
        
    return "Append your start date to the end of the url in YYYY-MM-DD format."

@app.route('/api/v1.0/start/<start_date>')
def trip_date(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()
    
    return jsonify(results)

@app.route('/api/v1.0/range/')
def range():

    return 'Append your start date/end date to the url in the following format: YYYY-MM-DD/YYYY-MM-DD'

@app.route('/api/v1.0/range/<start_date>/<end_date>')
def trip_range(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)