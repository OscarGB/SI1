
--
-- Tablas generales (sin relaciones)
--

CREATE TABLE public.clientes (
	clienteid integer            	PRIMARY KEY		NOT NULL,
	tarjeta character varying(50) 					NOT NULL,
	saldo real 										NOT NULL,    
	email character varying(50),
	nombre character varying(50) 					NOT NULL,
	password character varying(50) 					NOT NULL
);

ALTER TABLE public.clientes OWNER TO alumnodb;

CREATE TABLE public.actores (
    actorid integer					PRIMARY KEY		NOT NULL,
    nombre character varying(128) 					NOT NULL
);

ALTER TABLE public.actores OWNER TO alumnodb;

CREATE TABLE public.directores (
    directorid integer 				PRIMARY KEY		NOT NULL,
    nombre character varying(128) 					NOT NULL
);

ALTER TABLE public.directores OWNER TO alumnodb;

CREATE TABLE public.paises (
    paisid integer 					PRIMARY KEY		NOT NULL,
    nombre character varying(32) 					NOT NULL
);

ALTER TABLE public.paises OWNER TO alumnodb;

CREATE TABLE public.generos (
    generoid integer 				PRIMARY KEY		NOT NULL,
    nombre character varying(32) 					NOT NULL
);

ALTER TABLE public.generos OWNER TO alumnodb;

CREATE TABLE public.lenguas (
    lenguaid integer 				PRIMARY KEY		NOT NULL,
    nombre character varying(32) 					NOT NULL
);

ALTER TABLE public.lenguas OWNER TO alumnodb;


CREATE TABLE public.peliculas (
    peliculaid integer 				PRIMARY KEY		NOT NULL,
    titulo character varying(255) 					NOT NULL,
    estreno text									NOT NULL
);

ALTER TABLE public.peliculas OWNER TO alumnodb;

CREATE TABLE public.pedidos (
    pedidoid integer 				PRIMARY KEY		NOT NULL,
    fecha date 										NOT NULL,
    clienteid integer				REFERENCES clientes(clienteid),
    preciototal numeric,
    estado character varying(10)
);

ALTER TABLE public.pedidos OWNER TO alumnodb;

CREATE TABLE public.productos (
    productoid integer 				PRIMARY KEY 	NOT NULL,
    peliculaid integer 				REFERENCES peliculas(peliculaid),
    precio numeric 									NOT NULL,
    descripcion character varying(30) 				NOT NULL,
    stock integer									NOT NULL,
    ventas integer 									NOT NULL
);

ALTER TABLE public.productos OWNER TO alumnodb;

--
-- Tablas para relaciones
--

CREATE TABLE public.detallespedidos (
    pedidoid integer 				REFERENCES pedidos(pedidoid),
    productoid integer 				REFERENCES productos(productoid),
    precio numeric,
    cantidad integer 								NOT NULL
);

ALTER TABLE public.detallespedidos OWNER TO alumnodb;

CREATE TABLE public.actorpeliculas (
    actorid integer 				REFERENCES actores(actorid),
    peliculaid integer 				REFERENCES peliculas(peliculaid),
    personaje text 									NOT NULL,
    esvoz smallint 			DEFAULT (0)::smallint 	NOT NULL
);

ALTER TABLE public.actorpeliculas OWNER TO alumnodb;

CREATE TABLE public.directorpeliculas (
    directorid integer 				REFERENCES directores(directorid),
    peliculaid integer 				REFERENCES peliculas(peliculaid)
);

ALTER TABLE public.directorpeliculas OWNER TO alumnodb;

CREATE TABLE public.lenguapeliculas (
    lenguaid integer 				REFERENCES lenguas(lenguaid),
    peliculaid integer 				REFERENCES peliculas(peliculaid)
);

ALTER TABLE public.lenguapeliculas OWNER TO alumnodb;

CREATE TABLE public.paispeliculas (
    paisid integer 					REFERENCES paises(paisid),
    peliculaid integer 				REFERENCES peliculas(peliculaid)
);

ALTER TABLE public.paispeliculas OWNER TO alumnodb;

CREATE TABLE public.generopeliculas (
    generoid integer 				REFERENCES generos(generoid),
    peliculaid integer 				REFERENCES peliculas(peliculaid)
);

ALTER TABLE public.generopeliculas OWNER TO alumnodb;

--
-- Copiar datos
--

INSERT INTO public.clientes (clienteid, tarjeta, saldo, email, nombre, password)
SELECT customerid, creditcard, 80, email, CONCAT(firstname, ' ', lastname) as fullname, password
FROM public.customers;

INSERT INTO public.actores (actorid, nombre)
SELECT actorid, actorname FROM imdb_actors;

INSERT INTO public.directores (directorid, nombre)
SELECT directorid, directorname FROM imdb_directors;

INSERT INTO public.peliculas (peliculaid, titulo, estreno)
SELECT movieid, movietitle, year FROM imdb_movies;

INSERT INTO public.pedidos (pedidoid, fecha, clienteid, preciototal, estado)
SELECT orderid, orderdate, customerid, totalamount, status FROM orders;