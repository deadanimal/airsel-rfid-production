from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from operations.models import MeasurementType

# tanya aimi sama ada measurement type boleh update di WAMS


def insert_into_measurement_type(dict):

    # print("insert_into_measurement_type", dict)
    # find in the database first
    # if do not exist, insert data into database

    # for MeasurementType
    measurement_type = dict['MEASUREMENT_TYPE'] if 'MEASUREMENT_TYPE' in dict else ""
    description = dict['DESCRIPTION'] if 'DESCRIPTION' in dict else ""
    measurement_identifier_code = dict['MEASUREMENT_IDENTIFIER_CODE'] if 'MEASUREMENT_IDENTIFIER_CODE' in dict else ""

    dictionary_measurement_type = {
        "measurement_type": measurement_type,
        "description": description,
        "measurement_identifier": measurement_identifier_code
    }

    measurement_type = MeasurementType(**dictionary_measurement_type)
    measurement_type.save()


def get_measurementtype():

    MeasurementType.objects.all().delete()

    r = requests.post("http://139.59.125.201/getMeasurementType.php")

    json_dictionary = json.loads(r.content)
    for key in json_dictionary:
        if (key == "results"):
            print(key, ":", json_dictionary[key])
            if (type(json_dictionary[key]) == dict):
                # return single json
                print("dict")
                insert_into_measurement_type(json_dictionary[key])
            elif (type(json_dictionary[key]) == list):
                # return array of json
                print("list")
                results_json = json_dictionary[key]
                for x in results_json:
                    insert_into_measurement_type(x)

    return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-MEAUSREMENTTYPE?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # response = client.service.ExtractMeasurementType()
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractMeasurementType']['ouaf:results']
