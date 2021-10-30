from locale import currency
from flask import Flask, render_template, url_for, redirect, request, session
from routes import urls

import sqlite3
from sqlite3.dbapi2 import Error

from DBManager import DBManager
import utilsMethod
import config

import usuario
import producto
import wishlist
import comentarios

import base64

from markupsafe import escape

app = Flask(__name__) #creating the Flask class object 
  
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)

app.secret_key = config.SECRET_KEY

@app.route(urls.VIEW_LOGIN['r'], methods=urls.VIEW_LOGIN['m'])
def login():
	return usuario.ingreso(request,session)

@app.route(urls.VIEW_LOGIN_ADMIN['r'], methods=urls.VIEW_LOGIN_ADMIN['m'])
def loginAdmin():
	return usuario.ingresoAdmin(request,session)

@app.route(urls.VIEW_LOGOUT['r'], methods=urls.VIEW_LOGOUT['m'])
def logout():
    return usuario.logout(request,session)

@app.route(urls.VIEW_REGISTER['r'], methods=urls.VIEW_REGISTER['m'])
def register():   	
  	return usuario.registro(request,session)

@app.route(urls.VIEW_CHANGE_PASSWORD['r'], methods=urls.VIEW_CHANGE_PASSWORD['m'])
def changePassword():
    return usuario.changePassword(request,session)

@app.route(urls.VIEW_MY_PROFILE['r'], methods=urls.VIEW_MY_PROFILE['m'])
def myProfile():     	
  	return usuario.get_myProfile(request,session)   

@app.route(urls.VIEW_LIST_ALL_USUARIOS['r'], methods=urls.VIEW_LIST_ALL_USUARIOS['m'])
def listAllUsers():     	
  	return usuario.list_AllUsers(request,session)

@app.route(urls.VIEW_DELETE_USER['r'], methods=urls.VIEW_DELETE_USER['m'])
def deleteUsuario(username):
    _Loggedin_ = utilsMethod.Loggedin(session)    
    if (_Loggedin_):
        return usuario.deleteUsuario(request,session,username) 
    else:
        return usuario.nonAccess(request,session)     

# ------------------------------------------------------------------------
# methods for the entity 'producto'

@app.route(urls.VIEW_INDEX['r'], methods=urls.VIEW_INDEX['m'])
def index():
	return producto.listProducts(request,session)

@app.route(urls.VIEW_CREATE_PRODUCT['r'], methods=urls.VIEW_CREATE_PRODUCT['m'])
def post_productos():
    _Loggedin_ = utilsMethod.Loggedin(session)    
    if (_Loggedin_):
        return producto.createProductos(request,session)          
    else:
        return usuario.nonAccess(request,session)    

@app.route(urls.VIEW_READ_PRODUCT['r'], methods=urls.VIEW_READ_PRODUCT['m'])
def get_producto(codigoProducto):
    return producto.get_producto(request,session,codigoProducto)

@app.route(urls.VIEW_EDIT_VIEW_PRODUCT['r'], methods=urls.VIEW_EDIT_VIEW_PRODUCT['m'])
def editViewProducto(codigoProducto):
    return producto.editViewProducto(request,session,codigoProducto)

@app.route(urls.VIEW_EDIT_PRODUCT['r'], methods=urls.VIEW_EDIT_PRODUCT['m'])
def editProducto():
    return producto.editProducto(request,session)	
	    	
@app.route(urls.VIEW_DELETE_PRODUCT['r'], methods=urls.VIEW_DELETE_PRODUCT['m'])
def deleteProducto(codigoProducto):
    return producto.deleteProducto(request,session,codigoProducto)

# ------------------------------------------------------------------------
# methods for the entity 'comentarios' 

@app.route(urls.VIEW_CREATE_COMENTARIO['r'], methods=urls.VIEW_CREATE_COMENTARIO['m'])
def createComentario():
    return comentarios.create_Comentario(request,session)

@app.route(urls.VIEW_READ_COMENTARIO['r'], methods=urls.VIEW_READ_COMENTARIO['m'])
def getComentario(nombre,codigoProducto,precio):
    return comentarios.get_Comentario(request,session,nombre,codigoProducto,precio)

@app.route(urls.VIEW_LIST_COMENTARIO['r'], methods=urls.VIEW_LIST_COMENTARIO['m'])
def listComentarios(codigoProducto):
    return comentarios.list_Comentarios(request,session,codigoProducto)

@app.route(urls.VIEW_LIST_USER_COMENTARIO['r'], methods=urls.VIEW_LIST_USER_COMENTARIO['m'])
def listUserComentarios():
    return comentarios.list_User_Comentarios(request,session)

@app.route(urls.VIEW_LIST_ALL_COMENTARIO['r'], methods=urls.VIEW_LIST_ALL_COMENTARIO['m'])
def listAllComentarios():
    return comentarios.list_all_Comentarios(request,session)

@app.route(urls.VIEW_DELETE_COMENTARIO['r'], methods=urls.VIEW_DELETE_COMENTARIO['m'])
def deleteComentario(codigoProducto,username):
    return comentarios.delete_Comentario(request,session,codigoProducto,username)

# ------------------------------------------------------------------------
# methods for the entity 'wishlist' 

@app.route(urls.VIEW_CREATE_WISHLIST['r'], methods=urls.VIEW_CREATE_WISHLIST['m'])
def createWishList():
    return wishlist.createWishList(request,session)

@app.route(urls.VIEW_LIST_WISHLIST['r'], methods=urls.VIEW_LIST_WISHLIST['m'])
def listWishList():
    return wishlist.listWishList(request,session)

@app.route(urls.VIEW_DELETE_WISHLIST['r'], methods=urls.VIEW_DELETE_WISHLIST['m'])
def deleteWishList(codigoProducto,username):
    return wishlist.deleteWishList(request,session,codigoProducto,username)

# ------------------------------------------------------------------------

# Execute
if __name__ =='__main__': 
	app.run(use_reloader=config.USE_RELOADER,threaded=config.THREADED,debug=config.DEBUG,host=config.HOST)  