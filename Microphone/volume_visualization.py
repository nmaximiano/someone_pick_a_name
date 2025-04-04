import json
from matplotlib import pyplot as plt
import time

data = {}

def read_data(file_name : str):
    try:
        # Open file in read mode.
        with open(file_name, "r") as file:
            json_data = json.load(file)
            return json_data
        return None
    except:
        return None

# Tries to grab current data for display.
def update_data():
    return read_data("data/volume_level.json")

def get_last_24_hours_keys():
    # I think I have to do this because of timezone stuff.
    seconds_in_a_day = 86400 + 86400 / 3
    # A better way certainly exists.
    keys = list(data.keys())

    keys.sort()
    keys.reverse()

    keys_to_plot = []

    for key in keys:
        deltatime = abs(int(float(key)) - int(time.time()))
        if abs(deltatime) < abs(seconds_in_a_day):
            keys_to_plot.append(key)
        else:
            # Go until there are no more
            break

    keys_to_plot.reverse()

    return keys_to_plot

def get_volume_for_keys(keys):
    temps = []
    for key in keys:
        temps.append(data[key]["average"])

    return temps

def convert_keys_to_hours(keys):
    seconds_in_an_hour = 3600.0
    current_time = int(time.time())
    hour_keys = []
    for key in keys:
        epoch_difference = current_time - int(float(key))
        hour = epoch_difference / seconds_in_an_hour
        hour_keys.append(-(hour - 8)) # I do not know why this is necessary but it is
    return hour_keys


while True:
    data = update_data()
    plt.clf()

    keys = get_last_24_hours_keys()
    volumes = get_volume_for_keys(keys)


    plt.plot(convert_keys_to_hours(keys), volumes)

    plt.xlabel("Hours Ago")
    plt.ylabel("Decibels")

    plt.pause(30)