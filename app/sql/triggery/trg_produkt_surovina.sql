CREATE TRIGGER trg_log_produkt_surovina
ON produkt_surovina
AFTER DELETE, UPDATE
AS
BEGIN

    INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
    SELECT GETDATE(), SYSTEM_USER, 'DELETE produkt_surovina', 'Vymazan zaznam: ' + CONVERT(VARCHAR, d.id_suroviny), 'SUCCESS'
    FROM deleted d; 
    
	INSERT INTO zaznamy_udalosti (cas, uzivatel, skript, popis, stav)
	SELECT GETDATE(), SYSTEM_USER, 'UPDATE produkt_surovina', 'Aktualizovan zaznam: ' + CONVERT(VARCHAR, i.id_suroviny), 'SUCCESS'
	FROM inserted i; 

END;
