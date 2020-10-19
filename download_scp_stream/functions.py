from tqdm import tqdm
import pysftp


def sftp_connect(server, username=None, password=None):
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