import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import datetime
from tinydb import TinyDB, Query
from tinydb import where

app = FastAPI()


class InputsPost(BaseModel):
    id: int


@app.get("/")
async def root(data: InputsPost):
    return {"message": "Hello World"}


@app.post('/show_data')
async def show_data(data_in: InputsPost):
    database = TinyDB('weather_data.json')
    # weather request
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?id=" + "3439525" + "&appid=b2626a09f300fa0361d32b9ef5b208ff&units=metric")
    # create the dict with weather data
    weather_report = {
        'localtime': json.dumps(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))),
        'userID': data_in.id,
        'locals': [
            {
                'local_id': 3439525,
                'temp_c': response.json()['main']['temp'],
                'humidity': response.json()['main']['humidity']
            }]}

    add_data = {
        'local_id': 3439525,
        'temp_c': response.json()['main']['temp'],
        'humidity': response.json()['main']['humidity']
                }
    weather_report.get('locals').append(add_data)
    database.insert(weather_report)

    ident = Query()
    return database.search(ident.userID == 1)

