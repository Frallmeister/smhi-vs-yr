import logging
import uuid
import time
import datetime
import sys
import json
import requests
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, MetData
from conversions import SMHI_NAMES, PARAM_STATIONS
from log import configure_logging

import http.client as http_client
http_client.HTTPConnection.debuglevel = 1
configure_logging()
logger = logging.getLogger(__name__)
logger.propagate = True

COORDINATES = {'lat': '57.7088', 'lon': '11.9745'}
DB_URL = "sqlite:///weather_data.db"

engine = create_engine(DB_URL, echo=False, future=True)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)


def read_sql_to_pandas(table_name):
    """

    """
    logger.info("RUNNING: read_sql_to_pandas('%s')", table_name)
    return pd.read_sql_table(table_name=table_name, con=DB_URL)


def get_yr_forecast():
    """
    Retrieve forecast data from YR via their API
    """

    logger.info("RUNNING: get_yr_forecast()")
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/complete"
    headers = {'User-Agent': 'https://github.com/Frallmeister'}

    r = requests.get(url, params=COORDINATES, headers=headers)
    return r.json()


def get_smhi_forecast():
    """
    Retrieve forecast data from SMHI via their API
    """

    logger.info("RUNNING: get_smhi_forecast()")
    lon = COORDINATES['lon']
    lat = COORDINATES['lat']
    entry_point = "https://opendata-download-metfcst.smhi.se"
    url = f"/api/category/pmp3g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json"

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    r = requests.get(entry_point + url, headers=headers)
    return r.json()


def get_smhi_observation():

    logger.info("RUNNING: get_smhi_observation()")
    entry_point = "https://opendata-download-metobs.smhi.se/api/"
    query = "version/latest/parameter/{}/station/{}/period/latest-hour/data.json"

    observations = list()
    for param, station, summary in PARAM_STATIONS:
        logger.debug("param=%s, station=%s, summary=%s", param, station, summary)
        r = requests.get(entry_point + query.format(param, station))
        data = r.json()

        parameter = summary
        unit = data['parameter']['unit']
        value = None if data['value'] is None else data['value'][0]['value']
        date_updated = data['updated']
        valid_time = datetime.datetime.fromtimestamp(int(date_updated / 1000))
        observation = dict(
            parameter=parameter,
            value=value,
            unit=unit,
            valid_time=valid_time,
        )
        observations.append(observation)
        time.sleep(1)

    return observations


def process_yr_forecast(data: dict) -> list:
    """
    Parse the raw YR forecast into a format suitable for inserting in the DB.

    Returns a list of dictionaries with the following fields:
        - parameter: Name of forecasted property (STRING)
        - value: The value of the (STRING)
        - unit: 
        - valid_time:
    """

    logger.info("RUNNING: process_yr_forecast()")
    processed_data = list()
    
    meta = data['properties']['meta']
    units = meta['units']

    timeseries = data['properties']['timeseries']
    for record in timeseries:
        valid_time = datetime.datetime.strptime(record['time'], "%Y-%m-%dT%H:%M:%SZ")
        if valid_time.hour % 6 == 0:
            details = record['data']['instant']['details']
            for parameter, value in details.items():
                item = dict(
                    parameter=parameter,
                    value=value,
                    unit=units[parameter],
                    valid_time=valid_time,
                )
                processed_data.append(item)

            
            if 'next_6_hours' in record['data'].keys():
                details = record['data']['next_6_hours']['details']
                for parameter, value in details.items():
                    item = dict(
                        parameter=parameter,
                        value=value,
                        unit=units[parameter],
                        valid_time=valid_time,
                    )
                    processed_data.append(item)
    return processed_data
                

def process_smhi_forecast(data: dict) -> dict:
    """
    Parse the raw SMHI forecast into a dict that matches the DB table
    """
    
    logger.info("RUNNING: process_smhi_forecast()")
    processed_data = list()
    timeseries = data['timeSeries']
    for forecast in timeseries:
        valid_time = forecast['validTime']
        parameters = forecast['parameters']
        valid_time = datetime.datetime.strptime(valid_time, "%Y-%m-%dT%H:%M:%SZ")
        if valid_time.hour % 6 == 0:
            for parameter in parameters:
                mapped_param = SMHI_NAMES[parameter['name']]
                item = dict(
                    parameter=mapped_param,
                    value=parameter['values'][0],
                    unit=parameter['unit'],
                    valid_time=valid_time,
                )
            processed_data.append(item)
    return processed_data


def insert_data(payload: list, upload_id: str, retrieved_time: np.datetime64, variant: str, source: str):
    """
    Insert data in the database
    Args:
        payload: Data to insert.
        upload_id: A unique identifier
        retrieved_time: Datetime
        variant: 'forecast' or 'observation'.
        source: 'YR' or 'SMHI'
    """

    logger.info("RUNNING: insert_data()")
    with Session() as session:
        for record in payload:
            record['upload_id'] = upload_id
            record['retrieved_time'] = retrieved_time
            record['variant'] = variant
            record['source'] = source
            item = MetData(**record)
            session.add(item)
        session.commit()


def save_data(payload: list, variant: str, source: str):
    """
    Get forecasts from YR and SMHI and save them in the database

    Arguments:
        payload: List with processed weather data.
        variant: Either "forecast" or "observation".
        source: Either "SMHI" or "YR".
    """

    logger.info("RUNNING: save_data()")
    upload_id = str(uuid.uuid4())
    retrieved_time = datetime.datetime.now()
    
    insert_data(
        payload=payload,
        upload_id=upload_id,
        retrieved_time=retrieved_time,
        variant=variant,
        source=source
        )


def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("\n\n###### Running main() ######")
    logger.info("Current time: %s", current_time)

    # Retrieve, parse and save YR forecast data
    logger.info("GET YR forecast")
    yr_raw = get_yr_forecast()
    yr_processed = process_yr_forecast(yr_raw)
    save_data(payload=yr_processed, variant="forecast", source="YR")

    # Retrieve, parse and save SMHI forecast data
    logger.info("GET SMHI forecast")
    smhi_raw = get_smhi_forecast()
    smhi_processed = process_smhi_forecast(smhi_raw)
    save_data(payload=smhi_processed, variant="forecast", source="SMHI")

    # Retrieve, parse and save SMHI observation data
    logger.info("GET SMHI observations")
    observations = get_smhi_observation()
    save_data(payload=observations, variant="observation", source="SMHI")
    return yr_processed, smhi_processed, observations


if __name__== '__main__':
    main()