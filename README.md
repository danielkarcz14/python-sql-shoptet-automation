# Přehled projektu

Tento projekt je navržen pro automatizaci a optimalizaci procesu správy skladových zásob pro e-shop dekorativni-omitka.cz, který se specializuje na prodej marmolitů, betonových stěrek a dalších přislušenství. Stávající systém správy zásob, které se týkají marmolutů je manuální a spoléhá na intuici majitele, který rozhoduje, kdy je třeba objednat další materiál. Moje řešení využívá SQL databázi a Python skripty k automatizaci sledování množství zásob na skladě. Generuje PDF report obsahující aktuální množství a spotřebu materiálu a zasílá ho emailem každých 24 hodin.


# Komponenty projektu

## 1. SQL databáze

### Tabulky:
* dodavatel
* objednavky
* polozky_objednavky
* suroviny
* produkt_surovina (vztah mezi produktem a surovinou)
* produkty
* zaznamy_udalosti


## 2. Python skripty
#### db_connection.py
* Modul pro připojení k databázi.

#### orders_processor.py
* Skript pro načtení, zpracování a vložení objednávek do databáze.

#### generate_report.py
* Skript pro generování a odesílání reportů.

#### event_logger.py
* Modul pro zaznamenávání událostí do tabulky zaznamy_udalosti.


## 3. Automatizace
* Celý systém je automatizován pomocí crontab na Linux instanci AWS.
* Skripty se spouštějí každých 24 hodin, aby byla databáze a reporty neustále aktuální.


### Výsledek
* Automatizovaná správa zásob:

    * Objednávky jsou zpracovávány denně a množství surovin je automaticky aktualizováno.
    * Měsíční reporty jsou generovány a odesílány e-mailem a poskytují podrobný přehled o spotřebě materiálů a doporučení k nákupu.


* Manuální operace:

    * Pokud je to potřeba, skripty lze spustit ručně pro okamžitou aktualizaci databáze nebo regeneraci reportů.