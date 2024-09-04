ALTER TABLE suroviny
ALTER COLUMN mnozstvi DECIMAL(10, 2); 

UPDATE suroviny
SET mnozstvi = ROUND(mnozstvi, 2);