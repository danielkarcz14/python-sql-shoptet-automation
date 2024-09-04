CREATE TRIGGER trg_log_produkty
ON produkty
AFTER DELETE, UPDATE
AS
BEGIN

    INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
    SELECT GETDATE(), SYSTEM_USER, 'DELETE produkty', 'Vymazan zaznam: ' + CONVERT(VARCHAR, d.id_produktu), 'SUCCESS'
    FROM deleted d; 
    
	INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
	SELECT GETDATE(), SYSTEM_USER, 'UPDATE produkty', 'Aktualizovan zaznam: ' + CONVERT(VARCHAR, i.id_produktu), 'SUCCESS'
	FROM inserted i; 

END;

