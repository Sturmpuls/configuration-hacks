import os
from pathlib import Path

# pip install paramiko PySocks
import paramiko
import socks


# Helper function
def credentials(file):
    with open(file, 'r') as f:
        for line in f:
            user, pwd = line.strip().split(':')
    return user, pwd


# Connection Configuration
proxy_addr = 'proxy.host.address'
proxy_port = 1080
host_addr = 'sftp.host.address'
host_port = 22

# credentials in the form of user:pwd
credentials_path = "~/credentials.txt"
user, pwd = credentials(credentials_path)

# Data Configuration
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
file_src = './file.file'
file_dst = current_path / 'file.file'


if __name__ == '__main__':
    # Setup SOCKS5 Proxy
    s = socks.socksocket()
    s.set_proxy(
        proxy_type=socks.SOCKS5,
        addr=proxy_addr,
        port=proxy_port
    )
    s.connect((host_addr, host_port))

    # Connect to SFTP via Proxy
    transport = paramiko.Transport(s)
    transport.connect(username=user,password=pwd)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Sanity check
    print('Contents:', sftp.listdir())

    # Download actual file
    sftp.get(file_src, file_dst)
    print('Download done.')

    # Close connections
    sftp.close()
    transport.close()
    s.close()
