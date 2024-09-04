-- Vytvoøení tabulky produkty
CREATE TABLE produkty (
    kod_produktu VARCHAR(20) UNIQUE NOT NULL,
    nazev VARCHAR(100) NOT NULL,
    hmotnost_kg FLOAT NOT NULL,
	PRIMARY KEY(kod_produktu)
);

