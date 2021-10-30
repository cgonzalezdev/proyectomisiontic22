from flask import Flask, render_template, url_for, redirect, request, session

from DBManager import DBManager
import sqlite3
from sqlite3.dbapi2 import Error
import base64

import hashlib
import os
import binascii
import random
import time

import utilsMethod
import usuario	
import producto

from markupsafe import escape

import config 

def nonAccess(request, session):
    _Loggedin_ = utilsMethod.Loggedin(session)
    _userID_ = utilsMethod.userIDSession(session)
    _rolID_ = utilsMethod.rolIDSession(session)
    _photo_ = usuario.get_imageProfile(session)	
    return render_template("nonAccess.html", pageName="Sin Acceso", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_)

def ingreso(request, session):
	_Loggedin_ = utilsMethod.Loggedin(session)
	_userID_ = utilsMethod.userIDSession(session)
	_rolID_ = utilsMethod.rolIDSession(session)
	_photo_ = usuario.get_imageProfile(session)	
	utilsMethod.TokenCSRF()
	username = ''
	password = ''	
	if utilsMethod.Loggedin(session):	
		imageProfile = get_imageProfile(session)	
		return producto.listProducts(request, session)
	if request.method == 'GET':		
		CSRF = utilsMethod.TokenCSRF()
		session['TokenCSRF'] = CSRF
		return render_template("login.html", pageName="Login", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, TokenCSRF = CSRF)	
	if request.method == 'POST': 
		token = request.form.get('token') 
		username = escape(str(request.form.get('username')).strip())
		password = escape(str(request.form.get('password')).strip())
		if utilsMethod.checkTokenCSRF(session['TokenCSRF'], token):			
			if usuario.checkLogin(username,password):
				utilsMethod.createSession(session, username)
				session['rolID'] = 1
				imageProfile = get_imageProfile(session)
				return producto.listProducts(request, session)
			else:
				m = "Usuario o Contraseña incorrecto."
				CSRF = utilsMethod.TokenCSRF()
				session['TokenCSRF'] = CSRF
				return render_template('login.html', Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error = m, TokenCSRF = CSRF)
		else:
			m = "Token CSRF Errado."
			CSRF = utilsMethod.TokenCSRF()
			session['TokenCSRF'] = CSRF
			return render_template('login.html', Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error = m, TokenCSRF = CSRF)

def ingresoAdmin(request, session):
	_Loggedin_ = utilsMethod.Loggedin(session)
	_userID_ = utilsMethod.userIDSession(session)
	_rolID_ = utilsMethod.rolIDSession(session)
	_photo_ = usuario.get_imageProfile(session)	
	utilsMethod.TokenCSRF()
	username = ''
	password = ''	
	if utilsMethod.Loggedin(session):		
		return producto.listProducts(request, session)
	if request.method == 'GET':		
		CSRF = utilsMethod.TokenCSRF()
		session['TokenCSRF'] = CSRF
		return render_template('panelAdmin.html', pageName="Acceso Admin.", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, TokenCSRF = CSRF)	
	if request.method == 'POST': 
		token = request.form.get('token') 
		username = escape(str(request.form.get('username')).strip())
		password = escape(str(request.form.get('password')).strip())
		if utilsMethod.checkTokenCSRF(session['TokenCSRF'], token):			
			if usuario.checkLoginAdmin(username,password,session):
				utilsMethod.createSession(session, username)				
				return producto.listProducts(request, session)
			else:
				m = "Usuario o Contraseña incorrecto."
				CSRF = utilsMethod.TokenCSRF()
				session['TokenCSRF'] = CSRF
				return render_template('panelAdmin.html', pageName="Acceso Admin.", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error = m, TokenCSRF = CSRF)
		else:
			m = "Token CSRF Errado."
			CSRF = utilsMethod.TokenCSRF()
			session['TokenCSRF'] = CSRF
			return render_template('panelAdmin.html', pageName="Acceso Admin.", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error = m, TokenCSRF = CSRF)

