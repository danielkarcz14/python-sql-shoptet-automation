import os
import matplotlib.pyplot as plt
import smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from pathlib import Path
from fpdf import FPDF
from datetime import timedelta, datetime, date
from db_connection import db_connection
from event_logger import EventLogger


# Navázání spojení s databázi a inicializace loggeru událostí
conn, cur, user = db_connection()
event_logger = EventLogger(conn, cur)


# Cesta pro ukládání reportů
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
output_dir = current_dir / "reporty"


# Vytvoření složky, pokud neexistuje
output_dir.mkdir(parents=True, exist_ok=True)


# Parametry pro časové období, za které se generují reporty
today_date = datetime.now().date()
end_date = today_date - timedelta(days=30)


# Formátované datumy jako řetězce
END_DATE_STR = today_date.strftime('%Y%m%d')
START_DATE_STR = end_date.strftime('%Y%m%d')


# Definice měrných jednotek
KG = "kg"
KS = "ks"
ALL = ''


def main():
    # Geneorvání reportů pro jednotlivé suroviny
    report_mnozstvi_surovin(KG, "1.mnozstvi_krusiva.png")
    report_spotreba_surovin(KG, "2.spotreba_krusiva.png")
    report_mnozstvi_surovin(KS, "3.mnozstvi_kbeliku.png")
    report_spotreba_surovin(KS, "4.spotreba_kbeliku.png")

    # Vytvoření PDF reportu a jeho odeslání emailem
    create_pdf_report()
    send_report()

    # Uzavření spojení s databází
    conn.close()


# Funkce pro generování grafu na základě zadaných dat
def generate_graph(y_data, x_data, y_label, x_label, title, suffix):
    # Vytvoření gradientu barev pro graf
    min_value = 0
    max_value = max(x_data)
    colors = [plt.cm.YlOrRd_r((value - min_value) / (max_value - min_value)) for value in x_data]

    # Vytvoření horizontálního sloupcového grafu
    plt.figure(figsize=(12, 10))  # Zvětšení rozměrů obrázku
    bars = plt.barh(y_data, x_data, color=colors)  # Použití barev z vytvořeného gradientu
    plt.xlabel(y_label, fontsize=16)
    plt.ylabel(x_label, fontsize=16)
    plt.title(title, fontsize=20, fontweight='bold')

    # Skrytí horní a právé strany grafu
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Přidání popisků hodnot na konci každého sloupce
    for bar, value in zip(bars, x_data):
        plt.text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2, f'{value} {suffix}', va='center')

    plt.tight_layout()


# Funkce pro provádění SQL dotazu a načtení výsledků z databáze
def fetch_query(query, *args):
    try:
        cur.execute(query, *args)
        return cur.fetchall()
    except Exception as e:
        print(f"Error při exekuci dotazu: {e}")


# Funkce pro dotazování na množství surovin v databázi
def query_mnozstvi_suroviny(merna_jednotka):
    # Sestavení SQL dotazu na základě zvolené měrné jednotky
    if merna_jednotka == '':
        query = '''
        SELECT id_suroviny, nazev, zrnitost, mnozstvi, merna_jednotka 
        FROM sklad_surovin
        ORDER BY mnozstvi DESC
        '''
        data = fetch_query(query)
    else:
        query = '''
        SELECT id_suroviny, nazev, zrnitost, mnozstvi, merna_jednotka 
        FROM sklad_surovin
        WHERE merna_jednotka = ?
        ORDER BY mnozstvi DESC
        '''
        data = fetch_query(query, merna_jednotka)

    # Formátování výsledků do JSON-like struktury
    json_data = []
    for row in data:
        formatted_row = {
            "id_suroviny": row[0],
            "nazev": row[1],
            "zrnitost": row[2],
            "mnozstvi_na_sklade": float(row[3]),
            "merna_jednotka" : row[4]
        }
        json_data.append(formatted_row)
    return data, json_data


# Funkce pro dotazování na spotřebu surovin v databázi
def query_spotreba_suroviny(merna_jednotka):
    # Sestavení SQL dotazu pro spotřebu surovin na základě zvolené měrné jednotky
    if merna_jednotka == "kg":
        query = '''
        spotrebova_surovin @p_start_date = ?, @p_end_date = ?, @p_merna_jednotka = ?;
        '''
    elif merna_jednotka == "ks":
        query = '''
        spotrebova_surovin @p_start_date = ?, @p_end_date = ?, @p_merna_jednotka = ?;
        '''
    elif merna_jednotka == "":
        query = '''
        spotrebova_surovin @p_start_date = ?, @p_end_date = ?, @p_merna_jednotka = ?;
        '''
    
    data = fetch_query(query, (START_DATE_STR, END_DATE_STR, merna_jednotka))

    # Formátování výsledků do JSON-like struktury
    json_data = []
    for row in data:
        formatted_row = {
            "id_suroviny": row[0],
            "nazev": row[1],
            "zrnitost": row[2],
            "spotreba_za_mesic": float(row[3]), 
        }
        json_data.append(formatted_row)
    return data, json_data


