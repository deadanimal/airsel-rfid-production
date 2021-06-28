from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from operations.models import Planner


def insert_into_planner(dict):

    # print("insert_into_planner", dict)
    # find in the database first
    # if do not exist, insert data into database

    # for Planner
    planner = dict['PLANNER'] if 'PLANNER' in dict else ""
    description = dict['Description'] if 'Description' in dict else ""
    status = dict['Status'] if 'Status' in dict else ""
    user_id = dict['USER_ID'] if 'USER_ID' in dict else ""

    dictionary_planner = {
        "planner": planner,
        "description": description,
        "status": status,
        "user_id": user_id
    }

    planner_exist = Planner.objects.filter(planner=planner).exists()

    if not planner_exist:
        # planner does not exist in the database
        planner = Planner(**dictionary_planner)
        planner.save()

    else:
        planner = Planner.objects.get(planner=planner)
        planner.description = description
        planner.status = status
        planner.user_id = user_id
        planner.save()


def get_planner(from_date, to_date):

    
    payload = {
        "from_date": from_date,
        "to_date": to_date
    }

    # print("eeeeeeee")
    r = requests.post("http://139.59.125.201/getPlanner.php", data=payload)
    # print("qqqqqqqq")
    print(r)

    json_dictionary = json.loads(r.content)
    print(json_dictionary)

    if json_dictionary : 

        Planner.objects.all().delete()
        
        for key in json_dictionary:
            if (key == "results"):
                print(key, ":", json_dictionary[key])
                if (type(json_dictionary[key]) == dict):
                    # return single json
                    print("dict")
                    insert_into_planner(json_dictionary[key])
                elif (type(json_dictionary[key]) == list):
                    # return array of json
                    print("list")
                    results_json = json_dictionary[key]
                    for x in results_json:
                        insert_into_planner(x)

        return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-PLANNER?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # request_data = {
    #     'FROM_DATE': '2020-10-11T00:00:00.000+08:00',
    #     'TO_DATE': '2020-10-13T00:00:00.000+08:00'
    # }

    # response = client.service.ExtractPlanner(**request_data)
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractPlanner']['ouaf:results']
