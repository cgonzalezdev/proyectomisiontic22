# ------------------------------------------------------------------------
# Page Index
VIEW_INDEX = {
  "r": "/",
  "m": ['GET','POST']
}
VIEW_NON_ACCESS = {
  "r": "/nonAccess",
  "m": ['GET']
}
# ------------------------------------------------------------------------
# routes for the entity 'usuario'
VIEW_LOGIN = {
  "r": "/login",
  "m": ['GET','POST']
}
VIEW_LOGIN_ADMIN = {
  "r": "/panelAdmin",
  "m": ['GET','POST']
}
VIEW_LOGOUT = {
  "r": "/logout",
  "m": ['GET']
}
VIEW_REGISTER = {
  "r": "/register",
  "m": ['GET','POST']
}
VIEW_MY_PROFILE = {
  "r": "/myProfile",
  "m": ['GET','POST']
}
VIEW_CHANGE_PASSWORD = {
  "r": "/changePasswd",
  "m": ['GET', 'POST']
}
VIEW_LIST_ALL_USUARIOS = {
  "r": "/listUsers",
  "m": ['GET']
}
VIEW_DELETE_USER = {
  "r": "/user/delete/<username>",
  "m": ['GET']
}
# ------------------------------------------------------------------------
# routes for the entity 'producto'
VIEW_CREATE_PRODUCT = {
  "r": "/producto/create",
  "m": ['GET','POST']
}
VIEW_READ_PRODUCT = {
  "r": "/producto/<int:codigoProducto>",
  "m": ['GET']
}
VIEW_EDIT_VIEW_PRODUCT = {
  "r": "/producto/edit/<int:codigoProducto>",
  "m": ['GET']
}
VIEW_EDIT_PRODUCT = {
  "r": "/producto/edit",
  "m": ['POST']
}
VIEW_DELETE_PRODUCT = {
  "r": "/producto/delete/<int:codigoProducto>",
  "m": ['GET']
}
# ------------------------------------------------------------------------
# routes for the entity 'comentarios'
VIEW_CREATE_COMENTARIO = {
  "r": "/comentario/create",
  "m": ['POST']
}
VIEW_READ_COMENTARIO = {
  "r": "/comentario/read/<nombre>/<int:codigoProducto>/<precio>",
  "m": ['GET']
}
VIEW_LIST_COMENTARIO = {
  "r": "/comentario/<int:codigoProducto>",
  "m": ['GET']
}
VIEW_LIST_USER_COMENTARIO = {
  "r": "/misComentarios",
  "m": ['GET']
}
VIEW_LIST_ALL_COMENTARIO = {
  "r": "/allComentarios",
  "m": ['GET']
}
VIEW_DELETE_COMENTARIO = {
  "r": "/comentario/delete/<int:codigoProducto>/<username>",
  "m": ['GET']
}
# ------------------------------------------------------------------------
# routes for the entity 'wishlist'
VIEW_CREATE_WISHLIST = {
  "r": "/wishlist/create",
  "m": ['POST']
}
VIEW_LIST_WISHLIST = {
  "r": "/wishlist/list",
  "m": ['GET']
}
VIEW_DELETE_WISHLIST = {
  "r": "/wishlist/delete/<int:codigoProducto>/<username>",
  "m": ['GET']
}
# ------------------------------------------------------------------------