# Funkce pro vytvoření reportu na množství surovin
def report_mnozstvi_surovin(merna_jednotka, filename):
    data, _ = query_mnozstvi_suroviny(merna_jednotka)
    id = [row[0] for row in data]
    mnozstvi = [float(row[3]) for row in data]
    surovina_name = "krušiva" if merna_jednotka == "kg" else "kbelíků"
    generate_graph(id, mnozstvi, f"Množství {surovina_name} v {merna_jednotka}", "ID suroviny", f"Aktuální množství {surovina_name} na skladě v {merna_jednotka}", merna_jednotka)
    plt.savefig(output_dir / filename)
    

# Funkce pro vytvoření reportu o spotřebě surovin
def report_spotreba_surovin(merna_jednotka, filename):
    data, _ = query_spotreba_suroviny(merna_jednotka)
    id = [row[0] for row in data]
    mnozstvi = [float(row[3]) for row in data]
    surovina_name = "krušiva" if merna_jednotka == "kg" else "kbelíků"
    generate_graph(id, mnozstvi,  f"Spotřebované množství {surovina_name} v {merna_jednotka}", "ID suroviny", f"Spotřeba {surovina_name} v {merna_jednotka} / 30 dní", merna_jednotka)
    plt.savefig(output_dir / filename)


# Funkce pro výpočet zbývajících dnů do vyčerpání zásob
def calculate_days_left(mnozstvi, spotreba):
    if spotreba == 0:
        return float('inf')   
    return round(mnozstvi / spotreba)


# Funkce pro generování doporučení k nákupu surovin na základě zbývajících zásob
def generate_recommendation():
    _, data_spotreba = query_spotreba_suroviny(ALL)
    _, data_mnozstvi = query_mnozstvi_suroviny(ALL)

    spotreba_dict = {item['id_suroviny']: item['spotreba_za_mesic'] for item in data_spotreba}

    recommendations = []
    format_words = ['den', 'dny', 'dní']
    
    for mnozstvi_data in data_mnozstvi:
        mnozstvi = mnozstvi_data['mnozstvi_na_sklade']

        if mnozstvi_data['id_suroviny'] in spotreba_dict.keys():
            spotreba = spotreba_dict[mnozstvi_data['id_suroviny']]
            days_left = calculate_days_left(mnozstvi, spotreba)
          
        if days_left < 10:
            word_index = 0 if days_left == 1 else (1 if days_left < 5 else 2)
            recommendations.append(f"Dokoupit {mnozstvi_data['nazev'].strip()}[{mnozstvi_data['id_suroviny']}], surovina dojde priblizne za {days_left} {format_words[word_index]}.")
    return recommendations


# Funkce pro vytvoření PDF reportu
def create_pdf_report():
    font_color = (64, 64, 64)

    # Uložit všechny vytvořené reporty
    chart_filenames = [str(chart_path) for chart_path in output_dir.glob("*.png")]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)

    # Nadpis
    title = f"Report skladu ze dne {date.today().strftime('%d.%m.%Y')}"
    pdf.set_text_color(*font_color)
    pdf.cell(0, 20, title, align='C', ln=1)

    # Přidání každého reportu do dokumentu
    for chart_filename in chart_filenames:
        pdf.ln(10) 
        pdf.image(chart_filename, x=None, y=None, w=pdf.w - 20, h=0)
  
    # Přidání stránky s doporučením nákupu
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 20, "Doporuceni k nakupu", ln=True)
    recommendations = generate_recommendation()
    pdf.set_font('Arial', 'B', 8)
    pdf.set_text_color(0,0,0)
    for recommendation in recommendations:
        r = str(recommendation).encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 5, txt=r)

    # Uložit pdf
    pdf.output(output_dir / "report_skladu.pdf", "F")


# Funkce pro odeslání reportu emailem
def send_report():
    try:
        # Nastavení emailových adres odesílatele a příjemce
        sender = 'danielkarcz14@gmail.com'
        receiver = 'danielkarcz14@gmail.com'
        subject = 'Report skladových zásob'

        # Vytvoření emailové zprávy za použití MIMEMultipart
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject

        # Vytvoření názvu souboru PDF reportu podle aktuálního data
        filename = f"report_skladu_{today_date.strftime('%d_%m_%Y')}.pdf"

        # Určení cesty k souboru PDF reportu
        pdf_file_path = output_dir / "report_skladu.pdf"

        # Otevření PDF souboru a jeho přidání jako přílohy
        with open(pdf_file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        # Nastavení hlavičky pro připojení souboru jako přílohy
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        message.attach(part)

        # Připojení k SMTP serveru Gmailu a odeslání emailu
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, "rtmw xbtg fqqb nzoy")
        server.sendmail(sender, receiver, message.as_string())
        server.quit() # Odhlášení ze serveru

        # Zalogování úspěšného či chybného odeslání emailu do logovacího systému
        event_logger.log_success(user, os.path.basename(__file__), f"Odeslan email o stavu skladu")
    except smtplib.SMTPException as e:
        event_logger.log_error(user, os.path.basename(__file__), f"chyba pri odesilani emailu o stavu skladu, chyba: {str(e)}")


    
if __name__ == "__main__":
    main()
