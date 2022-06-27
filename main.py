import time
import sys
import json
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Forecast, Observation

COORDINATES = {'lat': '57.7088', 'lon': '11.9745'}
DB_URL = "sqlite:///weather_data.db"


engine = create_engine(DB_URL, echo=False, future=True)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)


def read_sql_to_pandas(table_name):
    return pd.read_sql_table(table_name=table_name, con=DB_URL)


def get_yr_forecast():
    """
    Retrieve forecast data from YR via their API
    """

    url = f"https://api.met.no/weatherapi/locationforecast/2.0/complete"
    headers = {'User-Agent': 'https://github.com/Frallmeister'}

    r = requests.get(url, params=COORDINATES, headers=headers)
    return r.json()


def get_smhi_forecast():
    lon = COORDINATES['lon']
    lat = COORDINATES['lat']
    entry_point = "https://opendata-download-metfcst.smhi.se"
    url = f"/api/category/pmp3g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json"

    r = requests.get(entry_point + url)
    return r.json()


def get_smhi_observation():
    station_number = 71420
    entry_point = "https://opendata-download-metobs.smhi.se/api/"
    query = f"version/latest/station/{station_number}/period/latest-hour/data.json"

    r = requests.get(entry_point + query)
    return r


def parse_cloud_area(value):
    """

    """
    pass


def parameters():
    results = {}
    url = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/{}/station/72420/period/latest-hour/data.json"
    # for i in [1, 3, 4, 6, 7, 9, 12, 13, 14, 21, 25, 26, 27, 38, 39]:
    print(url)
    for i in range(40):
        r = requests.get(url.format(i))
        if r.ok:
            data = r.json()
            name = data['parameter']['name']
            summary = data['parameter']['summary']
            unit = data['parameter']['unit']
            results[i] = {'name': name, 'summary': summary, 'unit': unit}
            print(i, " | ", name, " | ", summary)
        time.sleep(1)
        # print(i, r.ok)
    return results





def main():

    # Get YR forecast
    # yr_data = get_yr_forecast()
    # with open("yr_response.json", "w") as f:
    #     json.dump(yr_data, f, indent=2)

    # Get SMHI forecast
    # smhi_data = get_smhi_forecast()
    # with open("smhi_response.json", "w") as f:
    #     json.dump(smhi_data, f, indent=2)

    df = read_sql_to_pandas("observation")
    return df

if __name__== '__main__':
    out = main()
    with open("smhi_response.json") as f:
        data = json.load(f)
    ts = data['timeSeries']


    # summary = {
    #     "name": set(),
    #     "levelType": set(),
    #     "level": set(),
    #     "unit": set()
    #     }
    # for d in ts:
    #     params = d['parameters']
    #     for param in params:
    #         for k in summary.keys():
    #             summary[k].add(param[k])
