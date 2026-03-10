import sqlite3


class Dbase:
    def __init__(self, path):
        self.path = path
        self.con = None
        self.cur = None
        self._connect()

    def _connect(self):
        """Создаёт новое соединение для текущего потока"""
        self.con = sqlite3.connect(self.path, check_same_thread=False)
        self.cur = self.con.cursor()

    def createNewAppointment(self, clientId, date, time):
        if self.cur.execute("""SELECT (id) FROM appointments WHERE date = ? AND time = ?""", (date, time)).fetchone():
            return -1
        self.cur.execute("""INSERT INTO appointments(clientId, date, time) VALUES(?, ?, ?)""", (clientId, date, time))
        self.con.commit()
        return self.cur.execute("""SELECT (id) FROM appointments WHERE clientId = ?""", (clientId,)).fetchall()[-1][0]

    def getAppointment(self, idAppoinmtnet):
        return self.cur.execute("""SELECT * FROM appointments WHERE id = ?""", (idAppoinmtnet,)).fetchone()

    def getAppointments(self):
        return self.cur.execute("""SELECT * FROM appointments""").fetchall()

    def getClient(self, idClient):
        return self.cur.execute("""SELECT * FROM clients WHERE id = ?""", (idClient,)).fetchone()

    def newClient(self, clientName, clientSurName):
        self._connect()
        if self.cur.execute("""SELECT id FROM clients WHERE name = ? AND surname = ?""", (clientName, clientSurName)).fetchone():
            return -1
        self.cur.execute("""INSERT INTO clients(name, surname) VALUES(?, ?)""", (clientName, clientSurName))
        self.con.commit()
        # Исправлено: получаем последний добавленный id
        return self.cur.lastrowid

    def update_status(self, appointmentId, status):
        self.cur.execute("""UPDATE appointments SET status = ? WHERE id = ?""", (status, appointmentId))
        self.con.commit()

def get_db():
    db = Dbase('./db.sqlite')
    return db


# if __name__ ==