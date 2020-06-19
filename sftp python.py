import paramiko

ssh_client = paramiko.SSHClient() 
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh_client.connect(hostname='ftp.archivagroup.it',port=2411,username='berardibulloneriesrl',password='fzU4@wUD_Joy') 
s = ssh_client.open_sftp()

for i in s.listdir():
	lstatout=str(s.lstat(i)).split()[0]
	if 'd' in lstatout: print(i), 'is a directory'

s.put('C:/Users/tommolini/Desktop/Fatturazione/Fatture2.txt', '/TEST/file.ext')