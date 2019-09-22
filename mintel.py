import requests
import socket
import pandas as pd
import re
import json
import os


# function to get a list of users from wikipedia
# inputs: number of loops to perform
def obtain_ip(loop_count):
    try:
        wikipedia_total = []
        # loop to get more results as each call is limited to rclimit of 10000
        for i in range(loop_count):
            wiki_request = requests.get(url='https://en.wikipedia.org/w/api.php?action=query&list=recentchanges&rclimit=10000&rcprop=user&format=json')  # perform get request for wiki recent changes info
            wiki_data = wiki_request.json()  # extract wiki
            # append each set of results to the main wikipedia_full list
            for d in wiki_data['query']['recentchanges']:
                wikipedia_total.append(d)
        return wikipedia_total
    except requests.exceptions.RequestException as e:
        print(e)


# function extract ip addresses for later use
# input: list of users
# returns: list of valid ips
def parse_user_ips(users):
    valid_ip_list = []
    for u in users:
        try:
            # find IP Version 6 addresses and IP Version 4
            if (re.search('([A-F0-9]{1,4}:){7}', u['user'])) or (socket.inet_aton(u['user'])):
                valid_ip_list.append(u['user'])
        except socket.error as e:
            pass
    return valid_ip_list


# function uses ipstack api to get geolocation information
# input: list of ips
# returns: dictionary for city, region and country coords
def obtain_geolocation(ips):
    # initialise empty dicts
    city_dict = {}
    region_dict = {}
    country_dict = {}

    ipstack_api_key = 'b5f01d148610e9ccfeb179dd2e69665c'  # ipstack API key
    for ip in ips:
        try:
            included_fields = '&fields=latitude,longitude,city,region_name,country_name'  # include only required geo fields from api response
            ip_url = 'http://api.ipstack.com/' + ip + '?access_key=' + ipstack_api_key + included_fields  # build api call url
            jsn_ip = requests.get(ip_url)  # send request to api
            ip_result = jsn_ip.json()
            geo_lat = str(ip_result['latitude'])  # Set the Latitude
            geo_lon = str(ip_result['longitude'])  # Set the Longitude
            geo_city = str(ip_result['city'])  # Set the city
            geo_region = str(ip_result['region_name'])  # Set the region name
            geo_country = str(ip_result['country_name'])  # Set the country

            if str(ip_result['latitude']) != 'None':  # check added as very rarely an ip address would return with fields set to None
                # organise data into dicts by city, region and country
                if geo_city not in city_dict:
                    city_dict.update({geo_city: [geo_lat, geo_lon]})
                if geo_region not in region_dict:
                    region_dict.update({geo_region: [geo_lat, geo_lon]})
                if geo_country not in country_dict:
                    country_dict.update({geo_country: [geo_lat, geo_lon]})

        except requests.exceptions.RequestException as e:
            print(e)
    return city_dict, region_dict, country_dict


# function to get weather data from darksky
# inputs: dictionary of coords
# returns: dictionary of temperature, precipProbability, windSpeed and humidity
def get_weather_data(geo_data):
    api_key = '42fc73a7506af878ed7d2fae95cee144'  # darksky API key
    weather_main_dict = {}
    for k in geo_data:
        try:
            excluded_blocks = '?exclude=minutely,hourly,daily,alerts,flags'  # exclude data blocks from api response
            included_units = '?units=temperature,precipProbability,windSpeed,humidity'  # include only required weather units from api response
            request_url = 'https://api.darksky.net/forecast/' + api_key + '/' + geo_data[k][0] + ',' + geo_data[k][1] + excluded_blocks + included_units
            coord_weather_request = requests.get(url=request_url)  # perform api call
            coord_weather_data = coord_weather_request.json()  # extracting weather data in json
            coord_weather_data = coord_weather_data['currently']  # reset var to only include current weather details
            instance_weather_dict = {k: {'Temperature (f)': coord_weather_data['temperature'], 'PrecipProb (%)': coord_weather_data['precipProbability'] * 100, 'Wind speed (mps)': coord_weather_data['windSpeed'], 'Humidity (%)': coord_weather_data['humidity']}}
            weather_main_dict.update(instance_weather_dict)  # build main weather dictionary
        except requests.exceptions.RequestException as e:
            print(e)
    return weather_main_dict


# function to display data as dataframes to screen
# inputs: dictionary of weather data by location and max columns to display
def dataframe_generator(data_dict, columns):
    df = pd.DataFrame(data_dict)
    pd.set_option('display.max_columns', columns)
    print(df)


if __name__ == "__main__":

    user_list = obtain_ip(5)  # get list of users from wikipedia
    ip_list = parse_user_ips(user_list)  # parse user list to extract only valid ip addresses
    print('############################################')
    print('number of ip addresses being parsed: ' + (str(len(ip_list))))
    print('############################################')
    print('processing please wait...')

    # TODO: possible optimisation required (slow)
    geo_list = [obtain_geolocation(ip_list)]

    # TODO: possible optimisation required (slow)
    city_weather = get_weather_data(geo_list[0][0])
    region_weather = get_weather_data(geo_list[0][1])
    country_weather = get_weather_data(geo_list[0][2])

    # Output data to screen in panda dataframes
    print('-------------------------------------------')
    print('Weather by City: ')
    dataframe_generator(city_weather, 50)
    print('-------------------------------------------')
    print('Weather by Region: ')
    dataframe_generator(region_weather, 50)
    print('-------------------------------------------')
    print('Weather by Country: ')
    dataframe_generator(country_weather, 50)
    print('-------------------------------------------')
    print('')
    # Output data to screen in dictionary form
    print('City data dictionary:')
    print(city_weather)
    print('Region data dictionary:')
    print(region_weather)
    print('Country data dictionary:')
    print(country_weather)



