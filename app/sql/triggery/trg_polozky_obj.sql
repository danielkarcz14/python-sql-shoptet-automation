
CREATE TRIGGER trg_log_polozky_obj
ON polozky_objednavky
AFTER DELETE, UPDATE
AS
BEGIN

    INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
    SELECT GETDATE(), SYSTEM_USER, 'DELETE polozky_objednavky', 'Vymazana polozka obj s obj id: ' + CONVERT(VARCHAR, d.id_objednavky) + 'a kodem produktu' + CONVERT(VARCHAR, d.id_produktu), 'SUCCESS'
    FROM deleted d; 
    
	INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
	SELECT GETDATE(), SYSTEM_USER, 'UPDATE polozky_objednavky', 'Aktualizovana polozka obj s obj id: ' + CONVERT(VARCHAR, i.id_objednavky) + 'a kodem produktu' + CONVERT(VARCHAR, i.id_produktu), 'SUCCESS'
	FROM inserted i; 

END;