def logout(request,session):
    utilsMethod.destroySession(session)	
    CSRF = utilsMethod.TokenCSRF()
    session['TokenCSRF'] = CSRF
    _Loggedin_ = utilsMethod.Loggedin(session)
    return render_template("login.html", Loggedin=_Loggedin_, TokenCSRF = CSRF)

def existUserAdmin(user,session):
    	q_admin = "SELECT username,password,salt FROM administrador WHERE username = ?;"
    	d_param_admin = (str(user),)
    	q_superadmin = "SELECT username,password,salt FROM superAdministrador WHERE username = ?;"
    	d_param_superadmin = (str(user),)
    	with DBManager() as db:
    		r_admin = db.execute(q_admin, d_param_admin)
    		data_admin = db.fetchall()
    		r_superadmin = db.execute(q_superadmin, d_param_superadmin)
    		data_superadmin = db.fetchall()   
    		if (len(data_admin) > 0):
    			session['rolID'] = 2
    			return data_admin
    		if (len(data_superadmin) > 0):
    			session['rolID'] = 3
    			return data_superadmin		

def checkLoginAdmin(user, passwd, session):
		checkUserName = existUserAdmin(user,session)
		salt = ""
		for row in checkUserName:
			salt = row[2]
			print(salt)
		if session['rolID'] == 2: tableAdmin = "administrador"
		if session['rolID'] == 3: tableAdmin = "superAdministrador"
		if (len(checkUserName) > 0):
			queries = "SELECT username,password FROM " +str(tableAdmin)+ " WHERE username = ? AND password = ?;"		
			passwd = utilsMethod.passwordSalt(passwd, salt)
			print(passwd)
			print(tableAdmin)
			data_params = (str(user),str(passwd))
			with DBManager() as db:
				result = db.execute(queries, data_params)
				if db.fetchall():
					return True			
				else:
					return False

def existUser(user):
    	queries = "SELECT username,password,salt FROM usuarios WHERE username = ?;"
    	data_params = (str(user),)
    	with DBManager() as db:
    		result = db.execute(queries, data_params)
    		data = db.fetchall()
    		return data

def checkLogin(user, passwd):
		checkUserName = existUser(user)
		salt = ""
		for row in checkUserName:
			salt = row[2]
		if (len(checkUserName) > 0):
			queries = "SELECT username,password FROM usuarios WHERE username = ? AND password = ?;"		
			passwd = utilsMethod.passwordSalt(passwd, salt)
			data_params = (str(user),str(passwd))
			with DBManager() as db:
				result = db.execute(queries, data_params)
				if db.fetchall():
					return True			
				else:
					return False

