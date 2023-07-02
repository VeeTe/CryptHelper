import os
import random
import time
import datetime
from cryptography.fernet import Fernet
import hashlib
import string
import shutil

def readFile(strFilepath: str, strReadMethod: str="r") -> (bool,str):
	try:
		with open(strFilepath, strReadMethod) as file:
			objReturn = file.read()
		return True, objReturn
	except Exception as ex:
		print(f"readFile: {ex}")
		return False, str(ex)

def writeToFile(strFilepath: str, strWriteContent: str, strWriteMethod: str="w") -> (bool, str):
	try:
		with open(strFilepath, strWriteMethod) as file: 
			file.write(strWriteContent)
		return True, ""
	except Exception as ex:
		return False, ex

def getTimeNow(strTimeFormat: str="legible") -> (datetime, str):
	dtNow = datetime.datetime.now()
	strTimeFormat=strTimeFormat.lower()
	if strTimeFormat == "legible": strFormatting = '%Y-%m-%d %H:%M:%S.%f %Z'
	elif strTimeFormat == "mushed": strFormatting = '%Y%m%d%H%M%S%f%Z'
	else: strFormatting == "%Y%m%d_%H%M%S%f_%Z"
	strNow = dtNow.strftime(strFormatting)
	return dtNow, strNow


def writeLog(strLogMessage: str="", strFilepath: str="Log.txt") -> bool:
	if strLogMessage == "": return False, "ERROR: writeLog, no log message provided."
	dtNow,strNow = getTimeNow()
	strWriteContent = f"[[{strNow}]]: {strLogMessage}\n"
	bolWriteFile, strPotentialError = writeToFile(strFilepath, strWriteContent, "a")
	return bolWriteFile, strPotentialError


def ifLog(strLogMessage, bolLoggingConditional, strFilepath: str="Log.txt") -> (bool, str):
	if bolLoggingConditional: writeLog(strLogMessage, strFilepath) 

def getHashOfFile(objPassed):
	try:
		objHasher = hashlib.md5()
		with open(objPassed, 'rb') as f:
			objBuf = f.read()
			objHasher.update(objBuf)
		return True, objHasher.hexdigest()
	except Exception as ex:
		print(f"getHashOfFile: {ex}")
		return False, str(ex)

def overwriteFile(strFilepath, intPasses: int=3, bolCheckOverwrite = True) -> (bool,str):
	try: 
		if not os.path.isfile(strFilepath):
			return False, "File does not exist."
		file_size = os.path.getsize(strFilepath)
		for intCounter1 in range(intPasses):
			random_data = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(file_size))
			if bolCheckOverwrite:# Open the file in binary mode to read its content
				with open(strFilepath, 'rb') as file:
					original_data = file.read()
			with open(strFilepath, 'wb') as file:
				#original_data = file.read()
				file.write(random_data.encode())

			if bolCheckOverwrite: 
				if random_data.encode() != random_data.encode():
					strMessage = "File overwrite failed. Verify the necessary permissions."
					print(strMessage_temp)
					return False, strMessage_temp
			original_data = None
			random_data = None
			return True, ""
	except Exception as ex:
		print(f"overwriteFile: {ex}")
		return False, str(ex)
	

def secureDelete(strFilepath,  intPasses: int=3, bolCheckOverwrite = True) -> (bool,str):
	try:
		bolSuccess, strPotentialError = overwriteFile(strFilepath, intPasses, bolCheckOverwrite)
		if  bolSuccess == True:  os.remove(strFilepath)
		else: return False, strPotentialError
		return True, ""
	except Exception as ex:
		print("secureDelete: {ex}")
		return False, str(ex)
def copyFile(source_path, destination_path) -> (bool,str):
    try:
        shutil.copy(source_path, destination_path)
        return True, ""
    except Exception as ex:
    	return False, ex

def renameFile(strOldFilename, strNewFilename) -> (bool,str):
    try:
        os.rename(strOldFilename, strNewFilename)
        return True, ""
    except Exception as ex:
    	return False, ex

def writeKey(strKeyFilepath: str="Key.txt") -> (bool,str):
	try:
		objKey = Fernet.generate_key()
		bolSuccess, strPotentialError = writeToFile(strKeyFilepath, objKey, "wb")
		return bolSuccess, strPotentialError 
	except Exception as ex:
		return False, ex


def loadKey(strKeyFilepath: str="Key.txt") -> bytes:
	return open(strKeyFilepath, "rb").read()

def generateKeyChain(strKeyFilepath: str="KeyChain.txt", intNumberOfKeys: int=10)->(bool,str):
	strKeys = ""
	try:
		for intCounter1 in range(intNumberOfKeys):
			objKey = Fernet.generate_key()
			strKeys += str(objKey.decode()) + "\n"
		if len(strKeys) > 0: strKeys = strKeys[:-1]
		writeToFile(strKeyFilepath, strKeys, "w")
		return True, ""
	except Exception as ex: 
		return False, ex

