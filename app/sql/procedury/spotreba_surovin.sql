-- =======================================================
-- Create Stored Procedure Template for Azure SQL Database
-- =======================================================


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE spotrebova_surovin (
	@p_start_date DATE = '19000101',
	@p_end_date DATE = '99991231',
	@p_merna_jednotka CHAR(20) = ''
)
AS
BEGIN

	SET NOCOUNT ON
	

	SELECT ps.id_suroviny, s.nazev, s.zrnitost, ROUND(SUM(ps.mnozstvi * po.mnozstvi_ks), 2) AS 'mnozstvi'
	FROM produkt_surovina ps
	JOIN polozky_objednavky po ON po.id_produktu = ps.id_produktu
	JOIN sklad_surovin s on ps.id_suroviny = s.id_suroviny
	JOIN objednavky o on po.id_objednavky = o.id_objednavky
	WHERE (s.merna_jednotka = @p_merna_jednotka OR @p_merna_jednotka = '') AND o.datum_vytvoreni BETWEEN @p_start_date AND @p_end_date
	GROUP BY ps.id_suroviny, s.zrnitost, s.nazev
	ORDER BY SUM(ps.mnozstvi * po.mnozstvi_ks)


END
GO