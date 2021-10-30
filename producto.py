from flask import Flask, render_template, url_for, redirect, request, session

import sqlite3
from sqlite3.dbapi2 import Error
from DBManager import DBManager

import usuario
import utilsMethod

import base64

from markupsafe import escape

def createProductos(request,session):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	if request.method == 'GET':
    		userID = utilsMethod.userIDSession(session)
    		return render_template("createProducto.html", pageName="Crear un Producto",Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_)
    	if request.method == 'POST':    			
    		codigo = escape(str(request.form.get('codigo')).strip())
    		nombre = escape(str(request.form.get('nombre')).strip())
    		descripcion = escape(str(request.form.get('descripcion')).strip())
    		precio = escape(str(request.form.get('precio')).strip())
    		cantidad = escape(str(request.form.get('cantidad')).strip())
    		file = request.files['imagen']
    		if file: mimetype = file.content_type
    		else: mimetype = ""
    		if descripcion is None: descripcion = ""
    		if ('imagen' in request.files): documento = None			
    		queries = """INSERT INTO producto (codigo,nombre,descripcion,precio,cantidad,imagen,tipoImagen) 
					VALUES (?,?,?,?,?,?,?);"""
    		urlImage = base64.b64encode(utilsMethod.blobImageUpload(request,'imagen'))
    		getimgBase64Hex = urlImage
    		ImgDataURI = "data:%s;base64,%s" % (mimetype, getimgBase64Hex.decode("utf-8"))		
    		data_params = (codigo,nombre,descripcion,precio,cantidad,ImgDataURI,mimetype)		
    		if len(codigo)!=0 and len(nombre)!=0 and len(precio)!=0 and len(cantidad)!=0:
    			with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)	
    					return render_template("createProducto.html", pageName="Crear un Producto", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, success="El producto #{id:d} fue creado exitosamente.".format(id = int(codigo)))
    				except sqlite3.OperationalError as msg:
    					return render_template("createProducto.html", pageName="Crear un Producto", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))
    		else:
    				return render_template("createProducto.html", pageName="Crear un Producto", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error="Usuario/Password no pueden estar vacio.")

def get_producto(request,session,codigoProducto):
    _Loggedin_ = utilsMethod.Loggedin(session)
    _userID_ = utilsMethod.userIDSession(session)
    _rolID_ = utilsMethod.rolIDSession(session)
    _photo_ = usuario.get_imageProfile(session)	
    queries = "SELECT codigo,nombre,descripcion,precio,cantidad,imagen,tipoImagen FROM producto WHERE codigo = ?;"
    data_params = (codigoProducto,)
    if len(str(codigoProducto))!=0:
        	with DBManager() as db:
        		try:
        			result = db.execute(queries, data_params)
        			data = db.fetchone()
        			if data == None:
        				return str("[]")
        			else:
        				codigo = int(data[0])
        				nombre = data[1]
        				nombre = nombre.replace("/", "-")
        				descripcion = data[2]
        				precio = utilsMethod.convertToPesosCOP((data[3]))
        				cantidad = int(data[4])
        				getImgBytes = data[5]
        				mimetype = data[6]
        				q = "SELECT COUNT(codigo) Cantidad, AVG(calificacion) Promedio FROM comentarios WHERE codigo = ?;"
        				d_Params = (codigoProducto,)
        				r = db.execute(q, d_Params)
        				estadistica = db.fetchone()
        				Cant = estadistica[0]
        				Prom = estadistica[1]
        				if Cant == 0 and Prom == None:        					
        					Cant = int(0)
        					Prom = int(0)
        				q_checkComet = "SELECT COUNT(codigo) conteo FROM comentarios WHERE username = ? AND codigo = ?;"
        				username = utilsMethod.userIDSession(session)
        				d_Params_checkComet = (username,codigoProducto)
        				r_checkComet = db.execute(q_checkComet, d_Params_checkComet)
        				checkComentario = db.fetchone()
        				if int(checkComentario[0]) == 0:
        					enableComentario = True
        				else:
        					enableComentario = False
        				q_checkWL = "SELECT COUNT(codigo) conteo FROM wishList WHERE username = ? AND codigo = ?;"
        				username = utilsMethod.userIDSession(session)
        				d_Params_checkWL = (username,codigoProducto)
        				r_checkWL = db.execute(q_checkWL, d_Params_checkWL)
        				checkWL = db.fetchone()
        				if int(checkWL[0]) == 0:
        					enableWL = True
        				else:
        					enableWL = False
        				return render_template("producto.html", pageName="Ver Producto",Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, enableComentario=enableComentario,enableWL=enableWL,codigo=codigo,nombre=nombre,descripcion=descripcion,precio=precio,cantidad=cantidad,imagen=str(getImgBytes), Cant=int(Cant), Prom=int(Prom))
        		except sqlite3.OperationalError as msg:
        			return str(msg)
    else:
        		return str("[]")

