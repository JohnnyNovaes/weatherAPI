import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import datetime
from tinydb import TinyDB, Query
import aiohttp
import asyncio
app = FastAPI()


class InputsPost(BaseModel):
    id: int


@app.get("/")
async def root(data: InputsPost):
    return {"message": "Hello World"}


@app.post('/show_data')
async def show_data(data_in: InputsPost):
    # build or create json database
    database = TinyDB('weather_data.json')

    # authorization user unique id
    input_user = Query()
    if database.search(input_user.userID == data_in.id):
        raise HTTPException(status_code=401, detail=f"There's already the User ID: {data_in.id} in database")

    # load list of cities IDs
    with open('cities.txt', 'rb') as open_file:
        city_ids = json.load(open_file)

    # all cities weather data
    progress = 0    # show the progress of requests

    async with aiohttp.ClientSession() as session:

        for city_id in city_ids:
            # weather url
            weather_url = "http://api.openweathermap.org/data/2.5/weather?id="+str(city_id)+"&appid=b2626a09f300fa0361d32b9ef5b208ff&units=metric"
            # start async request
            async with session.get(weather_url) as resp:
                response = await resp.json()

                # create the dict with weather data
                if progress == 0:
                    weather_report = {
                        'localtime': json.dumps(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))),
                        'userID': data_in.id,
                        'locals': [
                            {
                                'local_id': city_id,
                                'temp_c': response['main']['temp'],
                                'humidity': response['main']['humidity']
                            }]}
                    progress += 1
                else:
                    add_data = {
                        'local_id': city_id,
                        'temp_c': response['main']['temp'],
                        'humidity': response['main']['humidity']
                                }
                    progress += 1
                    # append new local to weather_report
                    weather_report.get('locals').append(add_data)

    database.insert(weather_report)

    return database.search(input_user.userID > 0)

