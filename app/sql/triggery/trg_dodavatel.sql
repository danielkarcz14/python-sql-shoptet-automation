
CREATE TRIGGER trg_log_dodavatel
ON dodavatel
AFTER INSERT, DELETE, UPDATE
AS
BEGIN

    INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
    SELECT GETDATE(), SYSTEM_USER, 'DELETE dodavatel', 'Vymazan zaznam dodavatele: ' + CONVERT(VARCHAR, d.jmeno), 'SUCCESS'
    FROM deleted d; 
    
	INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
	SELECT GETDATE(), SYSTEM_USER, 'UPDATE dodavatel', 'Aktualizovan zaznam dodavatele: ' + CONVERT(VARCHAR, i.jmeno), 'SUCCESS'
	FROM inserted i; 

END;