def registro(request,session):
	_Loggedin_ = utilsMethod.Loggedin(session)	
	if request.method == 'GET':
      		return render_template('registro.html', Loggedin=_Loggedin_)
	if request.method == 'POST':    		
		username = escape(str(request.form.get('username')).strip())
		if (len(existUser(username)) > 0): return render_template("registro.html", Loggedin=_Loggedin_, error = "El usuario ya existe!")
		password = escape(str(request.form.get('password')).strip())
		salt = utilsMethod.generateSaltPasswd()
		password = utilsMethod.passwordSalt(password, salt)
		nombres = escape(str(request.form.get('nombres')).strip())
		apellidos = escape(str(request.form.get('apellidos')).strip())
		tipoDoc = escape(str(request.form.get('tipoDoc')).strip())
		documento = escape(str(request.form.get('numDoc')).strip())
		telefono = escape(str(request.form.get('telefono')).strip())
		email = escape(str(request.form.get('email')).strip())   
		direccion = escape(str(request.form.get('direccion')).strip()) 		
		if nombres is None: nombres = ""
		if apellidos is None: apellidos = ""
		if tipoDoc is None: tipoDoc = ""
		if documento is None: documento = None
		if telefono is None: telefono = None
		if direccion is None: direccion = ""
		file = request.files['imgUpload']
		if file: mimetype = file.content_type
		else: mimetype = ""
		urlImage = base64.b64encode(utilsMethod.blobImageUpload(request,'imgUpload'))
		getimgBase64Hex = urlImage
		ImgDataURI = "data:%s;base64,%s" % (mimetype, getimgBase64Hex.decode("utf-8"))
		queries = """INSERT INTO usuarios (username,password,salt,nombres,apellidos,tipoDoc,documento,telefono,email,direccion,imagen,tipoImagen) 
				VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""
		data_params = (username,password,salt,nombres,apellidos,tipoDoc,documento,telefono,email,direccion,ImgDataURI,mimetype)		
		if len(username)!=0 and len(password)!=0:
			with DBManager() as db:
				try:
					result = db.execute(queries, data_params)	
					return render_template('registro.html', Loggedin=_Loggedin_, success="Registro Exitoso.")	
				except sqlite3.OperationalError as msg:
					return render_template('registro.html', Loggedin=_Loggedin_, error=str(msg))
		else:
    			return render_template('registro.html', Loggedin=_Loggedin_, error="Error durante el registro del usuario.")

def changePassword(request,session):
    _Loggedin_ = utilsMethod.Loggedin(session)
    _userID_ = utilsMethod.userIDSession(session)
    _rolID_ = utilsMethod.rolIDSession(session)
    _photo_ = usuario.get_imageProfile(session)
    if request.method == 'GET':        
        return render_template("cambiarPassword.html", pageName="Cambiar Contraseña", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_)
    if request.method == 'POST':
    	passwdCurrent = escape(str(request.form.get('passwdCurrent')).strip())
    	password = escape(str(request.form.get('password')).strip())
    	retypePasswd = escape(str(request.form.get('retypePasswd')).strip())
    	checkUserName = usuario.existUser(_userID_)
    	salt = ""
    	for row in checkUserName:
    		salt = row[2]
    	if (len(checkUserName) > 0):
    		queries = "SELECT username,password FROM usuarios WHERE username = ? AND password = ?;"		
    		passwd = utilsMethod.passwordSalt(passwdCurrent, salt)
    		data_params = (str(_userID_),str(passwd))
    		with DBManager() as db:
    			result = db.execute(queries, data_params)
    			data = db.fetchall()
    			if len(data):
    				newSalt = utilsMethod.generateSaltPasswd()	
    				newPasswd = utilsMethod.passwordSalt(password, newSalt)
    				sql_update_query = "UPDATE usuarios SET password=?, salt=? WHERE username=?;"	
    				sql_data_params = (newPasswd,newSalt,_userID_)
    				with DBManager() as db:	
    					db.execute(sql_update_query, sql_data_params)    					
    					db.commit()
    				return render_template("cambiarPassword.html", pageName="Cambiar Contraseña", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, success="La contraseña ha sido cambiada con exito.")
    			if len(data) <= 0:
    				return render_template("cambiarPassword.html", pageName="Cambiar Contraseña", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error="Su actual contraseña no es correcta.")

def get_myProfile(request,session):
    _Loggedin_ = utilsMethod.Loggedin(session)
    _userID_ = utilsMethod.userIDSession(session)
    _rolID_ = utilsMethod.rolIDSession(session)
    _photo_ = usuario.get_imageProfile(session)
    if request.method == 'GET':  
    	if utilsMethod.Loggedin(session) == True: 
    		elems = []
    		queries = "SELECT username,nombres,apellidos,tipoDoc,documento,telefono,email,direccion,imagen,tipoImagen FROM usuarios WHERE username = ?;"
    		data_params = (_userID_,)
    		with DBManager() as db:
    			try:
    				result = db.execute(queries, data_params)
    				data = db.fetchall()
    				for row in data:
    					username = row[0]
    					nombres = row[1]
    					apellidos = row[2]
    					tipoDoc = row[3]
    					documento = row[4]
    					telefono = row[5]
    					email = row[6]
    					direccion = row[7]
    					imagen = row[8]
    					elemento = [username,nombres,apellidos,tipoDoc,documento,telefono,email,direccion,str(imagen)]
    					elems.append( elemento )
    			except sqlite3.OperationalError as msg:
        			return str(msg)	
    		return render_template("perfil.html", pageName="Mi Perfil", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, elems=elems)	
    if request.method == 'POST':  
    	email = escape(str(request.form.get('email')).strip())
    	nombres = escape(str(request.form.get('nombres')).strip())
    	apellidos = escape(str(request.form.get('apellidos')).strip())
    	tipoDoc = escape(str(request.form.get('tipoDoc')).strip())
    	documento = escape(str(request.form.get('numDoc')).strip())
    	telefono = escape(str(request.form.get('telefono')).strip())    	 
    	direccion = escape(str(request.form.get('direccion')).strip()) 		
    	if nombres is None: nombres = ""
    	if apellidos is None: apellidos = ""
    	if tipoDoc is None: tipoDoc = ""
    	if documento is None: documento = None
    	if telefono is None: telefono = None
    	if direccion is None: direccion = ""
    	file = request.files['imgUpload']
    	if file: 
    			mimetype = file.content_type
    			isImgUpload = True
    	else: 
    			mimetype = ""
    			isImgUpload = False
    	if (isImgUpload):
    		urlImage = base64.b64encode(utilsMethod.blobImageUpload(request,'imgUpload'))
    		getimgBase64Hex = urlImage
    		ImgDataURI = "data:%s;base64,%s" % (mimetype, getimgBase64Hex.decode("utf-8"))
    		queries = "UPDATE usuarios SET nombres=?,apellidos=?,tipoDoc=?,documento=?,telefono=?,email=?,direccion=?,imagen=?,tipoImagen=? WHERE username=?;"
    		data_params = (nombres,apellidos,tipoDoc,documento,telefono,email,direccion,ImgDataURI,mimetype,_userID_)	
    	else:
    		queries = "UPDATE usuarios SET nombres=?,apellidos=?,tipoDoc=?,documento=?,telefono=?,email=?,direccion=? WHERE username=?;"
    		data_params = (nombres,apellidos,tipoDoc,documento,telefono,email,direccion,_userID_)
    	if len(_userID_)!=0:
    		with DBManager() as db:
    			try:
    				db.execute(queries, data_params)
    				db.commit()	
    				return render_template('perfil.html', pageName="Mi Perfil", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, success="Se actualizó su información.")
    			except sqlite3.OperationalError as msg:
    				return render_template('perfil.html', pageName="Mi Perfil", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))
    	else:
    			return render_template('perfil.html', pageName="Mi Perfil", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error="Error durante la actualización del usuario.")

def list_AllUsers(request,session):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "SELECT * FROM usuarios;"
    	data_params = ()
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					data = db.fetchall()						
    					return render_template("listAllUsuarios.html", pageName="Listado Usuarios (Todos)", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, data=data)
    				except sqlite3.OperationalError as msg:
    					return render_template("listAllUsuarios.html", pageName="Listado Usuarios (Todos)", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))

def deleteUsuario(request,session,username):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "DELETE FROM usuarios WHERE username = ?;"
    	data_params = (str(username),)
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					return str("ok")
    				except sqlite3.OperationalError as msg:
    					return str("fail")

def get_imageProfile(session):
    if 'username' in session:
    	_rolID_ = utilsMethod.rolIDSession(session)
    	if (_rolID_ == 1):
    		userID = str(session['username'])
    		queries = "SELECT * FROM usuarios WHERE username = ?;"
    		data_params = (userID,)
    		with DBManager() as db:	
    			result = db.execute(queries, data_params)
    			data = db.fetchone()		
    			getImgBytes = data[10] #Field DB: imagen
    			return getImgBytes
    	else:
    		return str("data:image/png;base64,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")
    else:
    	return str("")
		
