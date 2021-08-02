import asyncio
import requests
import urllib
import time
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# Async parameter
MAX_WORKERS = 100
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


def async_download(application_numbers_range, year):

    request_parameters = get_request_parameters()
    court_decisions = []

    # Run async function
    future = asyncio.ensure_future(download_task(application_numbers_range, court_decisions, year, request_parameters))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(future)

    return court_decisions


def get_request_parameters():
    """
    :return: parameters for subsequent requests to https://app.echr.coe.int/SOP/index.aspx?lg=en
    """
    url = "https://app.echr.coe.int/SOP/index.aspx?lg=en"

    try:
        response = requests.request("GET", url=url, timeout=3)
    except Exception as e:
        print(e)
        return get_request_parameters()

    soup = BeautifulSoup(response.text, 'html.parser')

    request_parameters = {
        'viewstate': soup.find(id="__VIEWSTATE").get('value'),
        'viewstategenerator': soup.find(id="__VIEWSTATEGENERATOR").get('value'),
        'eventvalidation': soup.find(id="__EVENTVALIDATION").get('value')
    }

    return request_parameters


async def download_task(application_numbers_range, results, year, request_parameters):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        loop = asyncio.get_event_loop()
        for number in application_numbers_range:
            loop.run_in_executor(executor, catch_court_data, *(results, number, year, request_parameters))


def catch_court_data(results, number, year, request_parameters):
    """
    :return: ECHR court decision data as json
    """

    response = send_final_request(request_parameters, number, year)
    court_data = handle_response(response, number, year)

    if court_data is not None:
        results.append(court_data)


def send_final_request(request_parameters, number, year):
    """
    :return: court data from https://app.echr.coe.int/SOP/index.aspx?lg=en
    """
    url = "https://app.echr.coe.int/SOP/index.aspx?lg=en"
    payload = '__VIEWSTATE=' \
              + urllib.parse.quote_plus(request_parameters['viewstate']) \
              + '&__VIEWSTATEGENERATOR=' \
              + urllib.parse.quote_plus(request_parameters['viewstategenerator']) \
              + '&__EVENTVALIDATION=' \
              + urllib.parse.quote_plus(request_parameters['eventvalidation']) \
              + '&tbregno=' + str(number) + '%2F' + str(year) \
              + '&btngetdoc=Submit'

    headers = {
          'Cookie': 'SERVERID=Court177',
          'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.request("POST", url=url, headers=headers, data=payload, timeout=3)
    except Exception as e:
        return send_final_request(request_parameters, number, year)

    return response


def handle_response(response, number, year):
    soup = BeautifulSoup(response.text, 'html.parser')
    error = get_element_id(soup, "lblErrorMessage")

    if error is None:
        major_events = get_major_events(soup)

        echr_court_decision_data = {
            'application_number_id': str(number),
            'application_number_year': str(year),
            'application_number': get_element_id(soup, "lblRegisteredNo"),
            'application_title': get_element_id(soup, "lblCaseTitle"),
            'date_of_introduction': get_element_id(soup, "lblDateOfIntroduction"),
            'name_of_representative': get_element_id(soup, "lblRepresentativeName"),
            'current_state_of_proceedings': get_element_id(soup, "lblCurrentSOP"),
            'last_major_event_date': get_element_id(soup, "lblLME"),
            'last_major_event_description': get_element_id(soup, "lblLMEDesc"),
            'major_events': str(major_events)
        }

        return echr_court_decision_data

    else:
        return None


def get_element_id(soup, element_id):
    try:
        value = soup.find(id=element_id).text
        return value
    except Exception:
        return None


def get_major_events(soup):
    """
    :return: ECHR court decision major events table as list of dictionaries
    """
    try:
        table = soup.find(id="gvLMES")
        rows = table.findAll('tr')[1:]
        events = [{"Description": row.findAll('td')[0].text, "Event date":row.findAll('td')[1].text} for row in rows]
        return events
    except Exception:
        return None


# if __name__ == '__main__':
#     data = download_year_data(14, 100)
