from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from operations.models import (
    ServiceHistory,
    ServiceHistoryQuestion,
    ServiceHistoryQuestionValidValue
)


def insert_into_service_history(dict):

    # print("insert_into_service_history", dict)
    # find in the database first
    # if do not exist, insert data into database

    # for ServiceHistory
    service_hist_type = dict['SERVICE_HIST_TYPE'] if 'SERVICE_HIST_TYPE' in dict else ""
    service_hist_desc = dict['SERVICE_HIST_DESC'] if 'SERVICE_HIST_DESC' in dict else ""
    service_hist_bo = dict['SERVICE_HIST_BO'] if 'SERVICE_HIST_BO' in dict else ""
    category = dict['CATEGORY'] if 'CATEGORY' in dict else ""
    service_hist_subclass = dict['SERVICE_HIST_SUBCLASS'] if 'SERVICE_HIST_SUBCLASS' in dict else ""

    # for ServiceHistoryQuestion
    question_seq = dict['QUESTION_SEQ'] if 'QUESTION_SEQ' in dict else ""
    question_cd = dict['QUESTION_CD'] if 'QUESTION_CD' in dict else ""
    question_desc = dict['QUESTION_DESC'] if 'QUESTION_DESC' in dict else ""

    # for ServiceHistoryQuestionValidValue
    answer_seq = dict['ANSWER_SEQ'] if 'ANSWER_SEQ' in dict else ""
    answer_cd = dict['ANSWER_CD'] if 'ANSWER_CD' in dict else ""
    answer_desc = dict['ANSWER_DESC'] if 'ANSWER_DESC' in dict else ""
    point_value = dict['POINT_VALUE'] if 'POINT_VALUE' in dict else ""
    style = dict['STYLE'] if 'STYLE' in dict else ""

    dictionary_service_history = {
        "service_hist_type": service_hist_type,
        "service_hist_desc": service_hist_desc,
        "service_hist_bo": service_hist_bo,
        "category": category,
        "service_hist_subclass": service_hist_subclass
    }

    dictionary_service_history_question = {
        "question_seq": question_seq,
        "question_cd": question_cd,
        "question_desc": question_desc,
    }

    dictionary_service_history_question_valid_value = {
        "answer_seq": answer_seq,
        "answer_cd": answer_cd,
        "answer_desc": answer_desc,
        "point_value": point_value,
        "style": style
    }

    # ServiceHistory operation
    service_history = ServiceHistory.objects.filter(
        **dictionary_service_history).exists()

    if not service_history:
        # service history does not exist in the database
        service_history = ServiceHistory(**dictionary_service_history)
        service_history.save()
        service_history_id = service_history.id

    else:
        service_history = ServiceHistory.objects.filter(
            **dictionary_service_history).values()
        service_history_id = service_history[0]['id']

    # ServiceHistoryQuestion operation
    service_history_question = ServiceHistoryQuestion.objects.filter(
        **dictionary_service_history_question).exists()

    if not service_history_question:
        # service history question does not exist in the database
        service_history = ServiceHistory.objects.get(
            **dictionary_service_history)

        # to save into service history question
        service_history_question = ServiceHistoryQuestion.objects.create(
            **dictionary_service_history_question)
        service_history_question.service_history_id = service_history
        service_history_question.save()
        service_history_question_id = service_history_question.id

    else:
        service_history_question = ServiceHistoryQuestion.objects.filter(
            **dictionary_service_history_question).values()
        service_history_question_id = service_history_question[0]['id']

    # ServiceHistoryQuestionValidValue operation
    service_history_question_valid_value = ServiceHistoryQuestionValidValue.objects.filter(
        **dictionary_service_history_question_valid_value).exists()

    if not service_history_question_valid_value:
        # service history question valid value does not exist in the database
        service_history_question = ServiceHistoryQuestion.objects.get(
            **dictionary_service_history_question)

        # to save into service history question valid value
        service_history_question_valid_value = ServiceHistoryQuestionValidValue.objects.create(
            **dictionary_service_history_question_valid_value)
        service_history_question_valid_value.service_history_question_id = service_history_question
        service_history_question_valid_value.save()


def get_servicehistorytype():

    r = requests.post("http://139.59.125.201/getServiceHistoryType.php")

    json_dictionary = json.loads(r.content)
    for key in json_dictionary:
        if (key == "results"):
            print(key, ":", json_dictionary[key])
            if (type(json_dictionary[key]) == dict):
                # return single json
                print("dict")
                insert_into_service_history(json_dictionary[key])
            elif (type(json_dictionary[key]) == list):
                # return array of json
                print("list")
                results_json = json_dictionary[key]
                for x in results_json:
                    insert_into_service_history(x)

    return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-SVCHISTTYPE?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # response = client.service.ExtractServiceHistType()
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractServiceHistType']['ouaf:results']
