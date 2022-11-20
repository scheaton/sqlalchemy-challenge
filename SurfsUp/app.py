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

# Save reference to the table
Stations = Base.classes.station
Measurements = Base.classes.measurement

# Flask Setup
app = Flask(__name__)


# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<u><h3>Available Routes</h3></u>"
        "<strong>*input dates as yyyy-mm-dd</strong><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/&ltstart><br/>"
        f"/api/v1.0/&ltstart>/&ltend>"
    )

@app.route("/api/v1.0/precipitation")
def precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """precipitation"""
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
    # to a dictionary using date as the key and prcp as the value.
    results = session.query(Measurements.date, Measurements.prcp)\
                     .filter(Measurements.date > '2016-08-23')\
                     .order_by(Measurements.date).all()

    all_precipitations = []
    for date, prcp, in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitations.append(precipitation_dict)
    
    session.close()

    return jsonify(all_precipitations)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all Stations
    results = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of tobs from the dataset."""
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    results = session.query(Measurements.date, Measurements.tobs)\
                     .filter(Measurements.date > '2016-08-23')\
                     .order_by(Measurements.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """start date"""
    # Return a JSON list of the minimum temperature, the average temperature,
    # and the maximum temperature for a specified start or start-end range.
    low_high_avg = session.query(func.min(Measurements.tobs), \
                                 func.max(Measurements.tobs), \
                                 func.avg(Measurements.tobs)) \
                          .filter(Measurements.date > start).first()

    session.close()

    return jsonify({"TMIN": str(low_high_avg[0]),
                    "TAVG": str(low_high_avg[1]),
                    "TMAX": str(low_high_avg[2])})


@app.route("/api/v1.0/<start>/<end>")
def start_to_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """start date"""
    # Return a JSON list of the minimum temperature, the average temperature,
    # and the maximum temperature for a specified start or start-end range.
    low_high_avg = session.query(func.min(Measurements.tobs), \
                                 func.max(Measurements.tobs), \
                                 func.avg(Measurements.tobs)) \
                          .filter(Measurements.date > start)\
                          .filter(Measurements.date < end).first()

    session.close()

    return jsonify({"TMIN": str(low_high_avg[0]),
                    "TAVG": str(low_high_avg[1]),
                    "TMAX": str(low_high_avg[2])})


if __name__ == '__main__':
    app.run(debug=True)
