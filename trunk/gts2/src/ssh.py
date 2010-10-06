#!/usr/bin/env python

"""This runs a command on a remote host using SSH. At the prompts enter hostname,user, and password.

$Id: sshls.py 489 2007-11-28 23:40:34Z noah $
"""

import pexpect
import getpass, os

class SSHCommand:

	def __init__(self,user, host, password, command):
		self.user=user;
		self.host=host;
		self.password=password;
		self.command=command;

	def launch(self):

    		"""This runs a command on the remote host. This could also be done with the
pxssh class, but this demonstrates what that class does at a simpler level.
This returns a pexpect.spawn object. This handles the case when you try to
connect to a new host and ssh asks you if you want to accept the public key
fingerprint and continue connecting. """

		user=self.user;
		host=self.host;
		password=self.password;
		command=self.command;

    		ssh_newkey = 'Are you sure you want to continue connecting';
    		child = pexpect.spawn('ssh %s@%s %s'%(user, host, command));
		if password==None:
			i = child.expect([pexpect.TIMEOUT,ssh_newkey,pexpect.EOF],timeout=300);
		else:
    			i = child.expect([pexpect.TIMEOUT,ssh_newkey, 'password: '],timeout=10);
    		if i == 0: # Timeout
        		print 'ERROR!';
        		print 'SSH could not login. Here is what SSH said:';
        		print child.before, child.after;
        		return None;
    		if i == 1: # SSH does not have the public key. Just accept it.
        		child.sendline ('yes');
        		child.expect ('password: ');
        		i = child.expect([ 'password: '],timeout=10);
        		if i != 0: # Timeout
            			print 'ERROR!';
            			print 'SSH could not login. Here is what SSH said:';
            			print child.before, child.after;
            			return None;
		if not password==None:       
    			child.sendline(password);
			child.expect(pexpect.EOF,timeout=300);
    		return child.before;

	

if __name__ == '__main__':
    try:
        #host = raw_input('Hostname: ')
	#user = raw_input('User: ')
	user='malagoli'
	#password = getpass.getpass('Password: ')
	#print "'"+password+"'"
	
	for host in ['ambrogio.cs.unibo.it','maria.cs.unibo.it']:
		child = SSHCommand (user, host,None,'/bin/ls -l').launch();
		print "\'{0}\'".format(child);
	#print child.before
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(1)

