import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import re
import logging

def retrieve_distillation_profile(crudeName, snapshot='recent'):
    logger = logging.getLogger("Distillationprofileapp.retrievedistillationprofile")

    # Base url to fetch the distillation profile from crudemonitor.ca
    url = "https://www.crudemonitor.ca/crudes/dist.php?acr=CRUDE&time=snapshot"
    # Replace the url with crudename and snapshot
    url = url.replace("CRUDE", crudeName)
    new_url = url.replace("snapshot", snapshot)

    logger.info("Retrieving DP from %s", new_url)
    try:
        response = requests.get(new_url)
        if response.status_code != 200:
            logger.error("request url failed with response code: %s", response.status_code)
            exit(1)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
        exit(1)

    # Create soup object from the response content from the previous requests
    soup = BeautifulSoup(response.text, 'lxml')
    # Finding the Distillation profile table from the response content
    table = soup.find('table', class_="table table-sm table-striped")
    # Check if the Distillation profile table is present
    if not table:
        logger.error("Distillation profile table does not exist. URL requsted: %s ", new_url)
        exit(1)

    # Create the hader for the data frame
    headers = ["mass_recovered", "temperature", "average", "standard_deviation"]
    mydata = pd.DataFrame(columns=headers)

    # Retrieve the body of the distillation profile table from table object
    # and iterate to get the values
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        distillation_rows = []
        header = row.find('th')
        distillation_rows.append(header.text)
        # Iterate through the fields that are represented on in celsius
        for tdata in row.find_all('td', {"class": "celsius"}):
            distillation_rows.append(tdata.text)
        length = len(mydata)
        mydata.loc[length] = distillation_rows

    return mydata


def calculate_distillation_profile(df_crude_one, df_crude_two):
    logger = logging.getLogger("Distillationprofileapp.calculatedistillationprofile")

    logger.info("Calculating distillation profile for the mixture of crude")

    # Drop the Initial Boiling point from the dataframe
    df_crude_one.drop(df_crude_one.loc[df_crude_one['mass_recovered'] == "IBP"].index, inplace=True)
    df_crude_two.drop(df_crude_one.loc[df_crude_one['mass_recovered'] == "IBP"].index, inplace=True)

    # Create dataframe only with mass recovered and the temperature
    df_dp_crude_one = df_crude_one.apply(
        lambda row: pd.Series([row['mass_recovered'], row['temperature']], index=['mass_recovered', 'temperature']),
        axis=1)
    df_dp_crude_two = df_crude_two.apply(
        lambda row: pd.Series([row['mass_recovered'], row['temperature']], index=['mass_recovered', 'temperature']),
        axis=1)

    # updating the datatype for temperature column to float to help in processing
    df_dp_crude_one['temperature'] = df_dp_crude_one['temperature'].astype('float64')
    df_dp_crude_two['temperature'] = df_dp_crude_two['temperature'].astype('float64')

    # Calculate the temperature of distillation profile for the mixture of crude
    # by taking average of the temperature of the two crude oil provided.
    df_dp_crude_mixture = df_dp_crude_one.merge(df_dp_crude_two, on='mass_recovered')
    df_dp_crude_mixture["temperature"] = \
        round((df_dp_crude_mixture["temperature_x"] + df_dp_crude_mixture["temperature_y"]) / 2, 2)

    df_dp_crude_mixture = df_dp_crude_mixture.apply(
        lambda row: pd.Series([row['mass_recovered'], row['temperature']], index=['mass_recovered', 'temperature']),
        axis=1)

    return df_dp_crude_mixture
