import csv
import requests
import os

from io import StringIO
from db_connection import db_connection
from event_logger import EventLogger 
from datetime import timedelta, date, time, datetime


# Připojení k databázi a inicializace loggeru událostí
conn, cur, user = db_connection()
event_logger = EventLogger(conn, cur)

# Limit pro opakování pokusu připojení k databázi
RETRY_LIMIT = 5


# Třída pro zpracování objednávek
class OrdersProcessor:
    def __init__(self, event_logger):
        self.event_logger = event_logger

    def fetch_orders(self, url):
        # Stažení objednávek z URL feedu ve formátu CSV
        response = requests.get(url)
        if response.status_code == 200:
            # Pokud je odpověď úspěšná, načte obsah jako CSV
            content = StringIO(response.text)
            return csv.DictReader(content)
        else:
            # V případě chyby při stažení objednávek zaloguje chybu
            error_message = f"Chyba při stazeni objednavek z URL: {url}"
            self.event_logger.log_error("OrderProcessor", "fetch_orders", error_message)
            return None

    def extract_date(self, date_time_str):
        return date_time_str.split()[0]

    def filter_orders(self, orders, target_date):
        # Filtrování objednávek se včerejším datem 
        return [order for order in orders if self.extract_date(order['date']) == target_date.strftime("%Y-%m-%d")]

    def process_orders(self, url, target_date):
        # Načtení objednávek z URL
        orders = self.fetch_orders(url)

        # Filtrování objednávek na základě zadaného data
        filtered_orders = self.filter_orders(orders, target_date)
        for order in filtered_orders:
            # Zpracování pouze objednávek, které začínají kódem H1 nebo H2 (marmolity)
            if order['orderItemCode'].startswith('H1') or order['orderItemCode'].startswith('H2'):
                price = order['orderItemUnitPriceWithVat'].replace(",", ".")

                # Kontrola, zda objednávka s tímto ID již existuje v databázi
                if self.check_order_exists(order['id']) is None:
                    try:
                        # Vložení nové objednávky do databáze a zalogování úspěšného vložení
                        cur.execute("INSERT INTO objednavky (id_objednavky, datum_vytvoreni) VALUES (?, ?)", (order['id'], order['date']))
                        conn.commit() 
                        event_logger.log_success(user, os.path.basename(__file__), f"vlozena objednavka s id: {order['id']}")
                    except Exception as e:
                        # Zalogování chyby, pokud vložení do databáze selže
                        event_logger.log_error(user, os.path.basename(__file__), f"chyba pri vlozeni objednavky s id {order['id']}, chyba: {str(e)}")
                
                # Získání ID vložené objednávky z databáze
                cur.execute("SELECT id_objednavky FROM objednavky WHERE id_objednavky = ?", (order['id'],))
                order_id = cur.fetchone()[0]

                # Kontrola a vložení položek objednávky do databáze
                if order['id'] == order_id and self.check_order_item_exists(order_id, order['orderItemCode'])[0] == 0:
                    try:
                        # Vložení nové položky objednávky do databáze a zalogování úspěšného vložení
                        cur.execute(
                            """
                            INSERT INTO polozky_objednavky (id_objednavky, mnozstvi_ks, id_produktu, cena, nazev) VALUES (?, ?, ?, ?, ?)
                            """, (order_id, order['orderItemAmount'], order['orderItemCode'], price, order['orderItemVariantName']))
                        conn.commit()  
                        event_logger.log_success(user, os.path.basename(__file__), f"vlozena polozka objednavky s id: {order['orderItemCode']} {order['orderItemAmount']}ks")
                    except Exception as e:
                        # Zalogování chyby, pokud vložení do databáze selže
                        event_logger.log_error(user, os.path.basename(__file__), f"chyba pri vlozeni polozky objednavky s id polozky {order['orderItemCode']}, chyba: {str(e)}")

    def check_order_exists(self, order_id):
        # Kontrola, zda objednávka s daným ID již existuje v databázi
        cur.execute("SELECT id_objednavky FROM objednavky WHERE id_objednavky = ?", (order_id,))
        return cur.fetchone()

    def check_order_item_exists(self, order_id, product_code):
        # Kontrola, zda položka objednávky již existuje v databázi
        cur.execute("SELECT COUNT(*) FROM polozky_objednavky WHERE id_objednavky = ? AND id_produktu = ?", (order_id, product_code))
        return cur.fetchone()


def main():
    # URL adresa pro stahování objenávek ze Shoptetu v CSV formátu
    url = ""

    # Včerejší datum pro filtrování objednávek
    yesterday = date.today() - timedelta(days=1)

    # V případě selhání připojení k databázi opakovat max RETRY_LIMIT
    retry_count = 0
    while retry_count < RETRY_LIMIT:
        try:
            order_processor = OrdersProcessor(event_logger)
            order_processor.process_orders(url, yesterday)
            break
        except Exception as e:
            if conn:
                conn.close()
            retry_count += 1
            time.sleep(5)

    # Ukončení spojení s databází
    if conn:
        conn.close()


if __name__ == "__main__":
    main()
