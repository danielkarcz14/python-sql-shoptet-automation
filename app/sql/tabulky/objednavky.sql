CREATE TABLE objednavky (
    kod_objednavky VARCHAR(20) NOT NULL UNIQUE,
    datum_vytvoreni DATE,
	PRIMARY KEY(kod_objednavky)
);
