import requests
# import json

# extract values from nested json
def json_extract(obj, key):
    arr = []
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    values = extract(obj, arr, key)
    return values

def get_district_number(ZIPcode):
    endpoint = "https://api.geocod.io/v1.7/geocode"
    params   = {'api_key':'b12b4b2046b214a066a2363130b422b63a26222', 'fields':'cd', 'q':ZIPcode,}
    response = requests.get(endpoint, params=params)

    if response.text.find('error') > 0:
        return 0

    return json_extract(response.json(),'district_number')[0]


def get_bills():
    url = 'https://api.propublica.org/congress/v1/bills/search.json?sort=date&dir=desc'
    headers = {'X-API-Key': 'yh0XpOTmFdd8SRfOHu2fCNNnAXbXp4jC52zeSLdV'}
    api_request = requests.get(url, headers = headers)
    bills = api_request.json()['results'][0]['bills']
    # for bill in bills: 
        # print(bill['number'], '- ', bill['short_title'], ': ', bill['introduced_date'], bill['congressdotgov_url'])
    return bills

