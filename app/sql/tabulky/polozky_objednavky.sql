ALTER TABLE polozky_objednavky
ADD CONSTRAINT fk_objednavky
FOREIGN KEY (id_objednavky) REFERENCES objednavky(id_objednavky)
ON DELETE CASCADE;

