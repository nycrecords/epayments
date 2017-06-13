import paramiko
from contextlib import contextmanager
from flask import current_app


@contextmanager
def sftp_ctx():
    """
    Context manager that provides an SFTP client object
    (an SFTP session across an open SSH Transport)
    """
    transport = paramiko.Transport((current_app.config['SFTP_HOSTNAME'], current_app.config['SFTP_PORT']))
    transport.connect(username=current_app.config['SFTP_USERNAME'],
                      pkey=paramiko.RSAKey(filename=current_app.config['SFTP_RSA_KEY_FILE']))
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        yield sftp
    except Exception as e:
        current_app.logger.error("Exception occurred with SFTP: {}".format(e))
    finally:
        sftp.close()
        transport.close()


