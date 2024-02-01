from utility.basic import display_welcome_message
from geodConvert.geodetic_to_utm import GeodeticToUTM


def start_conversion(lat, lon):
    converter = GeodeticToUTM(latitude=lat, longitude=lon)
    converted = converter.convert()
    return converted


def conversion_tool():
    display_welcome_message()
    converted = start_conversion(-1.103000, 37.014802)
    print(converted)
    #   TODO: determine the type of conversion
    #   TODO: collect the data required for conversion
    #   TODO: Initiate the conversion and output data in the specific dataclass


if __name__ == '__main__':
    conversion_tool()
