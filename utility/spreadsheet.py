import pandas as pd
from geodConvert.utm_to_geodetic import UTMToGeodetic
from geodConvert.geodetic_to_utm import GeodeticToUTM


def process_spreadsheet(file_path, conversion_type):
    print(f"Processing spreadsheet at {file_path}")
    # assert file_path is csv
    assert file_path.endswith('.csv'), "File must be a csv file"
    # read spreadsheet csv
    df = pd.read_csv(file_path)

    if conversion_type == 1:
        # get the Northing, Easting, Zone columns from the spreadsheet
        northing = df['Northing']
        easting = df['Easting']
        zone = df['Zone']

        latitudes = []
        longitudes = []

        for i in range(len(northing)):
            # convert each row to latitude and longitude
            # using the UTMToGeodetic class
            # append the latitude and longitude to the latitudes and longitudes lists
            converter = UTMToGeodetic(northing=northing[i], easting=easting[i], zone=zone[i])
            converted = converter.convert()
            latitudes.append(converted['latitude'])
            longitudes.append(converted['longitude'])

        df["lat"] = latitudes
        df["lon"] = longitudes
        return df
    elif conversion_type == 2:
        # get the Latitude, Longitude columns from the spreadsheet
        latitudes = df['Latitude']
        longitudes = df['Longitude']

        northing = []
        easting = []
        zones = []

        for i in range(len(latitudes)):
            # convert each row to easting and northing
            # using the GeodeticToUTM class
            # append the easting and northing to the easting and northing lists
            converter = GeodeticToUTM(latitude=latitudes[i], longitude=longitudes[i])
            converted = converter.convert()
            easting.append(converted['easting'])
            northing.append(converted['northing'])
            zones.append(converter.zone)
        df["easting"] = easting
        df["northing"] = northing
    else:
        print("Invalid Conversion Type")
        return df
