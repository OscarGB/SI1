
CREATE TABLE public.clientes (
	clienteid integer            	PRIMARY KEY		NOT NULL,
	tarjeta character varying(50) 					NOT NULL,
	saldo real 										NOT NULL,    
	email character varying(50),
	nombre character varying(50) 					NOT NULL,
	password character varying(50) 					NOT NULL
);

ALTER TABLE public.clientes OWNER TO alumnodb;

CREATE TABLE public.imdb_actormovies (
    actorid integer 									NOT NULL,
    movieid integer 								NOT NULL,
    character text 									NOT NULL,
    isvoice smallint 	DEFAULT (0)::smallint 		NOT NULL
);