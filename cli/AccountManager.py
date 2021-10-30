import hashlib
import os
import binascii

import sys

# USAGE: python AccountManager.py --p MiContraseña1234

flag = str((sys.argv[1])).lower()

if (len(sys.argv) > 1):
	if (flag == "--p"):

		print("Contraseña Ingresada %s" % (sys.argv[2]))
		print()

		size = os.urandom(32)
		salt = binascii.b2a_hex(size).decode('utf-8')

		passwd = str((sys.argv[2]))
		passwd = passwd.encode('utf-8')
		key = hashlib.pbkdf2_hmac('sha256', passwd, salt.encode(), 100000)

		print("SALT: %s" % str(salt))
		print("Password SHA256: %s" % str(binascii.b2a_hex(key),'utf-8'))	
	else:
		print("Opcion invalida.")