import ftplib
from ftplib import FTP
from sys import argv
import warnings
import functions as F
from tqdm import tqdm
import os

warnings.filterwarnings('ignore')


def _is_ftp_dir(ftp, name, guess_by_extension=True):
    """ simply determines if an item listed on the ftp server is a valid directory or not """

    # if the name has a "." in the fourth to last position, its probably a file extension
    # this is MUCH faster than trying to set every file to a working directory, and will work 99% of time.
    if guess_by_extension is True:
        if len(name) >= 4:
            if name[-4] == '.':
                return False

    original_cwd = ftp.pwd()  # remember the current working directory
    try:
        ftp.cwd(name)  # try to set directory to new name
        ftp.cwd(original_cwd)  # set it back to what it was
        return True

    except ftplib.error_perm as e:
        print(e)
        return False

    except Exception as e:
        print(e)
        return False

def generate_sftp_write(file, bar):
    def sftp_write(data):
        file.write(data)
        bar.update(len(data))
    return sftp_write

def _make_parent_dir(sftp, sftp_path):
    dirname = os.path.dirname(sftp_path)

    if not sftp.exists(dirname):
        _make_parent_dir(sftp, dirname)
        sftp.mkdir(dirname)


def _download_ftp_file(ftp, ftp_path, sftp, sftp_path):
    print("downloading " + ftp_path + " to " + sftp_path)
    
    _make_parent_dir(sftp, sftp_path)

    with sftp.open(sftp_path, 'w') as file:
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024) as bar:
            ftp.retrbinary("RETR {0}".format(ftp_path), generate_sftp_write(file, bar))


def _mirror_ftp_dir(ftp, ftp_path, sftp, sftp_path):
    for item in ftp.nlst(ftp_path):
        destination = sftp_path + '/' + item.split('/')[-1]
        if _is_ftp_dir(ftp, item, True):
            _mirror_ftp_dir(ftp, item, sftp, destination)
        else:
            _download_ftp_file(ftp, item, sftp, destination)


def download_ftp_tree(ftp, ftp_path, sftp, sftp_path):
    ftp_path = ftp_path.lstrip('/')
    sftp_path = sftp_path.rstrip('/')
    _mirror_ftp_dir(ftp, ftp_path, sftp, sftp_path)

if __name__ == "__main__":
    if len(argv) is not 7:
        print("Usage: python download_ftp.py ftp_server ftp_path ssh_server ssh_username ssh_password ssh_path")
    else:
        ftp_server = argv[1]
        ftp_path = argv[2]
        ssh_server = argv[3]
        ssh_username = argv[4]
        ssh_password = argv[5]
        ssh_path = argv[6]

        ftp = FTP(ftp_server)
        ftp.login("", "")
        sftp = F.sftp_connect(ssh_server, ssh_username, ssh_password)

        download_ftp_tree(ftp, ftp_path, sftp, ssh_path)