class cryptor: 
	def __init__(self, key, loggingconditional: bool = "False", logfilepath: str="Log.txt") -> (bool,str):
		self.objKey = Fernet(key)
		self.bolLoggingConditional = loggingconditional
		self.strLogFilepath = logfilepath
		self.strClassName = self.__class__.__name__

	def ifLog(self,strLogMessage):
		ifLog(strLogMessage,self.bolLoggingConditional,self.strLogFilepath)

	def encryptFile(self, strInFilepath: str, strOutFilepath: str="") -> (bool,str):
		strLogHandle = f"{self.strClassName}.encryptFile;"
		if strOutFilepath == "": 
			self.ifLog(f"{strLogHandle} strOutFilepath empty, defaulting to strInFilepath ({strInFilepath}) as strOutFilepath")
			strOutFilepath = strInFilepath
		try:
			self.ifLog(f"{strLogHandle} starting")
			bolSuccess, byteFile = readFile(strInFilepath, "rb")
			self.ifLog(f"{strLogHandle} reading the file to encrypt: {strInFilepath}")
			if bolSuccess != True: 
				self.ifLog(f"{strLogHandle} error encountered reading the file: {byteFile}. Due to: {byteFile}")
				return False, byteFile
			byteEncryptedData = self.objKey.encrypt(byteFile)
			self.ifLog(f"{strLogHandle} bytes encrypted, pending write")
			bolWrite = writeToFile(strOutFilepath, byteEncryptedData, "wb")
			self.ifLog(f"{strLogHandle} bolWrite:{bolWrite}, encrypted file: {strOutFilepath}")
			return True, ""
		except Exception as ex: 
			self.ifLog(f"{strLogHandle} error encountered: {ex}")
			return False, ex


	def decryptFile(self, strInFilepath: str, strOutFilepath: str="") -> (bool,str):
		strLogHandle = f"{self.strClassName}.decryptFile;"
		if strOutFilepath == "": 
			self.ifLog(f"{strLogHandle} strOutFilepath empty, defaulting to strInFilepath ({strInFilepath}) as strOutFilepath")
			strOutFilepath = strInFilepath
		try:
			self.ifLog(f"{strLogHandle} starting")
			bolSuccess, byteEncryptedData = readFile(strInFilepath, "rb")
			self.ifLog(f"{strLogHandle} reading loaded file to decrypt: {strInFilepath}")
			if bolSuccess != True: 
				self.ifLog(f"{strLogHandle} failed to load file to decrypt: {strInFilepath}. Due to: {byteFile}")
				return True, byteFile
			byteDecryptedData = self.objKey.decrypt(byteEncryptedData)
			self.ifLog(f"{strLogHandle} bytes decrypted, pending write")
			bolWrite = writeToFile(strOutFilepath,byteDecryptedData, "wb")
			self.ifLog(f"{strLogHandle} bolWrite:{bolWrite}, decrypted file: {strOutFilepath}")
			return True, ""
		except Exception as ex:
			self.ifLog(f"{strLogHandle} error encountered: {ex}")
			return False, ex
	
	def secureDelete(self, strFilepath, intPasses: int=3, bolCheckOverwrite = True) -> (bool,str):
		strLogHandle = f"{self.strClassName}.decryptFile;"
		bolSuccess, strPotentialError = secureDelete(strFilepath, intPasses, bolCheckOverwrite)
		if bolSuccess: strTemp = "successfully removed"
		else: 
			strTemp = f"failed to be removed due to {strPotentialError}"
			print(f"ERROR: {strFilepath}, failed to delete securely, due to: {strPotentialError}")
		self.ifLog(f"{strLogHandle} {strFilepath} {strTemp}")
		return bolSuccess, strPotentialError

	def encryptAndVerify(self, strInFilepath: str, strOutFilepath: str="", 
						intMaxTries: int=5, intPasses: int=3, bolCheckOverwrite = True) -> (bool,str):
		strLogHandle = f"{self.strClassName}.decryptFile;"
		if strOutFilepath == "": 
			self.ifLog(f"{strLogHandle} strOutFilepath empty, defaulting to strInFilepath ({strInFilepath}) as strOutFilepath")
			strOutFilepath = strInFilepath
		strValidFileHash = getHashOfFile(strInFilepath)
		self.ifLog(f"{strLogHandle} the hash of the original file ({strInFilepath}) is {strValidFileHash}")
		strLastFileHash = ""
		self.ifLog(f"{strLogHandle} starting loop attempting to continue re-encrypting until the file hash matches")
		strEncrypted_temp = strInFilepath+"_e"
		strUnencrypted_temp = strInFilepath+"_u"

		#Verify hash, if reaches limit or hashes match, delete the test file (on which we test decryption)
		while (strLastFileHash != strValidFileHash and intMaxTries != 0):
			self.ifLog(f"{strLogHandle} attempt #{intMaxTries} starts")
			self.encryptFile(strInFilepath, strEncrypted_temp)
			self.ifLog(f"{strLogHandle} {strEncrypted_temp} file generated")
			self.decryptFile(strEncrypted_temp, strUnencrypted_temp)
			self.ifLog(f"{strLogHandle} {strUnencrypted_temp} file generated")
			strLastFileHash = getHashOfFile(strUnencrypted_temp)
			self.ifLog(f"{strLogHandle} {strUnencrypted_temp} file hash is: {strLastFileHash}")
			intMaxTries -= 1
		self.ifLog(f"{strLogHandle} intMaxTries={intMaxTries}, strUnencrypted_temp hash {strLastFileHash} =?= valid file hash {strValidFileHash}")
		self.secureDelete(strUnencrypted_temp, intPasses, bolCheckOverwrite)
		if strLastFileHash == strValidFileHash: 
			self.ifLog(f"{strLogHandle} hashes matched")
			if strInFilepath == strOutFilepath:
				self.ifLog(f"{strLogHandle} due to strInFilepath == strOutFilepath, strInFilepath has to be first securely deleted") 
				self.secureDelete(strInFilepath, intPasses, bolCheckOverwrite)
			
			bolSuccess, strPotentialError = renameFile(strEncrypted_temp, strOutFilepath)
			if bolSuccess: objReturn = True, ""
			else: 
				objReturn = False, strPotentialError 
		else:
			objReturn = False, "Failed to encrypt, try again."
		bolSuccess, strPotentialError = objReturn
		if bolSuccess: self.ifLog(f"{strLogHandle} Renaming of file was successful")
		else: self.ifLog(f"{strLogHandle} Renaming of file has failed: {strPotentialError}")
		return objReturn

