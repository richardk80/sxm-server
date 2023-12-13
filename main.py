import sys
import requests
import uuid
from flask import Flask, request, render_template


api = Flask(__name__)

SESSION = requests.session()

RESPONSES = {
    'activated': {
        'crm': {'resultCode': 'SUCCESS', 'opstatus': 0, 'httpStatusCode': 200},
        'create': {'resultData': [{'resultCode': 'SUCCESS'}], 'opstatus': 0, 'httpStatusCode': 200},
        'refresh': {'opstatus': 0, 'errors': [{'resultCode': 'SUCCESS'}], 'httpStatusCode': 200},
    },
    'already_activated': {
        'crm': {'resultCode': 'SUCCESS', 'opstatus': 0, 'httpStatusCode': 200},
        'create': {'resultData': [{'resultCode': 'FAILURE'}, {'code': '11-03-ACCT-1073'},
                                  {'message': 'Device ID is already active'}], 'opstatus': 0, 'httpStatusCode': 200},
        'refresh': {'opstatus': 0, 'errors': [{'resultCode': 'SUCCESS'}], 'httpStatusCode': 200},
    }
}


def appconfig():
    response = SESSION.post(
        url="https://mcare.siriusxm.ca/authService/100000002/appconfig",
        headers={
            "X-HTTP-Method-Override": "GET",
            "Accept": "*/*",
            "X-Kony-App-Secret": "e3048b73f2f7a6c069f7d8abf5864115",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "X-Kony-App-Key": "85ee60a3c8f011baaeba01ff3a5ae2c9",
            "User-Agent": "SXM Dealer/3 CFNetwork/1474 Darwin/23.0.0",
        },
    )

    return response.json()


def login():
    response = SESSION.post(
        url="https://mcare.siriusxm.ca/authService/100000002/login",
        headers={
            "X-Kony-Platform-Type": "ios",
            "Accept": "application/json",
            "X-Kony-App-Secret": "e3048b73f2f7a6c069f7d8abf5864115",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Kony-SDK-Type": "js",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SXM Dealer/3 CFNetwork/1474 Darwin/23.0.0",
            "X-Kony-SDK-Version": "8.4.134",
            "X-Kony-App-Key": "85ee60a3c8f011baaeba01ff3a5ae2c9",
        },
    )

    return response.json().get('claims_token').get('value')


def version_control(token: str, uuid4: str):
    response = SESSION.post(
        url="https://mcare.siriusxm.ca/services/DealerAppService7/VersionControl",
        headers={
            "Accept": "*/*",
            "X-Kony-ReportingParams": '{"os":"16.1.1","dm":"unknown","did":uuid4,'
                                      '"ua":"iPhone","aid":"DealerApp","aname":"SXM Dealer","chnl":"mobile",'
                                      '"plat":"ios","aver":"2.4.0","atype":"native","stype":"b2c","kuid":"",'
                                      '"mfaid":"3de259b8-e39b-4f60-b2ba-ae3d4a2655bf",'
                                      '"mfbaseid":"5fa7a77c-aa7e-423f-b9bd-4fe67e91bb71","mfaname":"DealerApp",'
                                      '"sdkversion":"8.4.134","sdktype":"js","fid":"frmHome","sessiontype":"I",'
                                      '"rsid":"1668318090440-ac27-f025-7685","svcid":"VersionControl"}',
            "X-Kony-API-Version": "1.0",
            "X-Kony-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SXM Dealer/3 CFNetwork/1399 Darwin/22.1.0",
            "X-Kony-Authorization": token,
        },
        data={
            "deviceCategory": "iPhone",
            "appver": "2.4.0",
            "deviceLocale": "en_US",
            "deviceModel": "unknown",
            "deviceVersion": "16.1.1",
            "deviceType": "",
        },
    )

    return response.json()


def get_properties(token: str, uuid4: str):
    response = SESSION.post(
        url="https://mcare.siriusxm.ca/services/DealerAppService7/getProperties",
        headers={
            "Accept": "*/*",
            "X-Kony-API-Version": "1.0",
            "X-Kony-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SXM Dealer/3 CFNetwork/1474 Darwin/23.0.0",
            "X-Kony-Authorization": token,
        },
        data={},
    )

    return response.json()


def update_device_sat_refresh_with_priority(device_id: str, token: str, uuid4: str):
    response = SESSION.post(
        url="https://mcare.siriusxm.ca/services/USUpdateDeviceSATRefresh/updateDeviceSATRefreshWithPriority",
        headers={
            "Accept": "*/*",
            "X-Kony-API-Version": "1.0",
            "X-Kony-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SXM Dealer/3 CFNetwork/1474 Darwin/23.0.0",
            "X-Kony-Authorization": token,
        },
        data={
            "deviceId": device_id,
            "appVersion": "2.4.0",
            "lng": "-86.210274696",
            "provisionPackageName": "",
            "vin": "",
            "deviceID": uuid4,
            "flow_name": "Enter Radio ID",
            "provisionPriority": "2",
            "provisionType": "activate",
            "phone": "",
            "note": "1",
            "AuthName": "",
            "AuthPwd": "",
            "lat": "32.374343677",
            "provisionDate": "",
            "dmCode": "",
            "vehicle_active_flag": "",
            "base64": "X06FDae2079Ge5H9PYW5sg==",
        },
    )

    return response.json()


