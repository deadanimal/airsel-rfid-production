from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from operations.models import MaintenanceManager


def insert_into_maintenance_manager(dict):

    # print("insert_into_maintenance_manager", dict)
    # find in the database first
    # if do not exist, insert data into database

    # for MaintenanceManager
    maintenance_manager = dict['MAINTENANCE_MANAGER'] if 'MAINTENANCE_MANAGER' in dict else ""
    description = dict['DESCRIPTION'] if 'DESCRIPTION' in dict else ""
    status = dict['STATUS'] if 'STATUS' in dict else ""
    user_id = dict['USER_ID'] if 'USER_ID' in dict else ""

    dictionary_maintenance_manager = {
        "maintenance_manager": maintenance_manager,
        "description": description,
        "status": status,
        "user_id": user_id
    }

    maintenance_manager_exist = MaintenanceManager.objects.filter(
        **dictionary_maintenance_manager).exists()

    if not maintenance_manager_exist:
        # maintenance manager does not exist in the database
        maintenance_manager = MaintenanceManager(**dictionary_maintenance_manager)
        maintenance_manager.save()

    else:
        maintenance_manager = MaintenanceManager.objects.get(maintenance_manager=maintenance_manager)
        maintenance_manager.description = description
        maintenance_manager.status = status
        maintenance_manager.user_id = user_id
        maintenance_manager.save()


def get_maintenancemanager(from_date, to_date):

    payload = {
        "from_date": from_date,
        "to_date": to_date
    }

    r = requests.post(
        "http://139.59.125.201/getMaintenanceManager.php", data=payload)

    json_dictionary = json.loads(r.content)
    for key in json_dictionary:
        if (key == "results"):
            print(key, ":", json_dictionary[key])
            if (type(json_dictionary[key]) == dict):
                # return single json
                print("dict")
                insert_into_maintenance_manager(json_dictionary[key])
            elif (type(json_dictionary[key]) == list):
                # return array of json
                print("list")
                results_json = json_dictionary[key]
                for x in results_json:
                    insert_into_maintenance_manager(x)

    return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-MAINTENANCEMANAGER?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # request_data = {
    #     'FROM_DATE': '2019-01-01T14:00:00.000+08:00',
    #     'TO_DATE': '2020-10-19T14:00:00.000+08:00'
    # }

    # response = client.service.ExtractMaintenanceManager(**request_data)
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractMaintenanceManager']['ouaf:results']
