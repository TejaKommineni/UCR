import requests
import json

def get_pre_applications(token, url, format='json'):
    data = {
        'token': token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': format
    }
    r = requests.post(url,data=data)
    return r.json()

if __name__ == "__main__":
    token = ""
    url   = "https://redcap01.brisc.utah.edu/ccts/redcap/api/"

    r = get_pre_applications(token, url)
    with open("test.json", 'w') as f:
        json.dump(r,f)


