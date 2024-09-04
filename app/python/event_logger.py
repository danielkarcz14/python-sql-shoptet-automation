class EventLogger:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def log_success(self, user, script_name, description):
        self._log_event(user, script_name, description, 'SUCCESS')

    def log_error(self, user, script_name, description):
        self._log_event(user, script_name, description, 'ERROR')

    def _log_event(self, user, script_name, description, state):
        try:
            self.cur.execute("""
                INSERT INTO zaznamy_udalosti (uzivatel, skript, popis, stav)
                VALUES (?, ?, ?, ?)
            """, (user, script_name, description, state))
            self.conn.commit()
        except Exception as e:
            print(f"Chyba při zápisu události do databáze: {e}")
