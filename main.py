import sys
import requests
import uuid
from flask import Flask, request, render_template, make_response


app = Flask(__name__, static_url_path='', static_folder="./static")
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
        url="https://dealerapp.siriusxm.com/authService/100000002/appconfig",
        headers={
            "X-HTTP-Method-Override": "GET",
            "Accept": "*/*",
            "X-Voltmx-App-Secret": "c086fca8646a72cf391f8ae9f15e5331",
            "X-Voltmx-Integrity": "CD7EYEDRZX27UI;48E6933FED8492CE9261266AFCBD5AF17A2C2B4EB40C69A620056B02F90495A2",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "br, gzip, deflate",
            "X-Voltmx-App-Key": "67cfe0220c41a54cb4e768723ad56b41",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-ReportingParams": "",
        },
    )

    return response.json()


def login():
    response = SESSION.post(
        url="https://dealerapp.siriusxm.com/authService/100000002/login",
        headers={
            "X-Voltmx-Platform-Type": "ios",
            "Accept": "application/json",
            "X-Voltmx-App-Secret": "c086fca8646a72cf391f8ae9f15e5331",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Voltmx-SDK-Type": "js",
            "Accept-Encoding": "br, gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-SDK-Version": "9.5.36",
            "X-Voltmx-App-Key": "67cfe0220c41a54cb4e768723ad56b41",
        },
    )

    return response.json().get('claims_token').get('value')


def version_control(token: str, uuid4: str):
    response = SESSION.post(
        url="https://dealerapp.siriusxm.com/services/DealerAppService7/VersionControl",
        headers={
            "Accept": "*/*",
            "X-Voltmx-ReportingParams": '{"os":"16.1.1","dm":"unknown","did":"8FF62332-71B1-4699-B11B-7D32F9C12999",'
                                      '"ua":"iPhone","aid":"DealerApp","aname":"SXM Dealer","chnl":"mobile",'
                                      '"plat":"ios","aver":"2.4.0","atype":"native","stype":"b2c","kuid":"",'
                                      '"mfaid":"3de259b8-e39b-4f60-b2ba-ae3d4a2655bf",'
                                      '"mfbaseid":"5fa7a77c-aa7e-423f-b9bd-4fe67e91bb71","mfaname":"DealerApp",'
                                      '"sdkversion":"8.4.134","sdktype":"js","fid":"frmHome","sessiontype":"I",'
                                      '"rsid":"1668318090440-ac27-f025-7685","svcid":"VersionControl"}',
            "X-Voltmx-API-Version": "1.0",
            "X-Voltmx-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-Authorization": token,
        },
        data={
            "deviceCategory": "iPhone",
            "appver": "3.1.0",
            "deviceLocale": "en_US",
            "deviceModel": "iPhone%206%20Plus",
            "deviceVersion": "16.1.1",
            "deviceType": "",
        },
    )

    return response.json()


def get_properties(token: str, uuid4: str):
    response = SESSION.post(
        url="https://dealerapp.siriusxm.com/services/DealerAppService7/getProperties",
        headers={
            "Accept": "*/*",
            "X-Voltmx-ReportingParams": '{"os":"16.1.1","dm":"unknown","did":"8FF62332-71B1-4699-B11B-7D32F9C12999",'
                                      '"ua":"iPhone","aid":"DealerApp","aname":"SXM Dealer","chnl":"mobile",'
                                      '"plat":"ios","aver":"2.4.0","atype":"native","stype":"b2c","kuid":"",'
                                      '"mfaid":"3de259b8-e39b-4f60-b2ba-ae3d4a2655bf",'
                                      '"mfbaseid":"5fa7a77c-aa7e-423f-b9bd-4fe67e91bb71",'
                                      '"mfaname":"DealerApp","sdkversion":"8.4.134","sdktype":"js","fid":"frmHome",'
                                      '"sessiontype":"I","rsid":"1668318090440-ac27-f025-7685",'
                                      '"svcid":"getProperties"}',
            "X-Voltmx-API-Version": "1.0",
            "X-Voltmx-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-Authorization": token,
        },
        data={
        },
    )

    return response.json()


