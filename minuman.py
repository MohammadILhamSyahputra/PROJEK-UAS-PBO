import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restoran_uas"
)
mycursor = mydb.cursor()

from menu import Menu

class Minuman(Menu):
    def __init__(self, id_menu, nama, harga, stok, penyajian):
        super().__init__(id_menu, nama, harga, stok)
        self.jenis_penyajian = penyajian

    def insert_kategori(self):
        new_id = super()._insert_menu_data()
        
        if new_id:
            sql = "INSERT INTO minuman (id, jenis_penyajian) VALUES (%s, %s)"
            val = (new_id, self.jenis_penyajian) 
            try:
                mycursor.execute(sql, val)
                mydb.commit()
                print(f"[Minuman] Data spesifik ID {new_id} berhasil disimpan.")
            except Exception as e:
                print(f"[Minuman] Error INSERT spesifik: {e}")

    def select_by_id(self):
        sql = """
            SELECT m.id, m.nama, m.harga, m.stok, b.jenis_penyajian
            FROM menu m INNER JOIN minuman b ON m.id = b.id
            WHERE m.id = %s
        """
        mycursor.execute(sql, (self.id_menu,))
        row = mycursor.fetchone()
        
        if row:
            return Minuman(row[0], row[1], row[2], row[3], row[4])
        return None
        
    def update_penyajian(self):
        sql = "UPDATE minuman SET jenis_penyajian=%s WHERE id=%s"
        val = (self.jenis_penyajian, self.id_menu)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, f"Jenis penyajian ID {self.id_menu} berhasil diupdate.")























    # def display_detail(self):
    #     print(f"🍹 MINUMAN | ID: {self.id_menu} | Nama: {self.nama} | Harga: {self.harga}")
    #     print(f"  Stok: {self.stok} | Penyajian: {self.jenis_penyajian}")