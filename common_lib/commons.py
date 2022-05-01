import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import re


def retrieve_distillation_profile(crudeName):
    url = "https://www.crudemonitor.ca/crudes/dist.php?acr=CRUDE&time=recent"
    new_url = url.replace("CRUDE", crudeName)
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', class_="table table-sm table-striped")

    headers = ["mass_recovered", "temperature", "average", "standard_deviation"]
    mydata = pd.DataFrame(columns=headers)

    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        distillation_rows = []
        header = row.find('th')
        distillation_rows.append(header.text)
        for tdata in row.find_all('td', {"class": "celsius"}):
            distillation_rows.append(tdata.text)
        length = len(mydata)
        mydata.loc[length] = distillation_rows

    # print(mydata)
    return mydata


def calculate_distillation_profile(df_crude_one, df_crude_two):
    df_crude_one.drop(df_crude_one.loc[df_crude_one['mass_recovered'] == "IBP"].index, inplace=True)
    df_crude_two.drop(df_crude_one.loc[df_crude_one['mass_recovered'] == "IBP"].index, inplace=True)

    df_dp_crude_one = df_crude_one.apply(
        lambda row: pd.Series([row['mass_recovered'], row['temperature']], index=['mass_recovered', 'temperature']),
        axis=1)
    df_dp_crude_two = df_crude_two.apply(
        lambda row: pd.Series([row['mass_recovered'], row['temperature']], index=['mass_recovered', 'temperature']),
        axis=1)

    df_dp_crude_one['temperature'] = df_dp_crude_one['temperature'].astype('float64')
    df_dp_crude_two['temperature'] = df_dp_crude_two['temperature'].astype('float64')

    df_dp_crude_mixture = df_dp_crude_one.merge(df_dp_crude_two, on='mass_recovered')
    df_dp_crude_mixture["temperature"] = \
        round((df_dp_crude_mixture["temperature_x"] + df_dp_crude_mixture["temperature_y"]) / 2, 2)

    df_dp_crude_mixture = df_dp_crude_mixture.apply(
        lambda row: pd.Series([row['mass_recovered'], row['temperature']], index=['mass_recovered', 'temperature']),
        axis=1)

    return df_dp_crude_mixture
