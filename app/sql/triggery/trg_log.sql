CREATE TRIGGER trg_log_zaznamy_udalosti
ON zaznamy_udalosti
AFTER DELETE, UPDATE
AS
BEGIN

    INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
    SELECT GETDATE(), SYSTEM_USER, 'SQL DELETE', 'Vymazan zaznam: ' + d.popis, 'Success'
    FROM deleted d; 
    
	INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
	SELECT GETDATE(), SYSTEM_USER, 'UPDATE', 'Aktualizovan zaznam: ' + i.popis, 'Success'
	FROM inserted i; 

END;
