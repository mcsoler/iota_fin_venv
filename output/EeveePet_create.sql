-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-11-21 02:50:42.703

-- tables
-- Table: Carrito
CREATE TABLE Carrito (
    idCarrito int  NOT NULL IDENTITY(1, 1),
    codigoCarrito nvarchar(15)  NOT NULL,
    CONSTRAINT Carrito_pk PRIMARY KEY  (idCarrito)
);

-- Table: Categoria
CREATE TABLE Categoria (
    idCategoria int  NOT NULL IDENTITY(1, 1),
    categoria varchar(100)  NOT NULL,
    descripcion varchar(500)  NULL,
    CONSTRAINT Categoria_pk PRIMARY KEY  (idCategoria)
);

-- Table: DetalleVenta
CREATE TABLE DetalleVenta (
    idDetalleVenta int  NOT NULL IDENTITY(1, 1),
    idVenta int  NOT NULL,
    idProducto int  NOT NULL,
    idCarrito int  NOT NULL,
    cantidad int  NOT NULL,
    subtotal money  NOT NULL,
    CONSTRAINT DetalleVenta_pk PRIMARY KEY  (idDetalleVenta)
);

-- Table: Distrito
CREATE TABLE Distrito (
    idDistrito int  NOT NULL IDENTITY(1, 1),
    distrito varchar(100)  NOT NULL,
    idProvincia int  NOT NULL,
    CONSTRAINT Distrito_pk PRIMARY KEY  (idDistrito)
);

-- Table: Pais
CREATE TABLE Pais (
    idPais int  NOT NULL IDENTITY(1, 1),
    pais varchar(50)  NOT NULL,
    CONSTRAINT Pais_pk PRIMARY KEY  (idPais)
);

-- Table: Producto
CREATE TABLE Producto (
    idProducto int  NOT NULL IDENTITY(1, 1),
    producto varchar(100)  NOT NULL,
    fechaCreacion datetime  NOT NULL,
    fechaModificacion datetime  NULL,
    descripcion varchar(500)  NULL,
    stock int  NOT NULL,
    imagenUrl varchar(1000)  NULL,
    precio money  NOT NULL,
    idCategoria int  NOT NULL,
    CONSTRAINT Producto_pk PRIMARY KEY  (idProducto)
);

-- Table: Promocion
CREATE TABLE Promocion (
    idPromocion int  NOT NULL IDENTITY(1, 1),
    codigo nvarchar(15)  NOT NULL,
    descripcion varchar(500)  NULL,
    descuento money  NOT NULL,
    fechaInicio datetime  NOT NULL,
    fechaFin datetime  NOT NULL,
    fechaCreacion datetime  NOT NULL,
    activo bit  NOT NULL,
    CONSTRAINT Promocion_pk PRIMARY KEY  (idPromocion)
);

-- Table: Provincia
CREATE TABLE Provincia (
    idProvincia int  NOT NULL IDENTITY(1, 1),
    provincia varchar(100)  NOT NULL,
    idPais int  NOT NULL,
    CONSTRAINT Provincia_pk PRIMARY KEY  (idProvincia)
);

-- Table: Rol
CREATE TABLE Rol (
    idRol int  NOT NULL IDENTITY(1, 1),
    rol varchar(50)  NOT NULL,
    CONSTRAINT Rol_pk PRIMARY KEY  (idRol)
);

-- Table: TipoComprobante
CREATE TABLE TipoComprobante (
    idTipoComprobante int  NOT NULL IDENTITY(1, 1),
    tipoComprobante varchar(150)  NOT NULL,
    CONSTRAINT TipoComprobante_pk PRIMARY KEY  (idTipoComprobante)
);

-- Table: TipoPago
CREATE TABLE TipoPago (
    idTipoPago int  NOT NULL IDENTITY(1, 1),
    tipoPago varchar(100)  NOT NULL,
    CONSTRAINT TipoPago_pk PRIMARY KEY  (idTipoPago)
);

