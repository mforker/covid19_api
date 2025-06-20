from fastapi import FastAPI
from typing import Optional
from utils.scraper import get_statewise_historical_data, get_list_of_states,get_current_data_india, get_statewise_current_data
import json

app = FastAPI(
    title="COVID-19 Data API",
    description="A FastAPI-based web API for accessing historical and current COVID-19 data for various states and union territories in India.",
    version="1.0.0",
    contact={
        "name": "Mitesh",
        "url": "https://github.com/mforker"
    })

@app.get("/", description="Welcome message")
def root():
    return {"message": "Hi, i am Mitesh and i am happy to provide you the COVID-19 Data API."}

@app.get("/states_ut_list", description="Provides list of states you can get data for.")
def states_list():
    return {"states_ut": get_list_of_states()}


@app.get("/historical_data/states/{states_str}", description="Comma separated list of states.")
def historical_states_data(states_str: str):
    if states_str is None:
        return {"states": []}
    states_lower = str(states_str).lower().title()
    states = states_lower.split(',')
    states = [x.strip() for x in states]
    data = get_statewise_historical_data(states)
    return json.loads(data, strict=False)

@app.get("/current_data/india", description="Current data for India.")
def current_data_india():
    data = get_current_data_india()
    return json.loads(data, strict=False)

@app.get("/current_data/states/{states_str}", description="Comma separated list of states.")
def current_states_data(states_str: str):
    if states_str is None:
        return {"states": []}
    states_lower = str(states_str).lower().title()
    if ',' in states_lower:
        states = states_lower.split(',')
        states = [x.strip() for x in states]
    else:
        states = states_lower
    data = get_statewise_current_data(states)

    return data