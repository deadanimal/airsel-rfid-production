from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from datetime import datetime
import pytz

from assets.models import (
    Asset,
    AssetAttribute,
    AssetMeasurementType,
    AssetMeasurementTypeInbound,
    AssetAttributeInbound
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
    print("here 2")
    print("here 3",dict['ASSET_ID'])
    # find in the database first
    # if do not exist, insert data into database
    asset = Asset.objects.filter(
        asset_id=dict['ASSET_ID']).exists()

    print("here 4")
    # for Asset
    asset_id = dict['ASSET_ID'] if 'ASSET_ID' in dict else ""
    asset_type = dict['ASSET_TYPE_CD'] if 'ASSET_TYPE_CD' in dict else ""
    description = dict['DESCRLONG'] if 'DESCRLONG' in dict else ""
    bo = dict['BUS_OBJ_CD'] if 'BUS_OBJ_CD' in dict else ""
    bo_status = dict['BO_STATUS_CD'] if 'BO_STATUS_CD' in dict else ""
    owning_access_group = dict['OWNING_ACCESS_GRP_CD'] if 'OWNING_ACCESS_GRP_CD' in dict else ""
    # effective_datetime = format_datetime(dict['EFF_DTTM']) if 'EFF_DTTM' in dict else ""

    # convert effctive_datetime into UTC
    
    timezone = pytz.timezone('Asia/Kuala_Lumpur')
    datetime_data = datetime.strptime(dict['EFF_DTTM'], "%Y-%m-%d-%H.%M.%S")
    print("datetime_data",datetime_data)

    datetime_timezone = timezone.localize(datetime_data)
    effective_datetime = datetime_timezone.astimezone(pytz.utc)

    print("effective_datetime",effective_datetime)
    # end convert affective datetime

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

    print("here 6")
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
        "registered_datetime": registered_datetime,
        "transaction_type":"UPDATE"
    }

    if not asset:
        print("here 7")
        # insert data into database
        # print("insert")
        asset = Asset(**dictionary)
        asset.save()
        inserted_asset_id = asset.id

    else:
        print("here 8")
        # update data into database
        # print("update")
        Asset.objects.filter(asset_id=asset_id).update(**dictionary)
        inserted_asset_id = Asset.objects.filter(asset_id=asset_id).first()

    characteristic_type_list = ["CM-MFG","CM-WASTC","CM-VRTVD","CM-VOWNS","CM-VROWN","CM-VINPT"]
    # to save measurement_types if exist
    print(measurement_types)
    if measurement_types != "":

        ### check for measurement type exist
        check_asset_measurement_type_inbound = {
            "measurement_type": measurement_types,
            "asset_id":inserted_asset_id
        }
        check_in_asset_measurement_type_inbound = AssetMeasurementTypeInbound.objects.filter(**check_asset_measurement_type_inbound).exists()

        ### insert data to asset measurement inbound
        asset_measurement_type_inbound = AssetMeasurementTypeInbound.objects.create(
                measurement_type=measurement_types,asset_id=Asset.objects.filter(asset_id=asset_id).first())
        # characteristic_type_list = ["CM-MFG","CM-WASTC","CM-VRTVD","CM-VOWNS","CM-VROWN","CM-VINPT"]
        print("here 9")

        # die()

        if not check_in_asset_measurement_type_inbound:

            print("here 10")
            
            asset = Asset.objects.get(asset_id=asset_id)
            asset_measurement_type = AssetMeasurementType.objects.create(measurement_type=measurement_types,action_type='UNCHANGED')
            asset.measurement_types.add(asset_measurement_type)

    # to save characteristic_type && characteristic_value if exist
    if characteristic_type != "" and characteristic_value != "":

        print("here 11")

        ## check for asset attribute
        check_asset_attribute_inbound = {
            "characteristic_type": characteristic_type,
            "asset_id":inserted_asset_id
        }            
        check_in_asset_attribute_inbound = AssetAttributeInbound.objects.filter(**check_asset_attribute_inbound).exists()

        ### insert data into asset attribute inbound
        asset_attribute_inbound = AssetAttributeInbound.objects.create(characteristic_type=characteristic_type, characteristic_value=characteristic_value, asset_id=Asset.objects.filter(asset_id=asset_id).first())

        # asset_attribute_inbound_exist = AssetAttributeInbound.objects.filter(asset_id=inserted_asset_id).exists()
        # print(asset_attribute_inbound_exist)
        
        if not check_in_asset_attribute_inbound:
            print("characteristic_type = ",characteristic_type)
            if characteristic_type in characteristic_type_list:
                asset = Asset.objects.get(asset_id=asset_id)
                asset_attribute = AssetAttribute.objects.create(
                    characteristic_type=characteristic_type, characteristic_value=characteristic_value,action_type='UNCHANGED')
                asset.asset_attributes.add(asset_attribute)
                print('found',asset_attribute)
            else:
                asset = Asset.objects.get(asset_id=asset_id)
                asset_attribute = AssetAttribute.objects.create(
                    characteristic_type=characteristic_type, adhoc_value=characteristic_value,action_type='UNCHANGED')
                asset.asset_attributes.add(asset_attribute)
                print("not found",asset_attribute)

    #     asset = Asset.objects.get(asset_id=asset_id)
    #     asset_measurement_type = AssetMeasurementType.objects.create(
    #         measurement_type=measurement_types)
    #     asset.measurement_types.add(asset_measurement_type)

    # # to save characteristic_type && characteristic_value if exist
    # if characteristic_type != "" and characteristic_value != "":
    #     asset = Asset.objects.get(asset_id=asset_id)
    #     asset_attribute = AssetAttribute.objects.create(
    #         characteristic_type=characteristic_type, characteristic_value=characteristic_value)
    #     asset.asset_attributes.add(asset_attribute)

def get_asset(badge_number):

    payload = {
        "badge_number": badge_number
    }

    r = requests.post("http://139.59.125.201/getAsset.php", data = payload)

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

    print("here 1")
    # insert_into_asset(json_dictionary['results'])
    return json.loads(r.content)

    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-ASSETFB?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # request_data = {
    #     'BADGE_NUMBER': 'AIRV-000TEST1'
    # }

    # response = client.service.ExtractAssetBadge(**request_data)
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractAssetBadge']['ouaf:results']
