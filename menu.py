import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restoran_uas"
)
mycursor = mydb.cursor()



class Menu:
    def __init__(self, id_menu, nama, harga, stok):
        self.id_menu = id_menu
        self.nama = nama
        self.harga = harga
        self.stok = stok
    
    def _insert_menu_data(self):
        sql = "INSERT INTO menu (nama, harga, stok) VALUES (%s, %s, %s)"
        val = (self.nama, self.harga, self.stok) 
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            new_id = mycursor.lastrowid 
            self.id_menu = new_id 
            return new_id
        except Exception as e:
            print(f"[Menu] Error INSERT: {e}")
            return False
        
    def update_data(self):
        sql = "UPDATE menu SET nama=%s, harga=%s, stok=%s WHERE id=%s"
        val = (self.nama, self.harga, self.stok, self.id_menu)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, f"Data menu ID {self.id_menu} berhasil diupdate.")

    def delete_data(self):
        sql = "DELETE FROM menu WHERE id = %s"
        val = (self.id_menu,)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, f"Data menu ID {self.id_menu} berhasil dihapus (CASCADE).")

    def select_all_data(self):
        from makanan import Makanan
        from minuman import Minuman
        
        sql = """
        SELECT m.id, m.nama, m.harga, m.stok, a.kategori_makanan, b.jenis_penyajian
        FROM menu m
        LEFT JOIN makanan a ON m.id = a.id
        LEFT JOIN minuman b ON m.id = b.id
        """
        mycursor.execute(sql)
        results = mycursor.fetchall()
        
        menu_list = []
        for row in results:
            id, nama, harga, stok, kategori, penyajian = row
            if kategori:
                menu_list.append(Makanan(id, nama, harga, stok, kategori))
            elif penyajian:
                menu_list.append(Minuman(id, nama, harga, stok, penyajian))
        return menu_list
    

