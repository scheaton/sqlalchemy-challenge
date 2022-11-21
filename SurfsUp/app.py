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
station_table = Base.classes.station # "station_table" rather than "station" to avoid using a keyword
measurement = Base.classes.measurement

# Flask Setup
app = Flask(__name__)


#################################################
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
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart><br/>"
        f"/api/v1.0/&ltstart>/&ltend>"
    )

@app.route("/api/v1.0/precipitation")
def precipitations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """precipitation"""
    # Query last 12 months of precipitation data from all stations
    results = session.query(measurement.date, measurement.prcp)\
                     .filter(measurement.date > '2016-08-23')\
                     .order_by(measurement.date).all()

    # Create a dictionary with the date as the key and the value as the precipitation from the row data
    # and append to a list of all_precipitations
    all_precipitations = []
    for date, prcp, in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitations.append(precipitation_dict)
    
    session.close()

    # Return JSON 
    return jsonify(all_precipitations)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """stations"""
    # Query all stations
    results = session.query(station_table.station, station_table.name, station_table.latitude, station_table.longitude, station_table.elevation).all()

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

    session.close()

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """tobs"""
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    results = session.query(measurement.date, measurement.tobs)\
                     .filter(measurement.date > '2016-08-23')\
                     .order_by(measurement.date).all()

    session.close()

    # Create a dictionary with the date as the key and the value as the tobs from the row data
    # and append to a list of all_tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """start date"""
    # Return a JSON list of the minimum temperature, average temperature,
    # and maximum temperature since a specified start date
    low_avg_high = session.query(func.min(measurement.tobs), \
                                 func.avg(measurement.tobs), \
                                 func.max(measurement.tobs)) \
                          .filter(measurement.date >= start).first()

    session.close()

    return jsonify({"TMIN": str(low_avg_high[0]),
                    "TAVG": str(low_avg_high[1]),
                    "TMAX": str(low_avg_high[2])})


@app.route("/api/v1.0/<start>/<end>")
def start_to_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """start to end"""
    # Return a JSON list of the minimum temperature, average temperature,
    # and maximum temperature for a specified start-end range.
    low_avg_high = session.query(func.min(measurement.tobs), \
                                 func.avg(measurement.tobs), \
                                 func.max(measurement.tobs)) \
                          .filter(measurement.date >= start)\
                          .filter(measurement.date <= end).first()

    session.close()

    return jsonify({"TMIN": str(low_avg_high[0]),
                    "TAVG": str(low_avg_high[1]),
                    "TMAX": str(low_avg_high[2])})


if __name__ == '__main__':
    app.run(debug=True)
