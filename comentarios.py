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

def get_Comentario(request,session,nombre,codigoProducto,precio):
    _Loggedin_ = utilsMethod.Loggedin(session)
    _userID_ = utilsMethod.userIDSession(session)
    _rolID_ = utilsMethod.rolIDSession(session)
    _photo_ = usuario.get_imageProfile(session)
    if request.method == 'GET':        
        return render_template("createComentario.html", pageName="Comentar un Producto", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, nombre=nombre, codigo=codigoProducto, precio=precio)

def create_Comentario(request,session):
    _Loggedin_ = utilsMethod.Loggedin(session)
    _userID_ = utilsMethod.userIDSession(session)
    _rolID_ = utilsMethod.rolIDSession(session)
    _photo_ = usuario.get_imageProfile(session)
    if request.method == 'POST':
    	codigo = escape(str(request.form.get('codigo')).strip()) 	
    	calificacion = escape(str(request.form.get('calificacion')).strip())		
    	comentario = escape(str(request.form.get('comentario')).strip())    	
    	queries = """INSERT INTO comentarios (username,codigo,calificacion,comentario) 
					VALUES (?,?,?,?);"""
    	userID = utilsMethod.userIDSession(session)
    	data_params = (userID,codigo,calificacion,comentario)
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)	
    					return render_template("msgComentario.html", pageName="Comentario Guardado", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, success="Comentario guardado para el producto #{id:d}.".format(id = int(codigo)))
    				except sqlite3.OperationalError as msg:
    					return render_template("msgComentario.html", pageName="Comentario Guardado", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))

def list_Comentarios(request,session,codigoProducto):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "SELECT * FROM comentarios INNER JOIN producto ON producto.codigo = comentarios.codigo WHERE comentarios.codigo = ?;"
    	data_params = (codigoProducto,)
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					data = db.fetchall()						
    					return render_template("listComentario.html", pageName="Listado Comentarios", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, data=data)
    				except sqlite3.OperationalError as msg:
    					return render_template("listComentario.html", pageName="Listado Comentarios", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))

def list_User_Comentarios(request,session):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "SELECT * FROM comentarios INNER JOIN producto ON producto.codigo = comentarios.codigo WHERE comentarios.username = ?;"
    	data_params = (_userID_,)
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					data = db.fetchall()						
    					return render_template("listUserComentario.html", pageName="Mis Comentarios", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, data=data)
    				except sqlite3.OperationalError as msg:
    					return render_template("listUserComentario.html", pageName="Mis Comentarios", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))

def list_all_Comentarios(request,session):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "SELECT * FROM comentarios INNER JOIN producto ON producto.codigo = comentarios.codigo;"
    	data_params = ()
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					data = db.fetchall()						
    					return render_template("listAllComentario.html", pageName="Listado Comentarios (Todos)", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, data=data)
    				except sqlite3.OperationalError as msg:
    					return render_template("listAllComentario.html", pageName="Listado Comentarios (Todos)", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))

def delete_Comentario(request,session,codigoProducto,username):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "DELETE FROM comentarios WHERE codigo = ? AND username = ?;"
    	data_params = (int(codigoProducto),str(username))
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					return str("ok")
    				except sqlite3.OperationalError as msg:
    					return str("fail")