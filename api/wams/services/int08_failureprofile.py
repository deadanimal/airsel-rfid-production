from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from employee.models import FailureProfile

# tanya aimi sama ada failure profile boleh update di WAMS
def insert_into_failure_profile(dict):

    # print("insert_into_failure_profile", dict)
    # find in the database first
    # if do not exist, insert data into database

    # for FailureProfile
    failure_profile = dict['FAILURE_PROFILE'] if 'FAILURE_PROFILE' in dict else ""
    description = dict['DESCRIPTION'] if 'DESCRIPTION' in dict else ""
    failure_repair = dict['FAILURE_REPAIR'] if 'FAILURE_REPAIR' in dict else ""
    failure_mode = dict['FAILURE_MODE'] if 'FAILURE_MODE' in dict else ""
    failure_comp = dict['FAILURE_COMP'] if 'FAILURE_COMP' in dict else ""
    failure_type = dict['FAILURE_TYPE'] if 'FAILURE_TYPE' in dict else ""

    dictionary_failure_profile = {
        "failure_profile": failure_profile,
        "description": description,
        "failure_repair": failure_repair,
        "failure_mode": failure_mode,
        "failure_comp": failure_comp,
        "failure_type": failure_type
    }

    failure_profile = FailureProfile(**dictionary_failure_profile)
    failure_profile.save()


def get_failureprofile():


    r = requests.post("http://139.59.125.201/getFailureProfile.php")
    
    json_dictionary = json.loads(r.content)

    
    if json_dictionary:
        FailureProfile.objects.all().delete()
        for key in json_dictionary:
            if (key == "results"):
                print(key, ":", json_dictionary[key])
                if (type(json_dictionary[key]) == dict):
                    # return single json
                    print("dict")
                    insert_into_failure_profile(json_dictionary[key])
                elif (type(json_dictionary[key]) == list):
                    # return array of json
                    print("list")
                    results_json = json_dictionary[key]
                    for x in results_json:
                        insert_into_failure_profile(x)

        return json.loads(r.content)
    else:
        print('error ',r.status_code)


    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-FAILUREPROFILE?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # response = client.service.ExtractFailureProf()
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractFailureProf']['ouaf:results']
