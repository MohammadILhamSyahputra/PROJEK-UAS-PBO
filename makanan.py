import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restoran_uas"
)
mycursor = mydb.cursor()

from menu import Menu

class Makanan(Menu):
    def __init__(self, id_menu, nama, harga, stok, kategori):
        super().__init__(id_menu, nama, harga, stok)
        self.kategori_makanan = kategori

    def insert_kategori(self):
        new_id = super()._insert_menu_data()
        
        if new_id:
            sql = "INSERT INTO makanan (id, kategori_makanan) VALUES (%s, %s)"
            val = (new_id, self.kategori_makanan) 
            try:
                mycursor.execute(sql, val)
                mydb.commit()
                print(f"[Makanan] Data spesifik ID {new_id} berhasil disimpan.")
            except Exception as e:
                print(f"[Makanan] Error INSERT spesifik: {e}")

    def select_by_id(self):
        sql = """
            SELECT m.id, m.nama, m.harga, m.stok, a.kategori_makanan
            FROM menu m INNER JOIN makanan a ON m.id = a.id
            WHERE m.id = %s
        """
        mycursor.execute(sql, (self.id_menu,))
        row = mycursor.fetchone()
        
        if row:
            return Makanan(row[0], row[1], row[2], row[3], row[4])
        return None
    
    def update_kategori(self):
        sql = "UPDATE makanan SET kategori_makanan=%s WHERE id=%s"
        val = (self.kategori_makanan, self.id_menu)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, f"Kategori makanan ID {self.id_menu} berhasil diupdate.")






























    # def display_detail(self):
    #     print(f"🍽️ MAKANAN | ID: {self.id_menu} | Nama: {self.nama} | Harga: {self.harga}")
    #     print(f"  Stok: {self.stok} | Kategori: {self.kategori_makanan}")