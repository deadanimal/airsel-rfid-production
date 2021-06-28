from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from employee.models import Employee


def insert_into_employee(dict):

    print("insert_into_employee", dict)
    # find in the database first
    # if do not exist, insert data into database
    employee = Employee.objects.filter(
        employee_id=dict['EMPLOYEE_ID']).exists()

    if not employee:
        print("new")
        # insert data into database
        w1_first_name = dict['W1_FIRST_NAME'] if 'W1_FIRST_NAME' in dict else ""
        employee = Employee(employee_id=dict['EMPLOYEE_ID'], first_name=w1_first_name, last_name=dict['W1_LAST_NAME'], phone_no=dict['W1_PHONE_VALUE'], user_type=dict['EMPLOYEE_TYPE_CD'],
                            bo_status_cd=dict['BO_STATUS_CD'], country=dict['COUNTRY'], business_unit_cd=dict['BUSINESS_UNIT_CD'], hr_employee_number=dict['HR_EMPLOYEE_NUMBER'])

        employee.save()
    
    else: 
        # update data in database
        print("update")
        w1_first_name = dict['W1_FIRST_NAME'] if 'W1_FIRST_NAME' in dict else ""

        dictionary = {
            "employee_id":dict['EMPLOYEE_ID'],
            "first_name": w1_first_name,
            "last_name": dict['W1_LAST_NAME'],
            "phone_no": dict['W1_PHONE_VALUE'],
            "user_type": dict['EMPLOYEE_TYPE_CD'],
            "bo_status_cd": dict['BO_STATUS_CD'],
            "country": dict['COUNTRY'],
            "business_unit_cd": dict['BUSINESS_UNIT_CD'],
            "hr_employee_number": dict['HR_EMPLOYEE_NUMBER']
        }
        Employee.objects.filter(employee_id=dict['EMPLOYEE_ID']).update(**dictionary)


def get_employee(from_date, to_date):

    # Employee.objects.all().delete()

    payload = {
        "from_date": from_date,
        "to_date": to_date
    }

    r = requests.post("http://139.59.125.201/getEmployee.php", data=payload)


    json_dictionary = json.loads(r.content)
    for key in json_dictionary:
        if (key == "results"):
            # print(key, ":", json_dictionary[key])
            if (type(json_dictionary[key]) == dict):
                # return single json
                print("dict")
                insert_into_employee(json_dictionary[key])
            elif (type(json_dictionary[key]) == list):
                # return array of json
                print("list")
                results_json = json_dictionary[key]
                for x in results_json:
                    insert_into_employee(x)

    return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-EMPLOYEE?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # request_data = {
    #     'FROM_DATE': '2020-01-01T14:00:00.000+00:00',
    #     'TO_DATE': '2020-10-05T15:00:00.000+00:00'
    # }

    # response = client.service.ExtractEmployee(**request_data)
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractEmployee']['ouaf:results']
