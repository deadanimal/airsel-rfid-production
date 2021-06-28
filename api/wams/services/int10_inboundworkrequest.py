from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict


def get_inboundworkrequest(type, data):

    if type == 'create':

        payload = {
            'description': data['description'],
            'long_description': data['long_description'],
            'required_by_date': data['required_by_date'],
            'approval_profile': data['approval_profile'],
            'bo': data['bo'],
            'creation_datetime': data['creation_datetime'],
            'creation_user': data['creation_user'],
            'downtime_start': data['downtime_start'],
            'planner': data['planner'],
            'work_class': data['work_class'],
            'work_category': data['work_category'],
            'work_priority': data['work_priority'],
            'requestor': data['requestor'],
            'owning_access_group': data['owning_access_group'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'primary_phone': data['primary_phone'],
            'mobile_phone': data['mobile_phone'],
            'home_phone': data['home_phone'],
            'node_id': data['node_id'],
            'asset_id': data['asset_id']
        }

        r = requests.post("http://139.59.125.201/getInboundWorkRequestCreate.php", data = payload)
        # r = requests.post("http://139.59.125.201/getInboundWorkRequestCreate.php", data = payload)
    elif type == 'update':

        payload = {
            'work_request_id': data['work_request_id'],
            'approval_profile': data['approval_profile'],
            'work_request_status': data['work_request_status']
        }

        r = requests.post("http://139.59.125.201/getInboundWorkRequestUpdate.php", data = payload)

    if (int(r.status_code) >= 500):
        return {'status': 'ERROR', 'status_code': r.status_code, 'error_details': 'An internal server error have been occurred.'}
    elif (int(r.status_code) >= 400 and int(r.status_code) < 500):
        return {'status': 'ERROR', 'status_code': r.status_code, 'error_details': 'A client error have been occurred.'}
    else:
        return json.loads(r.content)

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
