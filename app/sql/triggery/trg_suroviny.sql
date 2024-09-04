
CREATE TRIGGER trg_log_suroviny
ON sklad_surovin
AFTER DELETE, UPDATE
AS
BEGIN

    INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
    SELECT GETDATE(), SYSTEM_USER, 'DELETE suroviny', 'Vymazana surovina s kodem: ' + CONVERT(VARCHAR, d.id_suroviny), 'SUCCESS'
    FROM deleted d; 
    
	INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
	SELECT GETDATE(), SYSTEM_USER, 'UPDATE suroviny', 'Aktualizovana surovina s kodem: ' + CONVERT(VARCHAR, i.id_suroviny), 'SUCCESS'
	FROM inserted i; 

END;

