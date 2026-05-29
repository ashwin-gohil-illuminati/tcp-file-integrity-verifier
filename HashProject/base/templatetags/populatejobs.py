from django import template
import requests

register = template.Library()

apiURL = 'http://127.0.0.1:5000/'

def populate(request):

    
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}"
        }
    
    result = requests.get(apiURL+'hash/scanjobs', headers=header)
    data = result.json()
    if result.status_code == 200:
        #data = result.json()
        return data
    elif result.status_code == 404:
        return None


def populaterescanjobs(request):
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}"
        }
    result = requests.get(apiURL+'hash/rescanjobs', headers=header)
    data = result.json()
    if result.status_code == 200:
        #data = result.json()
        return data
    elif result.status_code == 404:
        return None



register.filter('populaterescanjobs', populaterescanjobs)
register.filter('populate', populate)