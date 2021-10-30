import hashlib
import os
import binascii
import random
import time

import sqlite3
from sqlite3.dbapi2 import Error

def createSession(session, user):
    session['username'] = str(user)
	  
def destroySession(session):
	session.pop('username', None)
	session.pop('rolID', None)

def Loggedin(session):
	if 'username' in session:
	    return True
	else: 
	    return False

def userIDSession(session):
    if 'username' in session:
    	return str(session['username'])
    else: 
	    return ""

def rolIDSession(session):
    # Not logged = 0
    # usuario = 1
	# administrador = 2
	# SuperAdministrador = 3
    if 'rolID' in session:
    	return int(session['rolID'])
    else: 
	    return int(0)

def convertToPesosCOP(value):
	ceros = ""
	for x in range(3, 10, 1):
		if ((x+1)==len(str(value))):
			price = "$ "+'{price:,.0f}'.format(price=int(value)).replace(',','.')
			return str(price)

def blobImageUpload(request, param):
    if (str(param) in request.files):
    		f = request.files[str(param)]
    		byteFileImg = f.read(1)
    		hex_byteImg = ""
    		while byteFileImg:
    				byte_array = bytearray(byteFileImg)
    				hex_byteImg = hex_byteImg + str(byte_array.hex())
    				byteFileImg = f.read(1)
    		bytesArrays = bytes.fromhex(hex_byteImg)
    return (sqlite3.Binary(bytesArrays))

def file2Bytes(f):
    byteFileImg = f.read(1)
    hex_byteImg = ""
    while byteFileImg:
    		byte_array = bytearray(byteFileImg)
    		hex_byteImg = hex_byteImg + str(byte_array.hex())
    		byteFileImg = f.read(1)
    return hex_byteImg

def generateSaltPasswd():
	size = os.urandom(32) # 32 bits
	salt = binascii.b2a_hex(size).decode('utf-8')
	return str(salt)

def passwordSalt(passwd, salt):
	password = passwd.encode('utf-8')
	key = hashlib.pbkdf2_hmac('sha256', password, salt.encode(), 100000)
	return str(binascii.b2a_hex(key),'utf-8')

def TokenCSRF():
    random.seed(time.time_ns())
    rand = random.random()
    CSRF = hashlib.md5()
    b = bytes(str(rand), 'utf-8')
    CSRF.update(b)
    return str(CSRF.hexdigest())

def checkTokenCSRF(token, tokenClient):
    if str(token) == str(tokenClient):
    	return True
    else:
    	return False