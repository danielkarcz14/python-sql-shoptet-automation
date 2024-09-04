CREATE TABLE dodavatel (
	ID_suroviny INT PRIMARY KEY IDENTITY(1, 1) NOT NULL,
	jmeno VARCHAR(50);
	email VARCHAR(150) NOT NULL;
	telefon VARCHAR(50);
)

INSERT INTO dodavatel (jmeno, email, telefon) VALUES ('Jan Novák', 'jannovak@jannovak.cz', '+48444555333');
