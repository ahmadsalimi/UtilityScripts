import requests as R
import functions as F

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def get_response(file_id:str):
    URL = "https://docs.google.com/uc?export=download"
    session = R.Session()

    response = session.get(URL, params = { 'id' : file_id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : file_id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    
    return response

def send_from_gdrive(id, server, username, password, path):
    sftp = F.sftp_connect(server, username, password)
    response = get_response(file_id)
    F.send_file(response, sftp, path)

if __name__ == "__main__":
    import sys
    import warnings

    warnings.filterwarnings('ignore')

    if len(sys.argv) is not 6:
        print("Usage: python gdrive_download.py drive_file_id server_address username password path")
    else:
        file_id = sys.argv[1]
        server = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
        path = sys.argv[5]

        send_from_gdrive(file_id, server, username, password, path)
