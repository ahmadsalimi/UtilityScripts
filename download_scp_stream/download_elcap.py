from bs4 import BeautifulSoup
import requests as R
from urllib.parse import urljoin
import functions as F
import sys
import warnings


def get_all_forms(response):
    # for javascript driven website
    # res.html.render()
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value = input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append(
            {"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def submit_download_form(session, url, form_details, hcode, hname, sel):
    data = {}
    for input_tag in form_details["inputs"]:
        data[input_tag["name"]] = input_tag["value"]

    data['help'] = hcode
    data['title'] = hname
    data['sel'] = sel

    url = urljoin(url, form_details["action"])

    return session.post(url, data=data, verify=False, stream=True)

def get_response(subset):
    session = R.Session()
    url = "https://veet.via.cornell.edu/lungdb.html"

    # LOG IN
    login_form_details = get_form_details(get_all_forms(session.get(url, verify=False))[0])
    login_data = {
        'inst': 'PC',
        'instkey': 'public',
        'perskey': 'ngyf1h6',
        None: ''
    }
    login_url = urljoin(url, login_form_details["action"])

    login_response = session.post(login_url, data=login_data)

    if (login_response.status_code == 200):
        print('LOGGED IN SUCCESSFULLY')
    else:
        raise Exception("Log in failed!", str(login_response.content))

    download_form_details = get_form_details(list(filter(lambda form: form.attrs['name'] == 'ghelp', get_all_forms(login_response)))[0])

    return submit_download_form(session, url, download_form_details, 'PCsub' + subset + '-20090909.zip', 'ELCAP Image Download', '2')


warnings.filterwarnings('ignore')

if len(sys.argv) is not 6:
    raise Exception(
        "Usage: python download_elcap.py subset server_address username password path")

subset = sys.argv[1]
server = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
path = sys.argv[5]

response = get_response(subset)
sftp = F.sftp_connect(server, username, password)
F.send_file(response, sftp, path)

