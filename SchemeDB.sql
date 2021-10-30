CREATE TABLE dbECommerce.usuarios(
   username    TEXT PRIMARY KEY NOT NULL,
   password    TEXT NOT NULL, 
   salt    	   TEXT NOT NULL,   
   nombres     CHAR(100),
   apellidos   CHAR(100),
   tipoDoc     CHAR(10),
   documento   INT,
   telefono    INT,
   email       TEXT,
   direccion   TEXT,
   imagen      TEXT,
   tipoImagen  CHAR(100)
);

CREATE TABLE dbECommerce.administrador(
   username    TEXT PRIMARY KEY NOT NULL,
   password    TEXT NOT NULL,   
   salt    	   TEXT NOT NULL,
   email       TEXT
);

CREATE TABLE dbECommerce.superAdministrador(
   username    TEXT PRIMARY KEY NOT NULL,
   password    TEXT NOT NULL,
   salt    	   TEXT NOT NULL,   
   email       TEXT
);

CREATE TABLE dbECommerce.producto(
   codigo      INT PRIMARY KEY NOT NULL,
   nombre      TEXT NOT NULL,   
   descripcion TEXT,
   precio      DOUBLE NOT NULL, 
   cantidad    DOUBLE NOT NULL,   
   imagen      TEXT,
   tipoImagen  CHAR(100)
);

CREATE TABLE dbECommerce.comentarios(   
   username      TEXT NOT NULL,  
   codigo        INT NOT NULL,
   calificacion  INT NOT NULL,
   comentario    TEXT,
   foreign key(username) references usuarios(username),
   foreign key(codigo) references producto(codigo)  
);

CREATE TABLE dbECommerce.wishList(   
   username      TEXT NOT NULL,  
   codigo        INT NOT NULL,
   foreign key(username) references usuarios(username),
   foreign key(codigo) references producto(codigo)  
);

/* Password = 1234 */
INSERT INTO dbECommerce.administrador (username,password,salt,email) VALUES
('admin','78f869ce6c43143a2999b5ffcf34a015fd4b4d6923420f84da1f0e6b3db8a0e9','539ab4905d2354fbee2f32d17d19ac91ff909a4a773caef471978cd2f313946c','admin@ecommerce.com' );
/* Password = 1234 */	
INSERT INTO dbECommerce.superAdministrador (username,password,salt,email) VALUES
('superadmin','a40235ce8e810a2c015d5866e16cdd3611b9d86997df683f053fd83cf7fa01a7','7b01b0a519ab8c4e57e66089f54f469bf2b80ace337b61fea88638db4aa88837','superadmin@ecommerce.com' );
