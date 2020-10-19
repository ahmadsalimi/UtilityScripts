# from paramiko import SSHClient
from tqdm import tqdm
import pysftp


def sftp_connect(server, username=None, password=None):
    # ssh = SSHClient()
    # ssh.load_system_host_keys()
    # ssh.connect(server, username=username, password=password)
    # return ssh.open_sftp()

    return pysftp.Connection(server, username=username, password=password)

def send_file(response, sftp, path):
    CHUNK_SIZE = 32768
    print(response)

    with sftp.open(path, 'w') as f:
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024) as bar:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    bar.update(CHUNK_SIZE)