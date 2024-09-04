CREATE TABLE sklad_surovin (
    id_suroviny VARCHAR(20) UNIQUE,
    nazev CHAR(100) NOT NULL,
    mnozstvi INTEGER NOT NULL,
    merna_jednotka CHAR(20) NOT NULL CHECK (merna_jednotka IN ('ks', 'kg')),
    cena DECIMAL(10, 2) NOT NULL,
	id_dodavatele INT NOT NULL,
	PRIMARY KEY(id_suroviny),
	FOREIGN KEY(id_dodavatele) REFERENCES dodavatel(id_dodavatele)
);
