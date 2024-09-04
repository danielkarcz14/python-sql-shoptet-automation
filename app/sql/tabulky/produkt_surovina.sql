CREATE TABLE produkt_surovina (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_produktu VARCHAR(20),
    id_suroviny VARCHAR(20),
    mnozstvi_kg FLOAT NOT NULL CHECK (mnozstvi_kg > 0),
    FOREIGN KEY (id_produktu) REFERENCES produkty(id_produktu),
    FOREIGN KEY (id_suroviny) REFERENCES sklad_surovin(id_suroviny)
);
