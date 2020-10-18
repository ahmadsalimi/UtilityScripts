from paramiko import SSHClient
from tqdm import tqdm

def sftp_connect(server:str, username:str=None, password:str=None):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(server, username=username, password=password)
    return ssh.open_sftp()

def send_file(response, sftp, path):
    CHUNK_SIZE = 32768
    print(response)

    with sftp.open(path, 'w') as f:
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024) as bar:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    bar.update(CHUNK_SIZE)