from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import datetime
from tinydb import TinyDB, Query, where
import aiohttp
import asyncio


app = FastAPI()


class InputsPost(BaseModel):
    id: int


@app.get("/")
async def root(data_in: int):
    # build or create json database
    database = TinyDB('progress.json')

    # search for the progress
    User = Query()
    progress = database.search(User.userID == data_in)

    # return progress
    if not progress:
        raise HTTPException(status_code=404, detail=f"There's no progress for User ID: {data_in} in database")
    else:
        return progress[0]['progress']


@app.post('/show_data')
def show_data(data_in: InputsPost):
    # build or create json database
    database = TinyDB('weather_data.json')

    # authorization user unique id
    input_user = Query()
    if database.search(input_user.userID == data_in.id):
        raise HTTPException(status_code=401, detail=f"There's already the User ID: {data_in.id} in database")

    # weather data async
    asyncio.run(build_database(data_in))
    database = TinyDB('weather_data.json')

    return database.search(input_user.userID > 0)


async def build_database(data_in):
    # build or create json database
    database = TinyDB('weather_data.json')

    # load list of cities IDs
    try:
        with open('cities.txt', 'rb') as open_file:
            city_ids = json.load(open_file)
    except FileNotFoundError:
        raise HTTPException(status_code=401, detail="There is no cities.txt file!")

    # all cities weather data
    flag = True
    # start the async task
    async with aiohttp.ClientSession() as session:

        for city_id in city_ids:
            # weather url
            weather_url = "http://api.openweathermap.org/data/2.5/weather?id=" + str(
                city_id) + "&appid=b2626a09f300fa0361d32b9ef5b208ff&units=metric"
            # start async request
            async with session.get(weather_url) as resp:
                response = await resp.json()

                # create the dict with weather data
                if flag:
                    weather_report = {
                        'localtime': json.dumps(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))),
                        'userID': data_in.id,
                        'locals': [
                            {
                                'local_id': city_id,
                                'temp_c': response['main']['temp'],
                                'humidity': response['main']['humidity']
                            }]}
                    # progress database
                    progress_base = TinyDB('progress.json')
                    percent = (len(weather_report.get('locals'))/167)*100
                    progress = {'userID': data_in.id, 'progress': percent}
                    progress_base.insert(progress)

                    # set flag
                    flag = False
                else:
                    add_data = {
                        'local_id': city_id,
                        'temp_c': response['main']['temp'],
                        'humidity': response['main']['humidity']
                    }
                    # append new local to weather_report
                    weather_report.get('locals').append(add_data)

                    # safe progress
                    progress_base = TinyDB('progress.json')
                    percent = int((len(weather_report.get('locals'))/167)*100)
                    User = Query()
                    progress_base.update({'progress': percent}, User.userID == data_in.id)

        database.insert(weather_report)