def get_list_all_productos(request,session):
	_Loggedin_ = utilsMethod.Loggedin(session)
	_userID_ = utilsMethod.userIDSession(session)
	_rolID_ = utilsMethod.rolIDSession(session)
	_photo_ = usuario.get_imageProfile(session) 	
	elems = []
	queries = "SELECT codigo,nombre,descripcion,precio,cantidad,imagen,tipoImagen FROM producto ORDER BY codigo;"
	data_params = ()
	with DBManager() as db:
			try:
				result = db.execute(queries, data_params)
				data = db.fetchall()
				for row in data:
					codigo = int(row[0])
					nombre = row[1]
					descripcion = row[2]
					precio = utilsMethod.convertToPesosCOP(row[3])
					cantidad = int(row[4])
					getImgBytes = row[5]
					mimetype = row[6]
					elemento = [codigo,nombre,descripcion,precio,cantidad,str(getImgBytes)]
					elems.append( elemento )
			except sqlite3.OperationalError as msg:
				return str(msg)	
	return render_template("productos.html", pageName="Inicio", searchProduct=True, Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, elems=elems)

def listProducts(request,session):
    return get_list_all_productos(request,session)

def editViewProducto(request,session,codigoProducto):
    _Loggedin_ = utilsMethod.Loggedin(session)
    _userID_ = utilsMethod.userIDSession(session)
    _rolID_ = utilsMethod.rolIDSession(session)
    _photo_ = usuario.get_imageProfile(session)
    if request.method == 'GET':
        if utilsMethod.Loggedin(session) == True: 
        	elems = []
        	queries = "SELECT codigo,nombre,descripcion,precio,cantidad,imagen,tipoImagen FROM producto WHERE codigo = ? ORDER BY codigo;"
        	data_params = (codigoProducto,)
        	with DBManager() as db:
        		try:
        			result = db.execute(queries, data_params)
        			data = db.fetchall()
        			for row in data:
        				codigo = int(row[0])
        				nombre = row[1]
        				descripcion = row[2]
        				precio = int(row[3])
        				cantidad = int(row[4])
        				getImgBytes = row[5]
        				mimetype = row[6]
        				elemento = [codigo,nombre,descripcion,precio,cantidad,str(getImgBytes)]
        				elems.append( elemento )
        		except sqlite3.OperationalError as msg:
        			return str(msg)	
    return render_template("editarProducto.html", pageName="Editar Producto", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, elems=elems)

def editProducto(request,session):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	if request.method == 'POST':    			
    		codigo = escape(str(request.form.get('codigo')).strip())
    		nombre = escape(str(request.form.get('nombre')).strip())
    		descripcion = escape(str(request.form.get('descripcion')).strip())
    		precio = escape(str(request.form.get('precio')).strip())
    		cantidad = escape(str(request.form.get('cantidad')).strip())
    		file = request.files['imagen']
    		if file: 
    			mimetype = file.content_type
    			isImgUpload = True
    		else: 
    			mimetype = ""
    			isImgUpload = False
    		if descripcion is None: descripcion = ""
    		if (isImgUpload):
    			queries = "UPDATE producto SET nombre=?,descripcion=?,precio=?,cantidad=?,imagen=?,tipoImagen=? WHERE codigo=?;"
    			urlImage = base64.b64encode(utilsMethod.blobImageUpload(request,'imagen'))
    			getimgBase64Hex = urlImage
    			ImgDataURI = "data:%s;base64,%s" % (mimetype, getimgBase64Hex.decode("utf-8"))		
    			data_params = (nombre,descripcion,precio,cantidad,ImgDataURI,mimetype,codigo)		
    		else:
    			queries = "UPDATE producto SET nombre=?,descripcion=?,precio=?,cantidad=? WHERE codigo=?;"    				
    			data_params = (nombre,descripcion,precio,cantidad,codigo)	
    		if len(nombre)!=0 and len(precio)!=0 and len(cantidad)!=0:
    			with DBManager() as db:
    				try:
    					db.execute(queries, data_params)
    					db.commit()	
    					return "ok"
    				except sqlite3.OperationalError as msg:
    					return render_template("editarProducto.html", pageName="Editar Producto", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error=str(msg))
    		else:
    				return render_template("editarProducto.html", pageName="Editar Producto", Loggedin=_Loggedin_,userID=_userID_,rolID=_rolID_,photo=_photo_, error="Hay campos vacios en el formulario.")

def deleteProducto(request,session,codigoProducto):
    	_Loggedin_ = utilsMethod.Loggedin(session)
    	_userID_ = utilsMethod.userIDSession(session)
    	_rolID_ = utilsMethod.rolIDSession(session)
    	_photo_ = usuario.get_imageProfile(session)
    	queries = "DELETE FROM producto WHERE codigo = ?;"
    	data_params = (int(codigoProducto),)
    	with DBManager() as db:
    				try:
    					result = db.execute(queries, data_params)
    					return str("ok")
    				except sqlite3.OperationalError as msg:
    					return str("fail")