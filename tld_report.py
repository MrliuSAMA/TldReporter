import pprint
import re
import subprocess
import sys
import os

CUR_PATH = "dummy"
ServerPath = "dummy"
DataFile = "dummy"
KeyFinger = "dummy"



def init():
	#get cur file dir
	global CUR_PATH
	path = sys.path[0]
	if os.path.isdir(path) == True:
		CUR_PATH = path
	elif os.path.isfile(path):
		CUR_PATH = os.path.dirname(path)

	global ServerPath
	global DataFile
	global KeyFinger

	f = open("%s/%s" % (CUR_PATH,"Configuration.in"))
	lines = f.readlines()
	for linenum in range(len(lines)):
		if lines[linenum].strip().split()[0] == "ServerPath":
			ServerPath = lines[linenum].strip().split()[-1]
		elif lines[linenum].strip().split()[0] == "DataFile":
			DataFile = lines[linenum].strip().split()[-1]
		elif lines[linenum].strip().split()[0] == "KeyFinger":
			KeyFinger = lines[linenum].strip().split()[-1]		
	f.close()


	return None


def KeyGenerate(curpath):
	if GetKeyID() != None:
		print "default key already exist!"
		return

	cmd = "gpg --batch --gen-key %s/%s" % (curpath,"DefaultKeyGE")
	sub = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
	sub.wait()
	res = sub.stderr.readlines()
	print res


	return None


def GetKeyID(keyuser = "default"):
	cmd = "gpg --locate-keys %s" % keyuser
	sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	sub.wait()
	res = sub.stdout.read()
	match = re.search(r"pub\s*[0-9A-Z]*/([0-9A-z]*)",res)
	if match!= None: 
		KeyID = match.group(1)
		return KeyID
	else:
		KeyID = None
		return KeyID

	
		


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

	
	return None



def SignFile(KeyID,inputfile):
	templist = inputfile.split("/")
	templist[-1] = templist[-1]+".sig"
	outputfile = "/".join(templist)

	cmd = "gpg --detach-sign --default-key %s --output %s %s" % (KeyID,outputfile,inputfile)
	sub = subprocess.Popen(cmd, shell=True)
	sub.wait()


	return None
	


def ExportPubKey(KeyID):
	cmd = "gpg --export -armor --output key.pub %s" % KeyID
	sub = subprocess.Popen(cmd, shell=True)
	sub.wait()


	return None
	


def MoveFile(curpath,datafile,serverpath):
	templist = datafile.strip().split('/')
	datadir = '/'.join(templist[:-1])

	cmd = "cp -f %s %s" % (datafile, serverpath)	
	sub = subprocess.Popen(cmd, shell=True)
	sub.wait()	

	cmd = "mv -f %s/*.sig %s/key.pub %s" % (datadir,curpath, serverpath)
	sub = subprocess.Popen(cmd, shell=True)
	sub.wait()
	

	return None


if __name__ == "__main__":
	init()

	keyID = "dummy"	
	if KeyFinger == "dummy":
		KeyGenerate(CUR_PATH)
		keyID = GetKeyID()
	else:	
		keyID = KeyFinger
	
	SignFile(keyID, DataFile)	
	ExportPubKey(keyID)
	MoveFile(CUR_PATH, DataFile, ServerPath)



