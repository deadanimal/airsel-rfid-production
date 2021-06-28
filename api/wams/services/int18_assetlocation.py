from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from assets.models import AssetLocationSync


def insert_into_asset_location_sync(dict):

    # print("insert_into_asset_location_sync", dict)
    # find in the database first
    # if do not exist, insert data into database

    # for AssetLocationSync
    node_id = dict['NODE_ID'] if 'NODE_ID' in dict else ""
    description = dict['DESCRIPTION'] if 'DESCRIPTION' in dict else ""

    dictionary_asset_location_sync = {
        "node_id": node_id,
        "description": description
    }

    asset_location_sync = AssetLocationSync.objects.filter(node_id=node_id).exists()

    if not asset_location_sync:
        # asset location sync does not exist in the database
        asset_location_sync = AssetLocationSync(**dictionary_asset_location_sync)
        asset_location_sync.save()

    else:
        asset_location_sync = AssetLocationSync.objects.get(node_id=node_id)
        asset_location_sync.description = description
        asset_location_sync.save()


def get_assetlocation(from_date, to_date):

    payload = {
        "from_date": from_date,
        "to_date": to_date
    }

    r = requests.post(
        "http://139.59.125.201/getAssetLocation.php", data=payload)

    json_dictionary = json.loads(r.content)
    for key in json_dictionary:
        if (key == "results"):
            print(key, ":", json_dictionary[key])
            if (type(json_dictionary[key]) == dict):
                # return single json
                print("dict")
                insert_into_asset_location_sync(json_dictionary[key])
            elif (type(json_dictionary[key]) == list):
                # return array of json
                print("list")
                results_json = json_dictionary[key]
                for x in results_json:
                    insert_into_asset_location_sync(x)

    return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM_ASSETLOCATION?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # response = client.service.CM_ASSETLOCATION()
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:CM_ASSETLOCATION']['ouaf:results']
