from utility.basic import display_welcome_message
from geodConvert.geodetic_to_utm import GeodeticToUTM
from geodConvert.utm_to_geodetic import UTMToGeodetic


def conversion_tool():
    display_welcome_message()
    parameters = {
        "conversion_type": int(input("Conversion Type: \n[1] = UTM -> WGS84 \n[2] = WGS84 -> UTM\n").strip()),
    }
    converted = None
    if parameters["conversion_type"] == 1:
        coordinates = {
            "northing": float(input("Northing: \n").strip()),
            "easting": float(input("Easting: \n").strip()),
            "zone": input("Zone: \n").strip()
        }
        converter = UTMToGeodetic(
            northing=coordinates['northing'],
            easting=coordinates['easting'],
            zone=coordinates['zone']
        )
        converted = converter.convert()
        print(converted)
        return converted
    elif parameters["conversion_type"] == 2:
        coordinates = {
            "latitude": float(input("Latitude: \n").strip()),
            "longitude": float(input("Longitude: \n").strip())
        }
        converter = GeodeticToUTM(
            latitude=coordinates['latitude'],
            longitude=coordinates['longitude']
        )
        converted = converter.convert()
        print(converted)
    else:
        print("Invalid Conversion Type")
    return converted


if __name__ == '__main__':
    repeat = True
    while repeat:
        conversion_tool()
        repeat = input("Do you want to convert another set of coordinates? [y/n]").strip().lower() == 'y'
