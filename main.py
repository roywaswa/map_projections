from utility.basic import display_welcome_message
from geodConvert.geodetic_to_utm import GeodeticToUTM


def conversion_tool():
    display_welcome_message()
    converter = GeodeticToUTM(-1.103000,37.014802)
    converted = converter.convert()
    print(converted)
    #   TODO: determine the type of conversion
    #   TODO: collect the data required for conversion
    #   TODO: Initiate the conversion and output data in the specific dataclass


if __name__ == '__main__':
    conversion_tool()
