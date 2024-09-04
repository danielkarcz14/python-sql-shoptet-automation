-- =======================================================
-- Create Stored Procedure Template for Azure SQL Database
-- =======================================================


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE spotrebovane_kbeliky (
	@p_start_date DATE = '19000101',
	@p_end_date DATE = '99991231'
)
AS
BEGIN

	SET NOCOUNT ON
	


	SELECT ps.kod_suroviny, s.nazev, s.zrnitost, SUM(ps.mnozstvi * po.mnozstvi_ks) AS 'Spotrebovane_kbeliky'
	FROM produkt_surovina ps
	JOIN polozky_objednavky po ON po.kod_produktu = ps.kod_produktu
	JOIN suroviny s on ps.kod_suroviny = s.kod_suroviny
	JOIN objednavky o on po.kod_objednavky = o.kod_objednavky
	WHERE merna_jednotka = 'ks' AND o.datum_vytvoreni BETWEEN @p_start_date AND @p_end_date
	GROUP BY ps.kod_suroviny, s.zrnitost, s.nazev
	ORDER BY ps.kod_suroviny ASC;


END
GO