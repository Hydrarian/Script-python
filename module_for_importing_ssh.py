import paramiko
import logging

class SSH(object):

    def __init__(self):
        pass

    def est_conn(self, ip, username, password, n_port):
    	#logging.basicConfig()
		#logging.getLogger("paramiko").setLevel(logging.WARNING) # for example
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        ssh.connect(hostname=ip, port=n_port, username=username, password=password, timeout=10)
        print("Asserting that ssh connection has been established...")
        assert ssh

        return ssh

ssh = SSH()