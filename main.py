import os

import requests
import json
import time

def read_localization_file(file_path):
    with open(file_path, 'r', encoding="utf8") as f:
        content = f.readlines()

    localization_values = {}

    for line in content:
        if '"' in line:
            key, value = line.split('"', 1)
            localization_values[key] = value.strip('"\n')

    return localization_values


def check_wikipedia(output, loc_values):
    engine_id = "XXX"
    api_key = "YYY"

    for key, value in loc_values.items():
        print("Checking " + key)
        if len(value) >= 60:
            # Split the value into 25 character long chunks
            chunks = [value[i:i + 60] for i in range(0, len(value),60)]

            for chunk in chunks:
                if len(chunk) < 60:
                    continue
                time.sleep(0.5)
                response = requests.get(
                    f"https://www.googleapis.com/customsearch/v1",
                    params={
                        "key": api_key,
                        "cx": engine_id,
                        "q": '"' + chunk + '"',
                        # "q": '"' + "The word rade comes from the old English term" + '"'
                    },
                )
                data = response.json()
                if "searchInformation" not in data:
                    print(response.status_code)

                # Check if there are any search results
                if data["searchInformation"]["totalResults"] != "0":
                    print(f'Text for {key} might be copied from Wikipedia. \n {chunk}')
                    output.write(f'Text for {key} might be copied from Wikipedia. \n {chunk}')
                    break  # no need to check further chunks if a match is found
                output.write(f'{key} seems fine...\n')



directory = 'i:\SteamLibrary\steamapps\common\Europa Universalis IV\localisation\\'
o = open(f'{directory}\\scan_output.txt', 'a+')

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        if "l_english" in f:
            print(f"Checking {f}...")
            localization_values = read_localization_file(f)
            check_wikipedia(o, localization_values)