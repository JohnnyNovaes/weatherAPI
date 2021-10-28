# 1 Weather API :sunny: :umbrella: :cloud: :snowflake:

The Weather API is used to collect the weather data from multiple places.
You'll have access to the humidity and temperature instantaneous of the places.


# 2 Quick Tour
<img src="https://raw.githubusercontent.com/aio-libs/aiohttp/master/docs/aiohttp-plain.svg" alt="alt text" width="50"/> <img src="https://dbdb.io/media/logos/tinydb.png" alt="alt text" width="150"/> 
<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="alt text" width="125"/>
<img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/horizontal-logo-monochromatic-white.png?itok=SBlK2TGU" alt="alt text" width="125"/> <img src="https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png" alt="alt text" width="125"/>


This project uses the technologies above to make all work. For the database was used the [TinyDB](https://tinydb.readthedocs.io/en/latest/) to manage a simple JSON file that saves the weather data for each request.

To make the API was using the [FastAPI](https://fastapi.tiangolo.com/). A web framework for building fast and reliable APIs.

For the weather data was use the [OpenWeather](https://openweathermap.org/api) API.

In this project, since the API make requests for 168 cities was use the [AIOHTTP](https://docs.aiohttp.org/en/stable/) for asynchronous HTTP requests.

In the end, to make it all very easy to work with as used the already known [Docker](docker) to make isolated environments that can be executed in any machine!

### 2.1 POST and GET
This API has simple functionality. For the **GET** it receives the User ID for the POST request and returns the number of cities already completed.
The **POST** request returns the JSON database file with the user ID and the weather data of the 168 cities.

# 3 How to run it
Follow the next steps very careful.

**1°** Clone the repository to your desktop.

`git clone https://github.com/JohnnyNovaes/weatherAPI.git`

**2°** Register into the [OpenWeather](https://openweathermap.org/api) API for the **API KEY**.

**3°** Put the API KEY from OpenWeather API into the file **apiKEY.txt**.

**4°** Build the docker image using the **Dockerfile**.
     
`docker build -t myimage .`

**5°** Run a container with the image created.

`docker run -d --name mycontainer -p 80:80 myimage`

**6°** Type into your browser: **0.0.0.0/docs**.
