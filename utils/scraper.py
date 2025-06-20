from bs4 import BeautifulSoup, Tag
import requests
import pandas as pd
import json
import datetime
import os

d1 = pd.read_csv('data/state_wise_cases_31_jan_2020-5_may_2023.csv')
d2 = pd.read_csv('data/state_wise_cases_6_may_2023-31_Dec_2024.csv')

states = [x for x in d2['State/UT'].to_list() if x in d1['State/UT'].to_list()] 


data = pd.concat([d1, d2], ignore_index=True)
cols = ['Cumulative_Cases_(Including_Foreigners)', 'Discharged/Cured/Migrated', 'Deaths']
aggregated_data = data.groupby('State/UT')[cols].sum().reset_index()

'''total state/ut wise cases from 31st jan 2020 to 31st dec 2024'''
aggregated_data = aggregated_data[aggregated_data['State/UT'] != 'TOTAL'].reset_index(drop=True)
aggregated_data.columns = ['State_UT', 'Cumulative_Cases', 'Discharged_Cured_Migrated', 'Deaths']
# print(aggregated_data)

def get_list_of_states():
    states = aggregated_data['State_UT'].to_list()
    return states

def get_statewise_historical_data(states:str | list[str]):
    # print(len(set(states).intersection(set(get_list_of_states()))))
    if len(set(states).intersection(set(get_list_of_states()))) == 0:
        return '{"error": "State not found"}'
    if isinstance(states, str):
        state_historical_data = aggregated_data[aggregated_data['State_UT'] == states].reset_index(drop=True).to_json(orient='records')
    else:
        state_historical_data = aggregated_data[aggregated_data['State_UT'].isin(states)].reset_index(drop=True).to_json(orient='records')
    
    data = {'from':'31/01/2020', 'to':'31/12/2024', 'data': json.loads(state_historical_data)}
    return json.dumps(data, indent=4)

def get_current_data_india():
    soup = requests.get(f'https://covid19dashboard.mohfw.gov.in/').text
    page = BeautifulSoup(soup, 'html.parser')
    dashboard = page.find('section', {'id': 'site-dashboard'})
    # print(len(dashboard.find_all('li')))
    active_cases_el, discharged_el, x= (dashboard.find_all('li') if isinstance(dashboard, Tag) else [])

    active_cases = active_cases_el.find_all('span') if isinstance(active_cases_el, Tag) else []
    active_cases_int = int(active_cases[-1].get_text())

    discharged = discharged_el.find_all('span') if isinstance(discharged_el, Tag) else []
    discharged_int = int(discharged[-1].get_text()) 

    df = pd.DataFrame({'datetime': [str(datetime.datetime.now())],'active_cases': [active_cases_int], 'discharged': [discharged_int]})

    if os.path.exists('data/current_data_coillection.csv'):
        db = pd.read_csv('data/current_data_coillection.csv')
        db_new = pd.concat([db, df], ignore_index=True)
        db_new.to_csv('data/current_data_coillection.csv', index=False)
    else:
        df.to_csv('data/current_data_coillection.csv', index=False)

    return df.reset_index(drop=True).to_json(orient='records', indent=4)


def get_statewise_current_data(state: str | list[str]):
    if os.path.exists('data/current_statewise_data.json'):
        file_ctime =  os.path.getctime('data/current_statewise_data.json')
        now = datetime.datetime.now().timestamp()
        time_diff = now - file_ctime
        cache_update_time_in_min = 15
        if time_diff >= 60*cache_update_time_in_min:
            print('removing old data...')
            os.remove('data/current_statewise_data.json')
            print('Updating data...')
            res = requests.get(f'https://covid19dashboard.mohfw.gov.in/data/datanew.json').json()
            with open('data/current_statewise_data.json', 'w') as f:
                json.dump(res, f)
        else:
            print('Using cached data...')
            with open('data/current_statewise_data.json', 'r') as f:
                res = json.load(f)
    
    data = list(res)
    data = data[:-1]
    d = {}

    for obj in data:
        obj_json = dict(obj)
        state_name = obj_json['state_name']
        active_cases = obj_json['new_active']
        cured_cases = obj_json['new_cured']
        deaths = obj_json['new_death']
        d[state_name] = {'active_cases': active_cases, 'cured_cases': cured_cases, 'deaths': deaths}
    
    if isinstance(state, str) and state in d.keys():
        return {state: d[state]}
    elif isinstance(state, list) and all([x in d.keys() for x in state]):
        return {x: d[x] for x in state}
    elif isinstance(state, str) and state in ['All','all','ALL']:
        return d
    else:
        return {'error': 'State not found'}

get_statewise_current_data('Andhra Pradesh')