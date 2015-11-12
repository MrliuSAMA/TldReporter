import subprocess
import pexpect
import sys
import os
import pprint
import re

CUR_PATH = "dummy"
PRINT = "yes"
SigFile = "dummy"
KeyFile = "dummy"
ServerPath = "dummy"
DataFile = "dummy"

def init():
	#get cur file dir
	global CUR_PATH
	path = sys.path[0]
	if os.path.isdir(path) == True:
		CUR_PATH = path
	elif os.path.isfile(path):
		CUR_PATH = os.path.dirname(path)

	global SigFile
	global KeyFile
	global ServerPath
	global DataFile
	f = open("%s/%s" % (CUR_PATH,"Configuration.in"))
	lines = f.readlines()
	pprint.pprint(lines)
	for linenum in range(len(lines)):
		if lines[linenum].strip().split()[0] == "ServerPath":
			ServerPath = lines[linenum].strip().split()[-1]
		elif lines[linenum].strip().split()[0] == "SigFile":
			SigFile = lines[linenum].strip().split()[-1]
		elif lines[linenum].strip().split()[0] == "KeyFile":
			KeyFile = lines[linenum].strip().split()[-1]
		elif lines[linenum].strip().split()[0] == "DataFile":
			DataFile = lines[linenum].strip().split()[-1]

	f.close()



def ImportKey(curpath,keyfilename):
	cmd = "sudo gpg --import %s/%s" % (curpath,keyfilename)
	sub = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
	sub.wait()
	res = sub.stderr.readlines() 
	if "not changed" in res[0] and PRINT == "yes":
		print "key already imported!"
	elif "imported" in res[0] and PRINT == "yes":
		print "key import successful"
			
	match = re.search(r"key\s([0-9A-Z]*)",res[0])
	if match != None:
		keyID = match.group(1)
		if PRINT == "yes":
			print keyID
		return keyID



def PromoteTrustkey(keyID):
	child = pexpect.spawn("sudo gpg --edit-key %s" % keyID)
	except_list = ["Command> ","Your decision\? ","\(y/N\) "]

	index = child.expect(except_list)
	if index == 0:
		child.sendline("trust")	
	index = child.expect(except_list)
	if index == 1:
		child.sendline("5")
	index = child.expect(except_list)
	if index == 2:
		child.sendline("y")
	index = child.expect(except_list)
	if index == 0:
		child.sendline("quit")



def CheckFile(sigfilename,datafilename):
	cmd = "sudo gpg --verify %s %s" % (sigfilename,datafilename)
	sub = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
	sub.wait()
	res = sub.stderr.readlines()
	if "Good signature" in res[-1]:
		return 1
	else:
		return 0
	pprint.pprint(res)



def Move2Server(curpath,keyfilename):
	ServerPath = "dummy"

	
	cmd = "mv %s/"

def GenerateKey()
	


if __name__ == "__main__":
	init()
	print CUR_PATH
	print ServerPath
	print SigFile
	print KeyFile
	print DataFile

#	KEYID = ImportKey(CUR_PATH, "PGPVarifyPublicKey") 	
#	PromoteTrustkey(KEYID)
#	Move2Server(CUR_PATH, "Configuration.in")
#	CheckFile(SigFile, DataFile)



