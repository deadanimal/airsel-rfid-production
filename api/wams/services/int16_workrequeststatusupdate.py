from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from operations.models import WorkRequestStatus,WorkRequest

def insert_into(dict):

    # print("insert_into", dict)
    # find in the database first
    # if do not exist, insert data into database

    # for AssetLocationSync
    work_re_id = dict['WORK_REQ_ID'] if 'WORK_REQ_ID' in dict else ""
    status = dict['STATUS'] if 'STATUS' in dict else ""

    dictionary = {
        "work_request_id": work_re_id,
        "status": status
    }

    work_request_statuses = WorkRequestStatus.objects.filter(work_request_id=work_re_id).exists()

    if not work_request_statuses:
        # asset location sync does not exist in the database
        work_request_statuses = WorkRequestStatus(**dictionary)
        work_request_statuses.save()

    else:
        work_request_statuses = WorkRequestStatus.objects.get(work_request_id=work_re_id)
        work_request_statuses.status = status
        work_request_statuses.save()

    work_requests = WorkRequest.objects.filter(work_request_id=work_re_id).exists()

    if work_requests:
        # asset location sync does not exist in the database
        workRequest = WorkRequest.objects.get(work_request_id=work_re_id)
        workRequest.work_request_status = status
        workRequest.save()


def get_workrequeststatusupdate(from_date, to_date):

    payload = {
        "from_date": from_date,
        "to_date": to_date,
    }

    r = requests.post("http://139.59.125.201/getWorkRequestStatusUpdate.php", data = payload)    

    if (int(r.status_code) >= 500):
        return {'status': 'ERROR', 'status_code': r.status_code, 'error_details': 'An internal server error have been occurred.'}
    elif (int(r.status_code) >= 400 and int(r.status_code) < 500):
        return {'status': 'ERROR', 'status_code': r.status_code, 'error_details': 'A client error have been occurred.'}
    else:
        return json.loads(r.content)

    json_dictionary = json.loads(r.content)
    if json_dictionary: 
        for key in json_dictionary:
            if (key == "results"):

                print(key, ":", json_dictionary[key])
                if (type(json_dictionary[key]) == dict):
                    # return single json
                    print("dict")
                    insert_into(json_dictionary[key])
                elif (type(json_dictionary[key]) == list):
                    # return array of json
                    print("list")
                    results_json = json_dictionary[key]
                    for x in results_json:
                        insert_into(x)

        # return json.loads(r.content)
        return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-CM-WORKREQUEST?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # response = client.service.ExtractWorkRequest()
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractWorkRequest']['ouaf:results']
