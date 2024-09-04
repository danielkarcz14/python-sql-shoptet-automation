CREATE TRIGGER trg_automaticka_aktualizace_surovin
ON polozky_objednavky
AFTER INSERT
AS
BEGIN
    -- Deklarace kurzoru pro iteraci přes nově vložené záznamy v tabulce polozky_objednavky
    DECLARE @orderCursor CURSOR;
    DECLARE @id_produktu VARCHAR(20);

    -- Inicializace kurzoru na unikátní id_produktu
    SET @orderCursor = CURSOR FOR
        SELECT DISTINCT id_produktu
        FROM inserted;

    -- Otevření kurzoru pro iteraci
    OPEN @orderCursor;

    -- Načtení prvního id do proměnné @id_produktu
    FETCH NEXT FROM @orderCursor INTO @id_produktu;

    -- Loop pro zpracování všech produktů
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Volání procedury pro aktuální id_produktu
        EXEC aktualizovat_mnozstvi_surovin @p_id_produktu = @id_produktu;

        -- Načtení dalšího id_produktu
        FETCH NEXT FROM @orderCursor INTO @id_produktu;
    END

    -- Uzavření kurzoru po dokončení iterace
    CLOSE @orderCursor;

    -- Uvolnění paměti alokované pro kurzor
    DEALLOCATE @orderCursor;
END;
