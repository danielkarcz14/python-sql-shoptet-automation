-- =======================================================
-- Create Stored Procedure Template for Azure SQL Database
-- =======================================================

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE aktualizovat_mnozstvi_surovin (
  @p_id_produktu varchar(20)
)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    SET NOCOUNT ON

	DECLARE @id_suroviny varchar(20);

	SELECT @id_suroviny = ps.id_suroviny
    FROM produkt_surovina ps
    WHERE ps.id_produktu = @p_id_produktu;

	UPDATE sklad_surovin 
	SET mnozstvi = mnozstvi - (
	  SELECT SUM(ps.mnozstvi * po.mnozstvi_ks)
	  FROM produkt_surovina ps
	  JOIN polozky_objednavky po ON po.id_produktu = ps.id_produktu
	  JOIN objednavky o ON po.id_objednavky = o.id_objednavky
	  WHERE ps.id_suroviny = sklad_surovin.id_suroviny
		AND ps.id_produktu = @p_id_produktu
		AND CAST(o.datum_vytvoreni AS DATE) = DATEADD(DAY, -1, CAST(GETDATE() AS DATE))
	)
	WHERE EXISTS (
	  SELECT 1
	  FROM produkt_surovina ps
	  WHERE ps.id_suroviny = sklad_surovin.id_suroviny
		AND ps.id_produktu = @p_id_produktu
		AND EXISTS (
            SELECT 1
            FROM polozky_objednavky po
            JOIN objednavky o ON po.id_objednavky = o.id_objednavky
            WHERE po.id_produktu = @p_id_produktu
            AND CAST(o.datum_vytvoreni AS DATE) = DATEADD(DAY, -1, CAST(GETDATE() AS DATE))
        )
	);

END
GO