-- Table: Usuario
CREATE TABLE Usuario (
    IdUsuario int  NOT NULL IDENTITY(1, 1),
    nombre varchar(50)  NULL,
    apellido varchar(100)  NULL,
    usuario nvarchar(100)  NULL,
    email varchar(100)  NOT NULL,
    direccion varchar(150)  NULL,
    contrasenia varchar(500)  NOT NULL,
    fechaRegistro datetime  NOT NULL,
    fechaModificacion datetime  NULL,
    idRol int  NOT NULL,
    idDistrito int  NOT NULL,
    CONSTRAINT Usuario_pk PRIMARY KEY  (IdUsuario)
);

-- Table: Venta
CREATE TABLE Venta (
    idVenta int  NOT NULL IDENTITY(1, 1),
    IdUsuario int  NOT NULL,
    idPromocion int  NULL,
    fechaVenta datetime  NOT NULL,
    idTipoComprobante int  NOT NULL,
    totalParcial money  NOT NULL,
    total money  NOT NULL,
    idTipoPago int  NOT NULL,
    CONSTRAINT Venta_pk PRIMARY KEY  (idVenta)
);

-- foreign keys
-- Reference: DetalleVenta_Carrito (table: DetalleVenta)
ALTER TABLE DetalleVenta ADD CONSTRAINT DetalleVenta_Carrito
    FOREIGN KEY (idCarrito)
    REFERENCES Carrito (idCarrito);

-- Reference: DetalleVenta_Producto (table: DetalleVenta)
ALTER TABLE DetalleVenta ADD CONSTRAINT DetalleVenta_Producto
    FOREIGN KEY (idProducto)
    REFERENCES Producto (idProducto);

-- Reference: DetalleVenta_Venta (table: DetalleVenta)
ALTER TABLE DetalleVenta ADD CONSTRAINT DetalleVenta_Venta
    FOREIGN KEY (idVenta)
    REFERENCES Venta (idVenta);

-- Reference: Distrito_Provincia (table: Distrito)
ALTER TABLE Distrito ADD CONSTRAINT Distrito_Provincia
    FOREIGN KEY (idProvincia)
    REFERENCES Provincia (idProvincia);

-- Reference: Producto_Categoria (table: Producto)
ALTER TABLE Producto ADD CONSTRAINT Producto_Categoria
    FOREIGN KEY (idCategoria)
    REFERENCES Categoria (idCategoria);

-- Reference: Provincia_Pais (table: Provincia)
ALTER TABLE Provincia ADD CONSTRAINT Provincia_Pais
    FOREIGN KEY (idPais)
    REFERENCES Pais (idPais);

-- Reference: Usuario_Distrito (table: Usuario)
ALTER TABLE Usuario ADD CONSTRAINT Usuario_Distrito
    FOREIGN KEY (idDistrito)
    REFERENCES Distrito (idDistrito);

-- Reference: Usuario_Rol (table: Usuario)
ALTER TABLE Usuario ADD CONSTRAINT Usuario_Rol
    FOREIGN KEY (idRol)
    REFERENCES Rol (idRol);

-- Reference: Venta_Promocion (table: Venta)
ALTER TABLE Venta ADD CONSTRAINT Venta_Promocion
    FOREIGN KEY (idPromocion)
    REFERENCES Promocion (idPromocion);

-- Reference: Venta_TipoComprobante (table: Venta)
ALTER TABLE Venta ADD CONSTRAINT Venta_TipoComprobante
    FOREIGN KEY (idTipoComprobante)
    REFERENCES TipoComprobante (idTipoComprobante);

-- Reference: Venta_TipoPago (table: Venta)
ALTER TABLE Venta ADD CONSTRAINT Venta_TipoPago
    FOREIGN KEY (idTipoPago)
    REFERENCES TipoPago (idTipoPago);

-- Reference: Venta_Usuario (table: Venta)
ALTER TABLE Venta ADD CONSTRAINT Venta_Usuario
    FOREIGN KEY (IdUsuario)
    REFERENCES Usuario (IdUsuario);

-- End of file.

