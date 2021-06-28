from requests import Session
from requests.auth import HTTPBasicAuth

import json
import requests
import xmltodict

from employee.models import Employee

from assets.models import (
    Asset,
    AssetType,
    AssetServiceHistory
)

from operations.models import (
    WorkOrderActivityCompletion,
    WorkActivityEmployee,
    WorkOrderActivityCompletionAssetLocationAssetList,
    AssetLocationAssetListServiceHistories,
    WorkOrderActivityCompletionAssetLocationAssetListInbound,
    AssetLocationAssetListServiceHistoriesInbound
)

# kena bincang dengan aimi pasal WorkOrderActivityCompletionAssetLocationAssetList


def insert_into_work_order_activity(dict):
    print("insert_into_work_order_activity", dict)
    # find in the database first
    # if do not exist, insert data into database
    workorderactivitycompletion = WorkOrderActivityCompletion.objects.filter(
        activityid=dict['ACT_ID']).exists()

    print("workorderactivitycompletion>>>",workorderactivitycompletion)

    # for WorkOrderActivityCompletion
    activityid = dict['ACT_ID'] if 'ACT_ID' in dict else ""
    bo_status_cd = dict['BO_STATUS_CD'] if 'BO_STATUS_CD' in dict else ""
    user_id_1 = dict['USER_ID_1'] if 'USER_ID_1' in dict else ""
    act_type_cd = dict['ACT_TYPE_CD'] if 'ACT_TYPE_CD' in dict else ""
    wo_id = dict['WO_ID'] if 'WO_ID' in dict else ""
    act_dpos_flg = dict['ACT_DPOS_FLG'] if 'ACT_DPOS_FLG' in dict else ""
    service_class_cd = dict['SERVICE_CLASS_CD'] if 'SERVICE_CLASS_CD' in dict else ""
    requestor_id = dict['REQUESTOR_ID'] if 'REQUESTOR_ID' in dict else ""
    required_by_dt = dict['REQUIRED_BY_DT'] if 'REQUIRED_BY_DT' in dict else ""
    work_priority_flg = dict['WORK_PRIORITY_FLG'] if 'WORK_PRIORITY_FLG' in dict else ""
    descr100 = dict['DESCR100'] if 'DESCR100' in dict else ""
    descrlong = dict['DESCRLONG'] if 'DESCRLONG' in dict else ""
    w1_descr100_upr = dict['W1_DESCR100_UPR'] if 'W1_DESCR100_UPR' in dict else ""
    held_for_parts_flg = dict['HELD_FOR_PARTS_FLG'] if 'HELD_FOR_PARTS_FLG' in dict else ""
    anniversary_value = dict['ANNIVERSARY_VALUE'] if 'ANNIVERSARY_VALUE' in dict else ""
    emergency_flg = dict['EMERGENCY_FLG'] if 'EMERGENCY_FLG' in dict else ""
    act_num = dict['ACT_NUM'] if 'ACT_NUM' in dict else ""
    planner_cd = dict['PLANNER_CD'] if 'PLANNER_CD' in dict else ""
    total_priority = dict['TOTAL_PRIORITY'] if 'TOTAL_PRIORITY' in dict else ""
    total_priority_src_flg = dict['TOTAL_PRIORITY_SRC_FLG'] if 'TOTAL_PRIORITY_SRC_FLG' in dict else ""
    node_id_1 = dict['NODE_ID_1'] if 'NODE_ID_1' in dict else ""
    asset_id_1 = dict['ASSET_ID_1'] if 'ASSET_ID_1' in dict else ""
    percentage = dict['PERCENTAGE'] if 'PERCENTAGE' in dict else ""
    seqno = dict['SEQNO'] if 'SEQNO' in dict else ""
    participation_flg = dict['PARTICIPATION_FLG'] if 'PARTICIPATION_FLG' in dict else ""
    cost_center_cd = dict['COST_CENTER_CD'] if 'COST_CENTER_CD' in dict else ""
    percentage_2 = dict['PERCENTAGE_2'] if 'PERCENTAGE_2' in dict else ""
    act_resrc_reqmt_id = dict['ACT_RESRC_REQMT_ID'] if 'ACT_RESRC_REQMT_ID' in dict else ""
    descrlong_1 = dict['DESCRLONG_1'] if 'DESCRLONG_1' in dict else ""
    resrc_src_flg = dict['RESRC_SRC_FLG'] if 'RESRC_SRC_FLG' in dict else ""
    resrc_type_id = dict['RESRC_TYPE_ID'] if 'RESRC_TYPE_ID' in dict else ""
    w1_quantity = dict['W1_QUANTITY'] if 'W1_QUANTITY' in dict else ""
    unit_price = dict['UNIT_PRICE'] if 'UNIT_PRICE' in dict else ""
    w1_duration = dict['W1_DURATION'] if 'W1_DURATION' in dict else ""
    crew_shift_id = dict['CREW_SHIFT_ID'] if 'CREW_SHIFT_ID' in dict else ""
    sched_duration = dict['SCHED_DURATION'] if 'SCHED_DURATION' in dict else ""
    break_in_dttm = dict['BREAK_IN_DTTM'] if 'BREAK_IN_DTTM' in dict else ""
    work_category = dict['WORK_CATEGORY'] if 'WORK_CATEGORY' in dict else ""

    # for WorkActivityEmployee
    employee_id = dict['EMPLOYEE_ID'] if 'EMPLOYEE_ID' in dict else ""

    # for WorkOrderActivityCompletionAssetLocationAssetList
    node_id = dict['NODE_ID'] if 'NODE_ID' in dict else ""
    asset_id = dict['ASSET_ID'] if 'ASSET_ID' in dict else ""

    # for AssetLocationAssetListServiceHistories
    service_history_type = dict['SVC_HIST_TYPE_CD'] if 'SVC_HIST_TYPE_CD' in dict else ""
    svc_hist_type_req_fl = dict['SVC_HIST_TYPE_REQ_FLG'] if 'SVC_HIST_TYPE_REQ_FLG' in dict else ""

    # # print(asset_id)
    # get_asset_data = Asset.objects.filter(asset_id=asset_id).values()
    # # print("get_asset_data = ")
    # # print(get_asset_data[0]['asset_type'])
    # asset_asset_type = get_asset_data[0]['asset_type']
    # get_asset_type_data = AssetType.objects.filter(asset_type_code=asset_asset_type).values()
    # asset_type_id = get_asset_type_data[0]['id']
    # # print('asset_type_id = ', asset_type_id)
    # get_asset_type_sh_data = AssetType.asset_service_history.through.objects.filter(assettype_id=asset_type_id).values()

    # print(service_history_type," = ",svc_hist_type_req_fl)
    # # print("get_asset_type_sh_data = ",get_asset_type_sh_data)

    # for data_val in get_asset_type_sh_data:
    #     # print("data_val = ",data_val['assetservicehistory_id'])
    #     service_history_ash = AssetServiceHistory.objects.filter(id=data_val['assetservicehistory_id']).values()
    #     print(service_history_type," == ",service_history_ash[0]['asset_service_history'])

    dictionary_work_order_activity_completion = {
        "activityid": activityid,
        "bo_status_cd": bo_status_cd,
        "user_id_1": user_id_1,
        "act_type_cd": act_type_cd,
        "wo_id": wo_id,
        "act_dpos_flg": act_dpos_flg,
        "service_class_cd": service_class_cd,
        "requestor_id": requestor_id,
        "required_by_dt": required_by_dt,
        "work_priority_flg": work_priority_flg,
        "descr100": descr100,
        "descrlong": descrlong,
        "w1_descr100_upr": w1_descr100_upr,
        "held_for_parts_flg": held_for_parts_flg,
        "anniversary_value": anniversary_value,
        "emergency_flg": emergency_flg,
        "act_num": act_num,
        "planner_cd": planner_cd,
        "total_priority": total_priority,
        "total_priority_src_flg": total_priority_src_flg,
        "node_id_1": node_id_1,
        "asset_id_1": asset_id_1,
        "percentage": percentage,
        "seqno": seqno,
        "participation_flg": participation_flg,
        "cost_center_cd": cost_center_cd,
        "percentage_2": percentage_2,
        "act_resrc_reqmt_id": act_resrc_reqmt_id,
        "descrlong_1": descrlong_1,
        "resrc_src_flg": resrc_src_flg,
        "resrc_type_id": resrc_type_id,
        "w1_quantity": w1_quantity,
        "unit_price": unit_price,
        "w1_duration": w1_duration,
        "crew_shift_id": crew_shift_id,
        "sched_duration": sched_duration,
        "break_in_dttm": break_in_dttm,
        "status": 'New',
        "field_1": work_category
    }

    dictionary_work_activity_employee = {
        "employee_id": employee_id
    }

    dictionary_work_order_activity_completion_asset_location_asset_list = {
        "node_id": node_id,
        "asset_id": asset_id
    }

    dictionary_asset_location_asset_list_service_histories = {
        "service_history_type": service_history_type,
        "svc_hist_type_req_fl": svc_hist_type_req_fl
    }

    # WorkOrderActivityCompletion operation
    print('qqqqqqqqqqqqqqqqqq')
    if not workorderactivitycompletion:
        # insert data into database
        print('wwwwwwwwwwwwww')
        workorderactivitycompletion = WorkOrderActivityCompletion(
            **dictionary_work_order_activity_completion)
        workorderactivitycompletion.save()
        woac_id = workorderactivitycompletion.id
        print('eeeeeeeeeeeeeeeeee',woac_id)

    else:
        print('aaaaaaaaaaaaa')
        workorderactivitycompletion = WorkOrderActivityCompletion.objects.filter(
            **dictionary_work_order_activity_completion).values()
        # workorderactivitycompletion = WorkOrderActivityCompletion.objects.filter(
        #     **dictionary_work_order_activity_completion).values()

        woac_data = WorkOrderActivityCompletion.objects.get(activityid=dict['ACT_ID'])
        woac_id = woac_data.id
        print(woac_id)

        # field_object = WorkOrderActivityCompletion._meta.get_field(id)
        # woac_id = field_object.value_from_object(workorderactivitycompletion)

        # print('sssssssssssssssss',woac_id)

    # WorkActivityEmployee operation
    if employee_id != "":
        employee = Employee.objects.get(employee_id=employee_id)
        workorderactivitycompletion = WorkOrderActivityCompletion.objects.get(
            activityid=activityid)

        check_wae = {
            "employee_id": employee,
            "work_order_activity_completion_id":workorderactivitycompletion
        }

        print(check_wae)
        wae_exist = WorkActivityEmployee.objects.filter(**check_wae).exists()

        if not wae_exist:
            workactivityemployee = WorkActivityEmployee.objects.create(
                employee_id=employee, work_order_activity_completion_id=workorderactivitycompletion)
            workactivityemployee.save()

    ## check data make sure not empty
    if node_id != "" and asset_id != "":
        print("lepas bocaahhhhhhhhhh")

        ## check if exist in inbound activity_id and asset_id
        print('ddddddddddd')
        check_woacalali = {
            "node_id": node_id,
            "asset_id": asset_id,
            "activityid":activityid
        }
        print('ggggggggggggg')
        woacalali_exist = WorkOrderActivityCompletionAssetLocationAssetListInbound.objects.filter(**check_woacalali).exists()
        
        print('hhhhhhhhhhhhh')
        dictionary_work_order_activity_completion_asset_location_asset_list_inbound = {
            "node_id": node_id,
            "asset_id": asset_id,
            "activityid":activityid
        }
        # print("dictionary_work_order_activity_completion_asset_location_asset_list_inbound = ",dictionary_work_order_activity_completion_asset_location_asset_list_inbound)
        # woacalali_exist = WorkOrderActivityCompletionAssetLocationAssetListInbound.objects.filter(activityid=activityid).exists()
        woacalal = WorkOrderActivityCompletionAssetLocationAssetListInbound(
            **dictionary_work_order_activity_completion_asset_location_asset_list_inbound)
        woacalal.save()

        # print("woacalali ==== ",woacalal)

        # WorkOrderActivityCompletionAssetLocationAssetList operation
        if not woacalali_exist:

            print("here 3333")
            ## save data woacalali
            woacalal_save = WorkOrderActivityCompletionAssetLocationAssetList(
                **dictionary_work_order_activity_completion_asset_location_asset_list)
            woacalal_save.save()


            # print("woacalal data ==== ",woacalal)

            # save into woac table


            # if queryset is None :

            # new_woacalal_count = WorkOrderActivityCompletionAssetLocationAssetList.objects.filter(asset_id=asset_id).count()
            # print("new_woacalal_count",new_woacalal_count)

            # if new_woacalal_count == 1 :

                # new_woacalal = WorkOrderActivityCompletionAssetLocationAssetList.objects.get(asset_id=asset_id)
            # print("new_woacalal>>>",new_woacalal)
            woac_table = WorkOrderActivityCompletion.objects.get(activityid=activityid)
            woac_table.asset_location_asset_list.add(woacalal_save.id)
            print("woac_table>>>",woac_table)

            # else : 

            #     print("woac_id ==== ",woac_id)
            #     queryset = WorkOrderActivityCompletion.objects.filter(id=woac_id).values_list('asset_location_asset_list', flat=True)
            #     print("queryset------------------",queryset)
            #     print("queryset------------------",len(queryset))

            #     woacalal_table = WorkOrderActivityCompletionAssetLocationAssetList.objects.filter(node_id=node_id,asset_id=asset_id).values_list('id', flat=True)
            #     print("woacalal_table = ",woacalal_table)
            #     for line in woacalal_table:

            #         if line in queryset : 
            #             print('exist',line)
            #             woacalal_data = WorkOrderActivityCompletionAssetLocationAssetList.objects.get(id=line)
            #             print(woacalal_data)
            #             woacalal_data.service_histories.add(alalsh)

             
    # check for asset location asset list service history
    print("node_id>>>>",node_id)
    print("asset_id>>>>",asset_id)
    if node_id != "" and asset_id != "":
        print("dah lepas cokkkkkkkkkkk")
        ## check if exist in asset location asset list service history inbound for asset_id, activity_id, service_history_type
        check_alalsh = {
            "asset_id": asset_id,
            "activityid":activityid,
            "service_history_type":service_history_type
        }
        alalshi_exist = AssetLocationAssetListServiceHistoriesInbound.objects.filter(**check_alalsh).exists()
        print("alalshi_exist = ",alalshi_exist)
        ## insert in a 
        dictionary_asset_location_asset_list_service_histories_inbound = {
            "service_history_type": service_history_type,
            "svc_hist_type_req_fl": svc_hist_type_req_fl,
            "asset_id": asset_id,
            "activityid":activityid,
        }

        alalshi_insert = AssetLocationAssetListServiceHistoriesInbound(
            **dictionary_asset_location_asset_list_service_histories_inbound)
        alalshi_insert.save()

        # check AssetLocationAssetListServiceHistories operation
        # AssetLocationAssetListServiceHistories operation
        # if service_history_type != "" and svc_hist_type_req_fl != "":

        alalsh_table = AssetLocationAssetListServiceHistories(
            **dictionary_asset_location_asset_list_service_histories)
        alalsh_table.save()
        alalsh = alalsh_table.id


        # woacalali_table = WorkOrderActivityCompletionAssetLocationAssetListInbound.objects.get(node_id=node_id,asset_id=asset_id)
        # print("woacalal_table = ",woacalali_table)
        # for woacalali_value in woacalali_table:
            # woacalali_table.service_histories.add(alalsh)    

        # print(asset_id)
        get_asset_data = Asset.objects.filter(asset_id=asset_id).values()
        # print("get_asset_data = ")
        # print(get_asset_data[0]['asset_type'])
        asset_asset_type = get_asset_data[0]['asset_type']
        get_asset_type_data = AssetType.objects.filter(asset_type_code=asset_asset_type).values()
        asset_type_id = get_asset_type_data[0]['id']
        # print('asset_type_id = ', asset_type_id)
        get_asset_type_sh_data = AssetType.asset_service_history.through.objects.filter(assettype_id=asset_type_id).values()

        print(service_history_type," = ",svc_hist_type_req_fl)
        # print("get_asset_type_sh_data = ",get_asset_type_sh_data)

        fill_the_data = "no"
        for data_val in get_asset_type_sh_data:
            # print("data_val = ",data_val['assetservicehistory_id'])
            service_history_ash = AssetServiceHistory.objects.filter(id=data_val['assetservicehistory_id']).values()
            print(service_history_type," == ",service_history_ash[0]['asset_service_history'])
            if service_history_type == service_history_ash[0]['asset_service_history'] :
                fill_the_data = "yes"
        
        print(fill_the_data)
        print(svc_hist_type_req_fl)
        if not alalshi_exist:
            if fill_the_data == "yes" and svc_hist_type_req_fl == "W1YS":
                # if svc_hist_type_req_fl == "W1YS":

                print('alalsh = ',alalsh)

                ### need to add more checking for to make sure there is only one data to enter ( woacalal_table.service_histories.add(alalsh) )
                
                # new_woacalal_count = WorkOrderActivityCompletionAssetLocationAssetList.objects.filter(asset_id=asset_id).count()
                # print("new_woacalal_count",new_woacalal_count)

                # if new_woacalal_count == 1:

                    # if queryset is None :

                woacalal_table = WorkOrderActivityCompletionAssetLocationAssetList.objects.get(node_id=node_id,asset_id=asset_id)
                print("tttttttttttttttttt = ",woacalal_table)
                woacalal_table.service_histories.add(alalsh)
                    
                # else :

                #     print("woac_id",woac_id)
                #     # woac_data = WorkOrderActivityCompletion.objects.filter(id=woac_id).values()
                #     queryset = WorkOrderActivityCompletion.objects.filter(id=woac_id).values_list('asset_location_asset_list', flat=True)
                #     print("queryset=====================",queryset)

                #     print('xxxxxxxxxxxxx')
                #     woacalal_table = WorkOrderActivityCompletionAssetLocationAssetList.objects.filter(node_id=node_id,asset_id=asset_id).values_list('id', flat=True)
                #     print("uuuuuuuuuuuuuuuuuuu = ",woacalal_table)
                #     for line in woacalal_table:
                #         print(line)
                #         if line in queryset : 
                #             print('exist',line)
                #             woacalal_data = WorkOrderActivityCompletionAssetLocationAssetList.objects.get(id=line)
                #             print(woacalal_data)
                #             woacalal_data.service_histories.add(alalsh)



