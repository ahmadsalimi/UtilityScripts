import sys
import warnings
import requests as R
import functions as F

warnings.filterwarnings('ignore')

if len(sys.argv) is not 6:
    print("Usage: python direct_download.py url server_address username password path")
else:
    url = sys.argv[1]
    server = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    path = sys.argv[5]

    response = R.get(url, stream = True)
    sftp = F.sftp_connect(server, username, password)
    F.send_file(response, sftp, path)