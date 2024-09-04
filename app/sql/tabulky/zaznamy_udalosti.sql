CREATE TABLE zaznamy_udalosti (
	id_zaznamu INT PRIMARY KEY NOT NULL IDENTITY (1, 1),
	cas DATETIME DEFAULT GETDATE(),
	uzivatel VARCHAR(255) NOT NULL,
	skript VARCHAR(50) NOT NULL,
	popis VARCHAR(255) NOT NULL,
	stav CHAR(50) CHECK (stav in ('SUCCESS', 'ERROR'))
);