import paramiko
from contextlib import contextmanager
from flask import current_app


@contextmanager
def sftp_ctx():
    """
    Context manager that provides an SFTP client object
    (an SFTP session across an open SSH Transport)
    """
    transport = paramiko.Transport(('localhost', 22))
    transport.connect(username='btang', pkey=paramiko.RSAKey(filename='/Users/btang/.ssh/id_rsa'))
    # transport = paramiko.Transport((os.environ.get('SFTP_HOSTNAME'), os.environ.get('SFTP_PORT')))
    # transport.connect(username=os.environ.get('SFTP_USERNAME'),
    #               pkey=paramiko.RSAKey(filename=os.environ.get('SFTP_RSA_KEY_FILE')))
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        yield sftp
    except Exception as e:
        current_app.logger.error("Exception occurred with SFTP: {}".format(e))
    finally:
        sftp.close()
        transport.close()
