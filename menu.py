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
        menu_id = self.id_menu
        val = (menu_id,)
        
        try:
            sql_makanan = "DELETE FROM makanan WHERE id = %s"
            mycursor.execute(sql_makanan, val)

            sql_minuman = "DELETE FROM minuman WHERE id = %s"
            mycursor.execute(sql_minuman, val)

            sql_menu = "DELETE FROM menu WHERE id = %s"
            mycursor.execute(sql_menu, val)
            
            mydb.commit()
            
            print(f"Data menu ID {menu_id} berhasil dihapus dari semua tabel secara manual.")

        except Exception as e:
            mydb.rollback()
            print(f"[Menu] Error DELETE: Gagal menghapus data ID {menu_id}: {e}")

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
    

    def select_by_name(self):
        sql = "SELECT id, nama FROM menu WHERE id = %s"
        
        try:
            mycursor.execute(sql, (self.id_menu,))
            row = mycursor.fetchone()
            
            if row:
                return row 
            return None
        except Exception as e:
            print(f"[Menu] Error SELECT basic data: {e}")
            return None
        
    def search_menu_by_name(self, nama_keyword): # self DITAMBAHKAN
        """Mencari menu di tabel menu berdasarkan nama keyword."""
        # Menggunakan LIKE untuk pencarian yang fleksibel
        sql = "SELECT id, nama, harga, stok FROM menu WHERE nama LIKE %s"
        # Tambahkan wildcard % di awal dan akhir keyword
        mycursor.execute(sql, ('%' + nama_keyword + '%',))
        return mycursor.fetchall()

    # 2. get_harga_menu_by_id (Menjadi Metode Instance)
    def get_harga_menu_by_id(self, menu_id): # self DITAMBAHKAN
        """Mengambil harga satuan dari menu berdasarkan ID."""
        sql = "SELECT harga FROM menu WHERE id = %s"
        mycursor.execute(sql, (menu_id,))
        result = mycursor.fetchone()
        return result[0] if result else 0

