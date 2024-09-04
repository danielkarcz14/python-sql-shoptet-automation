import pyodbc
import configparser
import os

def db_connection():
    # Cesta ke konfiguračnímu souboru
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config", "configfile.ini")

    # Načtení konfiguračního souboru
    config_obj = configparser.ConfigParser()
    config_obj.read(config_path)

    # Načtení databázových parametrů z konfiguračního souboru
    dbparam = config_obj["login"]
    server = dbparam["server"]
    database = dbparam["database"]
    username = dbparam["username"]
    password = dbparam["password"]

    try:
        # Pokus o připojení k databázi pomocí parametrů z konfiguračního souboru
        conn = pyodbc.connect('DRIVER={/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.2.1};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password + ';LOGIN_TIMEOUT=60')
        
        # Vytvoření kurzoru pro provádění SQL dotazů
        cur = conn.cursor()
        
        # Získání uživatelského jména přihlášeného k databázi
        user = conn.getinfo(pyodbc.SQL_USER_NAME)
        return conn, cur, user
    
    except pyodbc.Error as e:
        print(f"Nepodařilo se připojit k db {e}")
        return None
    
