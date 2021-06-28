from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from assets.models import (
    Asset,
    AssetAttribute,
    AssetMeasurementType
)


# kena bincang dengan aimi untuk manytomanyfield
def format_datetime(datetime):

    # from : 2021-01-29-02.23.31
    # to : 2021-02-21 15:00:00
    date = datetime[:10]
    time = datetime[11:].replace('.', ':')

    return date + ' ' + time + "+00:00"


def insert_into_asset(dict):

    # print("insert_into_asset", dict)
    # find in the database first
    # if do not exist, insert data into database
    asset = Asset.objects.filter(
        asset_id=dict['ASSET_ID']).exists()

    # for Asset
    asset_id = dict['ASSET_ID'] if 'ASSET_ID' in dict else ""
    asset_type = dict['ASSET_TYPE_CD'] if 'ASSET_TYPE_CD' in dict else ""
    description = dict['DESCRLONG'] if 'DESCRLONG' in dict else ""
    bo = dict['BUS_OBJ_CD'] if 'BUS_OBJ_CD' in dict else ""
    bo_status = dict['BO_STATUS_CD'] if 'BO_STATUS_CD' in dict else ""
    owning_access_group = dict['OWNING_ACCESS_GRP_CD'] if 'OWNING_ACCESS_GRP_CD' in dict else ""
    effective_datetime = format_datetime(
        dict['EFF_DTTM']) if 'EFF_DTTM' in dict else ""
    node_id = dict['NODE_ID'] if 'NODE_ID' in dict else ""
    badge_no = dict['BADGE_NUMBER'] if 'BADGE_NUMBER' in dict else ""
    serial_no = dict['SERIAL_NUMBER'] if 'SERIAL_NUMBER' in dict else ""
    condition_rating = dict['CONDITION_RATING'] if 'CONDITION_RATING' in dict else ""
    condifence_rating = dict['CONFIDENCE_RATING'] if 'CONFIDENCE_RATING' in dict else ""
    maintenance_specification = dict['MAINT_SPEC_CD'] if 'MAINT_SPEC_CD' in dict else ""
    attached_to_asset_id = dict['LOCATION_ATTACHED_TO_ASSET'] if 'LOCATION_ATTACHED_TO_ASSET' in dict else ""
    registered_datetime = format_datetime(
        dict['CRE_DTTM']) if 'CRE_DTTM' in dict else ""
    pallet_no = dict['PALLET_NUMBER'] if 'PALLET_NUMBER' in dict else ""
    handed_over_asset = dict['WAC_HOA_SCRCH_VALUE'] if 'WAC_HOA_SCRCH_VALUE' in dict else ""
    scada_id = dict['SCADA_ID'] if 'SCADA_ID' in dict else ""

    # for AssetMeasurementType
    measurement_types = dict['MEASUREMENT_TYPE_CD'] if 'MEASUREMENT_TYPE_CD' in dict else ""

    # for AssetAttribute
    characteristic_type = dict['WAA_CHAR_TYPE_CD'] if 'WAA_CHAR_TYPE_CD' in dict else ""
    characteristic_value = dict['ASSET_ATTR_SCRH'] if 'ASSET_ATTR_SCRH' in dict else ""

    dictionary = {
        "asset_id": asset_id,
        "asset_type": asset_type,
        "description": description,
        "bo": bo,
        "bo_status": bo_status,
        "owning_access_group": owning_access_group,
        "effective_datetime": effective_datetime,
        "node_id": node_id,
        "badge_no": badge_no,
        "serial_no": serial_no,
        "pallet_no": pallet_no,
        "handed_over_asset": handed_over_asset,
        "scada_id": scada_id,
        "condition_rating": condition_rating,
        "condifence_rating": condifence_rating,
        "maintenance_specification": maintenance_specification,
        "attached_to_asset_id": attached_to_asset_id,
        "registered_datetime": registered_datetime
    }

    if not asset:
        # insert data into database
        # print("insert")
        asset = Asset(**dictionary)
        asset.save()

    else:
        # update data into database
        # print("update")
        Asset.objects.filter(asset_id=asset_id).update(**dictionary)

    # to save measurement_types if exist
    if measurement_types != "":
        asset = Asset.objects.get(asset_id=asset_id)
        asset_measurement_type = AssetMeasurementType.objects.create(
            measurement_type=measurement_types)
        asset.measurement_types.add(asset_measurement_type)

    # to save characteristic_type && characteristic_value if exist
    if characteristic_type != "" and characteristic_value != "":
        asset = Asset.objects.get(asset_id=asset_id)
        asset_attribute = AssetAttribute.objects.create(
            characteristic_type=characteristic_type, characteristic_value=characteristic_value)
        asset.asset_attributes.add(asset_attribute)


def get_assetsyncoutbound(from_date, to_date):

    payload = {
        "from_date": from_date,
        "to_date": to_date
    }

    r = requests.post(
        "http://139.59.125.201/getAssetSyncOutbound.php", data=payload)

    json_dictionary = json.loads(r.content)
    for key in json_dictionary:
        if (key == "results"):
            print(key, ":", json_dictionary[key])
            if (type(json_dictionary[key]) == dict):
                # return single json
                print("dict")
                insert_into_asset(json_dictionary[key])
            elif (type(json_dictionary[key]) == list):
                # return array of json
                print("list")
                results_json = json_dictionary[key]
                for x in results_json:
                    insert_into_asset(x)

    return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-ASSETSYNCOB?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # request_data = {
    #     'FROM_DATE': '2019-02-01T14:00:00.000+08:00',
    #     'TO_DATE': '2020-10-20T14:00:00.000+08:00'
    # }

    # response = client.service.ExtractAssetSync(**request_data)
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractAssetSync']['ouaf:results']
