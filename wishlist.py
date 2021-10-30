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

def createWishList(request,session):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	username = escape(str(request.form.get('username')).strip())
    	codigo = escape(str(request.form.get('codigo')).strip())    	
    	queries = """INSERT INTO wishList (username,codigo) 
					VALUES (?,?);"""
    	data_params = (username,codigo)
    	with DBManager() as db:
    		try:
    			result = db.execute(queries, data_params)	
    			return str("ok")
    		except sqlite3.OperationalError as msg:
    			return str(msg)

def listWishList(request,session):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "SELECT * FROM wishList INNER JOIN producto ON producto.codigo = wishList.codigo WHERE wishList.username = ?;"    	
    	data_params = (_userID_,)
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					data = db.fetchall()						
    					return render_template("listWishList.html", pageName="Lista de Deseos", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, data=data)
    				except sqlite3.OperationalError as msg:
    					return render_template("listWishList.html", pageName="Lista de Deseos", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))

def deleteWishList(request,session,codigoProducto,username):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "DELETE FROM wishList WHERE codigo = ? AND username = ?;"
    	data_params = (int(codigoProducto),str(username))
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					return str("ok")
    				except sqlite3.OperationalError as msg:
    					return str("fail")