def get_workorderactivity(from_date, to_date):

    payload = {
        "from_date": from_date,
        "to_date": to_date
    }

    # data = []

    # node_id = '831688426895'
    # asset_id = '004678152672'

    # woac_id = '5c6c7fdb-5579-498f-9600-10b0becfab2d'

    # # woac_data = WorkOrderActivityCompletion.objects.filter(id=woac_id).values()
    # queryset = WorkOrderActivityCompletion.objects.filter(id=woac_id).values_list('asset_location_asset_list', flat=True)
    # # print("queryset",queryset)

    # for line in queryset:
    #     print(line)

    # woacalal_table = WorkOrderActivityCompletionAssetLocationAssetList.objects.filter(node_id=node_id,asset_id=asset_id).values_list('id', flat=True)
    # # print("woacalal_table = ",woacalal_table)
    # for line in woacalal_table:

    #     if line in queryset : 
    #         print('exist',line)
    #         woacalal_data = WorkOrderActivityCompletionAssetLocationAssetList.objects.get(id=line)
    #         print(woacalal_data)

    #     # print(line)

    # return json.loads(data)



    r = requests.post("http://139.59.125.201/getWorkOrderActivity.php", data=payload)
    print(r)

    json_dictionary = json.loads(r.content)
    for key in json_dictionary:
        if (key == "results"):
            # print(key, ":", json_dictionary[key])
            if (type(json_dictionary[key]) == dict):
                # return single json
                print("dict")
                insert_into_work_order_activity(json_dictionary[key])
            elif (type(json_dictionary[key]) == list):
                # return array of json
                print("list")
                results_json = json_dictionary[key]
                for x in results_json:
                    insert_into_work_order_activity(x)

    return json.loads(r.content)





    # wsdl = "https://pasb-dev-uwa-iws.oracleindustry.com/ouaf/webservices/CM-WORKORDERACTIVITY?WSDL"
    # session = Session()
    # session.auth = HTTPBasicAuth("RFID_INTEGRATION", "Rfid_1nt")

    # client = Client(wsdl, transport=Transport(session=session),
    #                 settings=Settings(strict=False, raw_response=True))

    # request_data = {
    #     'FROM_DATE': '2020-09-01T18:00:21.000+00:00',
    #     'TO_DATE': '2020-10-01T18:00:21.000+00:00'
    # }

    # response = client.service.ExtractWorkOrderActivity(**request_data)
    # response_xml = response.content
    # # print(response_xml)
    # middleware_response_json = json.loads(
    #     json.dumps(xmltodict.parse(response_xml)))
    # return middleware_response_json['env:Envelope']['env:Body']['ouaf:ExtractWorkOrderActivity']['ouaf:results']
