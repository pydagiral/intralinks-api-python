import requests
import json

def get_exchanges(base_url, access_token):
    response = requests.get(base_url + '/v2/workspaces', headers={
        'Authorization': 'Bearer {}'.format(access_token)
    })
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    json_data = response.json()
    if 'workspace' not in json_data:
        raise Exception(response.text)
    exchanges = json_data['workspace']
    return exchanges

def get_splash(base_url, access_token, exchange_id):
    response = requests.get(
        base_url + '/v2/workspaces/{}/splash'.format(exchange_id), 
        headers={'Authorization': 'Bearer {}'.format(access_token)}
    )
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    json_data = response.json()
    if 'splash' not in json_data:
        raise Exception(response.text)
    splash = json_data['splash']
    return splash

def get_splash_image(base_url, access_token, exchange_id, file_path):
    response = requests.get(base_url + '/services/workspaces/splashImage', params={'workspaceId': exchange_id}, headers={
        'Authorization': 'Bearer {}'.format(access_token)
    }, stream=True)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    extensions = {
        'image/jpeg':'.jpg',
        'image/gif':'.gif',
    }
    extension = extensions[response.headers['Content-Type']]
    with open(file_path + extension, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk: 
                file.write(chunk)
    
    return file_path + extension

def accept_splash(base_url, access_token, exchange_id):
    response = requests.post(base_url + '/v2/workspaces/{}/splash'.format(exchange_id), data=json.dumps({
            "acceptSplash": True
        }), headers={
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
    })
    if response.status_code != 201:
        raise Exception(response.status_code, response.text)
    json_data = response.json()
    if 'state' not in json_data:
        raise Exception(response.text)
    accept_splash_state = json_data['state']
    return accept_splash_state