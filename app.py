import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())
# Save reference to the table
m = Base.classes.measurement
s = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (f"W/api/v1.0/precipitation"
            f"/api/v1.0/stations"
            f"/api/v1.0/tobs"
            f"/api/v1.0/<start>"
            f"/api/v1.0/<start>/<end>"
            )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data including the date and precipitation"""
    # Query all precipitation 
    results = session.query(m.date, m.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    all_precipitation= []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of stations from the data set """
    # Query all stations
    results = session.query(s.station, s.name, s.latitude, s.longitude, s.elevation).all()

    session.close()

     # Create a dictionary from the row data and append to a list 
    all_stations= []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["Elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of stations from the data set """
    # Query all stations
    USC00519281 = session.query(m.tobs,m.date).\
             filter(m.station == 'USC00519281').\
             filter(m.date >= '2016-08-23').filter(m.date <= '2017-08-23').all()

    session.close()

    active_tobs = []
    for tobs, date in USC00519281:
        station_dict = {}
        station_dict["tobs"]=tobs
        station_dict["date"]=date
        active_tobs.append(station_dict)
    return jsonify(active_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of stations from the data set """
    # Query all stations
    results = session.query(func.min(m.tobs),func.max(m.tobs),func.avg(m.tobs)).\
             filter(m.date >= start).all()

    session.close()

    start_tobs = []
    for min, max, avg in results:
        start_dict = {}
        start_dict["Min"]=min
        start_dict["Max"]=max
        start_dict["Average"]=avg
        start_tobs.append(start_dict)
    return jsonify(start_tobs)


@app.route("/api/v1.0/<start>/<end>")
def startEnd(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of stations from the data set """
    # Query all stations
    results = session.query(func.min(m.tobs),func.max(m.tobs),func.avg(m.tobs)).\
             filter(m.date >= start).filter(m.date <= end).all()

    session.close()

    startEnd_tobs = []
    for min, max, avg in results:
        startEnd_dict = {}
        startEnd_dict["Min"]=min
        startEnd_dict["Max"]=max
        startEnd_dict["Average"]=avg
        startEnd_tobs.append(startEnd_dict)
    return jsonify(startEnd_tobs)



    
    
        


if __name__ == '__main__':
    app.run(debug=True)