def update_device_sat_refresh_with_priority(device_id: str, token: str, uuid4: str):
    response = SESSION.post(
        url="https://dealerapp.siriusxm.com/services/USUpdateDeviceSATRefresh/updateDeviceSATRefreshWithPriority",
        headers={
            "Accept": "*/*",
            "X-Voltmx-ReportingParams": '{"os":"16.1.1","dm":"unknown","did":"8FF62332-71B1-4699-B11B-7D32F9C12999",'
                                      '"ua":"iPhone","aid":"DealerApp","aname":"SXM Dealer","chnl":"mobile",'
                                      '"plat":"ios","aver":"2.4.0","atype":"native","stype":"b2c","kuid":"",'
                                      '"mfaid":"3de259b8-e39b-4f60-b2ba-ae3d4a2655bf",'
                                      '"mfbaseid":"5fa7a77c-aa7e-423f-b9bd-4fe67e91bb71","mfaname":"DealerApp",'
                                      '"sdkversion":"8.4.134","sdktype":"js","fid":"frmRefresh","sessiontype":"I",'
                                      '"rsid":"1668318090440-ac27-f025-7685",'
                                      '"svcid":"updateDeviceSATRefreshWithPriority"}',
            "X-Voltmx-API-Version": "1.0",
            "X-Voltmx-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-Authorization": token,
        },
        data={
            "deviceId": device_id,
            "appVersion": "3.1.0",
            "lng": "-86.210274696",
            "provisionPackageName": "",
            "vin": "",
            "deviceID": uuid4,
            "flow_name": "Enter Radio ID",
            "provisionPriority": "2",
            "provisionType": "activate",
            "phone": "",
            "device_Type": "iPhone unknown",
            "note": "1",
            "AuthName": "",
            "os_Version": "iPhone 16.1.1",
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
        url="https://dealerapp.siriusxm.com/services/DemoConsumptionRules/GetCRMAccountPlanInformation",
        headers={
            "Accept": "*/*",
            "X-Voltmx-ReportingParams": '{"os":"16.1.1","dm":"unknown","did":"8FF62332-71B1-4699-B11B-7D32F9C12999",'
                                      '"ua":"iPhone","aid":"DealerApp","aname":"SXM Dealer","chnl":"mobile",'
                                      '"plat":"ios","aver":"2.4.0","atype":"native","stype":"b2c","kuid":"",'
                                      '"mfaid":"3de259b8-e39b-4f60-b2ba-ae3d4a2655bf",'
                                      '"mfbaseid":"5fa7a77c-aa7e-423f-b9bd-4fe67e91bb71","mfaname":"DealerApp",'
                                      '"sdkversion":"8.4.134","sdktype":"js","fid":"frmRefresh","sessiontype":"I",'
                                      '"rsid":"1668318090440-ac27-f025-7685","svcid":"GetCRMAccountPlanInformation"}',
            "X-Voltmx-API-Version": "1.0",
            "X-Voltmx-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-Authorization": token,
        },
        data={
            "seqVal": seq_value,
            "deviceId": device_id,
        },
    )

    return response.json()


def db_update_for_google(device_id: str, token: str, seq: str, uuid4: str):
    response = SESSION.post(
        url="https://dealerapp.siriusxm.com/services/DBSuccessUpdate/DBUpdateForGoogle",
      headers={
          "Accept": "*/*",
          "X-Voltmx-API-Version": "1.0",
          "X-Voltmx-DeviceId": uuid4,
          "Accept-Language": "en-us",
          "Accept-Encoding": "br, gzip, deflate",
          "Content-Type": "application/x-www-form-urlencoded",
          "User-Agent":
          "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
          "X-Voltmx-Authorization": token,
      },
      data={
          "OM_ELIGIBILITY_STATUS": "Eligible",
          "appVersion": "3.1.0",
          "flag": "failure",
          "Radio_ID": device_id,
          "deviceID": uuid4,
          "G_PLACES_REQUEST": "",
          "OS_Version": "iPhone 17.1.2",
          "G_PLACES_RESPONSE": "",
          "Confirmation_Status": "SUCCESS",
          "seqVal": seq,
      },
    )

    return response.json()


def block_list_device(token: str, uuid4: str):
    response = SESSION.post(
        url="https://dealerapp.siriusxm.com/services/USBlockListDevice/BlockListDevice",
        headers={
            "Accept": "*/*",
            "X-Voltmx-ReportingParams": '{"os":"16.1.1","dm":"unknown","did":"8FF62332-71B1-4699-B11B-7D32F9C12999",'
                                      '"ua":"iPhone","aid":"DealerApp","aname":"SXM Dealer","chnl":"mobile",'
                                      '"plat":"ios","aver":"2.4.0","atype":"native","stype":"b2c","kuid":"",'
                                      '"mfaid":"3de259b8-e39b-4f60-b2ba-ae3d4a2655bf",'
                                      '"mfbaseid":"5fa7a77c-aa7e-423f-b9bd-4fe67e91bb71","mfaname":"DealerApp",'
                                      '"sdkversion":"8.4.134","sdktype":"js","fid":"frmRefresh","sessiontype":"I",'
                                      '"rsid":"1668318090440-ac27-f025-7685","svcid":"BlockListDevice"}',
            "X-Voltmx-API-Version": "1.0",
            "X-Voltmx-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-Authorization": token,
        },
        data={
            "deviceId": uuid4,
        },
    )

    return response.json()


def create_account(device_id: str, token: str, seq_value, uuid4: str):

    response = SESSION.post(
        url="https://dealerapp.siriusxm.com/services/DealerAppService3/CreateAccount",
        headers={
            "Connection": "close",
            "Accept": "*/*",
            "X-Voltmx-ReportingParams": '{"os":"16.1.1","dm":"unknown","did":"8FF62332-71B1-4699-B11B-7D32F9C12999",'
                                      '"ua":"iPhone","aid":"DealerApp","aname":"SXM Dealer","chnl":"mobile",'
                                      '"plat":"ios","aver":"2.4.0","atype":"native","stype":"b2c","kuid":"",'
                                      '"mfaid":"3de259b8-e39b-4f60-b2ba-ae3d4a2655bf",'
                                      '"mfbaseid":"5fa7a77c-aa7e-423f-b9bd-4fe67e91bb71","mfaname":"DealerApp",'
                                      '"sdkversion":"8.4.134","sdktype":"js","fid":"frmRefresh","sessiontype":"I",'
                                      '"rsid":"1668318090440-ac27-f025-7685","svcid":"CreateAccount"}',
            "X-Voltmx-API-Version": "1.0",
            "X-Voltmx-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-Authorization": token,
        },
        data={
            "seqVal": seq_value,
            "deviceId": device_id,
            "oracleCXFailed": "1",
            "appVersion": "3.1.0",
        },
    )

    return response.json()


def update_device_sat_refresh_with_priority_cc(device_id: str, token: str, uuid4: str):
    response = SESSION.post(
        url="https://dealerapp.siriusxm.com/services/USUpdateDeviceRefreshForCC/updateDeviceSATRefreshWithPriority",
        headers={
            "Accept": "*/*",
            "X-Voltmx-ReportingParams": '{"os":"16.1.1","dm":"unknown","did":"8FF62332-71B1-4699-B11B-7D32F9C12999",'
                                      '"ua":"iPhone","aid":"DealerApp","aname":"SXM Dealer","chnl":"mobile",'
                                      '"plat":"ios","aver":"2.4.0","atype":"native","stype":"b2c","kuid":"",'
                                      '"mfaid":"3de259b8-e39b-4f60-b2ba-ae3d4a2655bf",'
                                      '"mfbaseid":"5fa7a77c-aa7e-423f-b9bd-4fe67e91bb71","mfaname":"DealerApp",'
                                      '"sdkversion":"8.4.134","sdktype":"js","fid":"frmRefresh","sessiontype":"I",'
                                      '"rsid":"1668318090440-ac27-f025-7685",'
                                      '"svcid":"updateDeviceSATRefreshWithPriority"}',
            "X-Voltmx-API-Version": "1.0",
            "X-Voltmx-DeviceId": uuid4,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "SiriusXM%20Dealer/3.1.0 CFNetwork/3826.500.131 Darwin/24.5.0",
            "X-Voltmx-Authorization": token,
        },
        data={
            "deviceId": device_id,
            "provisionPriority": "2",
            "appVersion": "3.1.0",
            "note": "1",
            "provisionPackageName": "",
            "dmCode": "",
            "device_Type": "iPhone iPhone 14 Pro",
            "deviceID": uuid4,
            "os_Version": "iPhone 18.5",
            "provisionType": "activate",
            "provisionDate": "",
            "base64": "X06FDae2079Ge5H9PYW5sg%3D%3D",
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
    db_update_for_google(device_id, auth_token, seq, uuid4)
    block_list_device(auth_token, uuid4)
    results['create'] = create_account(device_id, auth_token, seq, uuid4)
    results['refresh'] = update_device_sat_refresh_with_priority_cc(device_id, auth_token, uuid4)
    db_update_for_google(device_id, auth_token, seq, uuid4)

    return results


@app.route("/", methods=['GET', 'POST'])
def index() -> str:
    test = 'test' in request.args.keys()

    if test:
        result = {
            'success': True,
            'responses': RESPONSES.get('activated'),
        }
        return render_template('index.html', result=result)
    
    if request.method == 'GET': # If request is GET and there is a cookie with radio_id, use it to prefill the form with the radio_id
        radio_id = request.cookies.get('radio_id')
        if radio_id:
            return render_template('index.html', radio_id=radio_id)

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

        if result['success']:
            resp = make_response(render_template('index.html', result=result, radio_id=radio_id))
            resp.set_cookie('radio_id', radio_id, max_age=60 * 60 * 24 * 365)
            return resp
        

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
        app.run()