'''
Gets the file with all of the keys & split it by line into a list
'''
def readKeyChain(strKeysFilepath: str="KeyChain.txt") -> (bool,str):
	try:
		bolSuccess, strKeyChain = readFile(strKeysFilepath)
		arrKeyChain = strKeyChain.split()
		return True, arrKeyChain
	except Exception as ex:
		return False, ex

'''
Encrypts files multiple times, safely overwriting the previous copy
'''
def chainCryptor(strFunction: str, #encrypt or decrypt
				strInFilepath: str, strOutFilepath: str, 
				strKeysFilepath: str="KeyChain.txt", 
				intMaxTries: int=5, intPasses: int=3, bolCheckOverwrite = True, 
				bolLoggingConditional: bool=False, strLogFilepath: str="Log.txt") -> (bool,str):
	bolSuccess, arrKeyChain = readKeyChain(strKeysFilepath)
	if bolSuccess == False: return False, arrKeyChain
	if len(arrKeyChain) < 1: return False, "KeyChain contains less than 1 key"
	if strFunction.lower() == "decrypt": bolDecrypt = True
	elif strFunction.lower() == "encrypt": bolDecrypt = False
	else: return False, f"strFunction invalid ({strFunction}), only accepted values are encrypt or decrypt"
	if bolDecrypt: arrKeyChain = arrKeyChain[::-1]
	strEncrypted_temp = strInFilepath
	arrTempFiles = []
	for intCounterKey in range(len(arrKeyChain)):
		bytesKey = bytes(arrKeyChain[intCounterKey], 'utf-8')
		objCryptor = cryptor(bytesKey, bolLoggingConditional, strLogFilepath)
		strEncrypted_temp1 = strInFilepath + "_" + str(intCounterKey)
		if bolDecrypt: bolSuccess, strPotentialError = objCryptor.decryptFile(strEncrypted_temp, strEncrypted_temp1)
		else: bolSuccess, strPotentialError = objCryptor.encryptAndVerify(strEncrypted_temp, strEncrypted_temp1, intMaxTries, intPasses, bolCheckOverwrite)
		arrTempFiles.append(strEncrypted_temp1)
		strEncrypted_temp = strEncrypted_temp1
		if bolSuccess == False: return False, strPotentialError
	bolSuccess, strPotentialError = renameFile(strEncrypted_temp, strOutFilepath)
	if len(arrTempFiles) > 0:  arrTempFiles=arrTempFiles[:-1]
	if bolSuccess: objReturn = True, ""
	else:
		bjReturn = False, strPotentialError 
	for strTempFile in arrTempFiles: secureDelete(strTempFile, intPasses, bolCheckOverwrite)
	return True, ""