def get_crm_account_plan_information(device_id: str, token: str, seq_value, uuid4: str):
    response = SESSION.post(
        url=
        "https://mcare.siriusxm.ca/services/DemoConsumptionRules/GetCRMAccountPlanInformation",
        headers={
            "Accept": "*/*",
            "X-Kony-API-Version": "1.0",
            "X-Kony-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SXM Dealer/3 CFNetwork/1474 Darwin/23.0.0",
            "X-Kony-Authorization": token,
        },
        data={
            "seqVal": seq_value,
            "deviceId": device_id,
        },
    )
    return response.json()


def db_update_for_google():
    response = SESSION.post(
        url="https://mcare.siriusxm.ca/services/DBSuccessUpdate/DBUpdateForGoogle"
    )

    return response.json()


def block_list_device(token: str, uuid4: str):
    response = SESSION.post(
        url=
        "https://mcare.siriusxm.ca/services/USBlockListDevice/BlockListDevice",
        headers={
            "Accept": "*/*",
            "X-Kony-API-Version": "1.0",
            "X-Kony-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SXM Dealer/3 CFNetwork/1474 Darwin/23.0.0",
            "X-Kony-Authorization": token,
        },
        data={
            "deviceId": uuid4,
        },
    )
    return response.json()


def create_account(device_id: str, token: str, seq_value, uuid4: str):
    response = SESSION.post(
        url=
        "https://mcare.siriusxm.ca/services/DealerAppService3/CreateAccount",
        headers={
            "Connection": "close",
            "Accept": "*/*",
            "X-Kony-API-Version": "1.0",
            "X-Kony-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SXM Dealer/3 CFNetwork/1474 Darwin/23.0.0",
            "X-Kony-Authorization": token,
        },
        data={
            "seqVal": seq_value,
            "deviceId": device_id,
            "oracleCXFailed": "1",
            "appVersion": "2.4.0",
        },
    )
    return response.json()


def update_device_sat_refresh_with_priority_cc(device_id: str, token: str,
                                               uuid4: str):
    response = SESSION.post(
        url=
        "https://mcare.siriusxm.ca/services/USUpdateDeviceRefreshForCC/updateDeviceSATRefreshWithPriority",
        headers={
            "Accept": "*/*",
            "X-Kony-API-Version": "1.0",
            "X-Kony-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SXM Dealer/3 CFNetwork/1474 Darwin/23.0.0",
            "X-Kony-Authorization": token,
        },
        data={
            "deviceId": device_id,
            "provisionPriority": "2",
            "appVersion": "2.4.0",
            "note": "1",
            "provisionPackageName": "",
            "dmCode": "",
            "deviceID": uuid4,
            "provisionType": "activate",
            "provisionDate": "",
        },
    )
    return response.json()


def process(device_id: str):

    results = {}

    appconfig()
    auth_token = login()
    uuid4 = str(uuid.uuid4())
    version_control(auth_token, uuid4)
    get_properties(auth_token, uuid4)
    response = update_device_sat_refresh_with_priority(device_id, auth_token, uuid4)
    seq = int(response.get('seqValue'))
    results['crm'] = get_crm_account_plan_information(device_id, auth_token, seq, uuid4)
    db_update_for_google()
    block_list_device(auth_token, uuid4)
    results['create'] = create_account(device_id, auth_token, seq, uuid4)
    results['refresh'] = update_device_sat_refresh_with_priority_cc(device_id, auth_token, uuid4)
    db_update_for_google()

    return results


@api.route("/", methods=['GET', 'POST'])
def index() -> str:
    test = 'test' in request.args.keys()

    if test:
        result = {
            'success': True,
            'responses': RESPONSES.get('activated'),
        }
        return render_template('index.html', result=result)

    if request.method == 'POST':

        radio_id = request.form.get('radio_id').upper().strip()
        result = {
            'success': False,
            'responses': process(radio_id),
        }

        responses = {k: result.get('responses')[k] for k in result.get('responses').keys()}
        if responses.get('crm', {}).get('deviceId'):
            responses['crm'].pop('deviceId')

        result['success'] = responses == RESPONSES.get('activated') or responses == RESPONSES.get('already_activated')

        return render_template('index.html', result=result)

    else:
        return render_template('index.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        radio_id_input = sys.argv[1].upper().strip()
        print(f'Processing for Radio ID "{radio_id_input}"...')
        for key, value in process(radio_id_input).items():
            print(f"\n{key}:\n{value.strip()}")
    else:
        api.run()
