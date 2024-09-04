
CREATE TRIGGER trg_log_obj
ON objednavky
AFTER DELETE, UPDATE
AS
BEGIN

    INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
    SELECT GETDATE(), SYSTEM_USER, 'DELETE objednavky', 'Vymazana obj s obj id: ' + CONVERT(VARCHAR, d.id_objednavky), 'SUCCESS'
    FROM deleted d; 
    
	INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
	SELECT GETDATE(), SYSTEM_USER, 'UPDATE objednavky', 'Aktualizovana obj s obj id: ' + CONVERT(VARCHAR, i.id_objednavky), 'SUCCESS'
	FROM inserted i; 

END;

