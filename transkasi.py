import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restoran_uas"
)
mycursor = mydb.cursor()

class Transaksi:
    def __init__(self, id_transaksi=None, kode_transaksi=None, id_menu=None, qty=0, harga_total=0.0):
        self.id_transaksi = id_transaksi
        self.kode_transaksi = kode_transaksi
        self.id_menu = id_menu
        self.qty = qty
        self.harga_total = harga_total

    def _get_new_kode_transaksi(self):
        sql = "SELECT MAX(kode_transaksi) FROM transaksi"
        mycursor.execute(sql)
        max_kode = mycursor.fetchone()[0]
        return (max_kode or 0) + 1

    def insert_item(self):
        sql = """
        INSERT INTO transaksi (kode_transaksi, id_menu, qty, harga_total, tanggal) 
        VALUES (%s, %s, %s, %s, NOW())
        """
        val = (self.kode_transaksi, self.id_menu, self.qty, self.harga_total)
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            self.id_transaksi = mycursor.lastrowid
            return True
        except Exception as e:
            print(f"[Transaksi] Error INSERT ITEM: {e}")
            return False

    def get_items_by_kode(self, kode):
        sql = """
        SELECT t.id_transaksi, t.kode_transaksi, m.nama, t.qty, t.harga_total
        FROM transaksi t
        JOIN menu m ON t.id_menu = m.id
        WHERE t.kode_transaksi = %s
        ORDER BY t.id_transaksi
        """
        mycursor.execute(sql, (kode,))
        return mycursor.fetchall()

    def calculate_grand_total(self, kode):
        sql = "SELECT SUM(harga_total) FROM transaksi WHERE kode_transaksi = %s"
        mycursor.execute(sql, (kode,))
        total = mycursor.fetchone()[0]
        return total or 0