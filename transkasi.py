import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restoran_uas"
)
mycursor = mydb.cursor()

class Transaksi:
    def __init__(self, id_transaksi=None, kode_transaksi=None, id_menu=None, username_kasir=None, qty=0, harga_total=0.0):
        self.id_transaksi = id_transaksi
        self.kode_transaksi = kode_transaksi
        self.id_menu = id_menu
        self.username_kasir = username_kasir
        self.qty = qty
        self.harga_total = harga_total

    def _get_new_kode_transaksi(self):
        sql = "SELECT MAX(kode_transaksi) FROM transaksi"
        mycursor.execute(sql)
        max_kode = mycursor.fetchone()[0]
        return (max_kode or 0) + 1

    def insert_item(self):
        sql = """
        INSERT INTO transaksi (kode_transaksi, id_menu, username_kasir, qty, harga_total, tanggal) 
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        val = (self.kode_transaksi, self.id_menu, self.username_kasir, self.qty, self.harga_total)
        
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
    
    def get_riwayat_by_kasir(self, username, tgl_awal, tgl_akhir):
        """Mengambil detail transaksi oleh kasir dalam rentang tanggal."""
        # Query ini akan mengembalikan setiap item yang dibeli
        sql = """
        SELECT 
            t.id_transaksi,
            t.kode_transaksi,
            m.nama AS nama_menu,        -- Ambil Nama Menu dari tabel menu
            t.username_kasir,
            t.qty,
            t.harga_total,
            t.tanggal
        FROM transaksi t
        JOIN menu m ON t.id_menu = m.id
        WHERE t.username_kasir = %s
          AND t.tanggal >= %s 
          AND t.tanggal < %s
        ORDER BY t.tanggal DESC
        """
        # Kita menggunakan GROUP BY kode_transaksi karena satu kode mewakili satu nota
        mycursor.execute(sql, (username, tgl_awal, tgl_akhir))
        return mycursor.fetchall()
    
    def calculate_total_riwayat(self, username, tgl_awal, tgl_akhir):
        """Menghitung total keseluruhan transaksi oleh kasir dalam rentang tanggal."""
        sql = """
        SELECT SUM(harga_total)
        FROM transaksi
        WHERE username_kasir = %s
        AND tanggal >= %s 
        AND tanggal < %s
        """
        mycursor.execute(sql, (username, tgl_awal, tgl_akhir))
        result = mycursor.fetchone()
        return result[0] or 0
    
    def get_all_kasir_usernames(self):
        """Mengambil daftar unik semua username kasir dari tabel transaksi."""
        # Note: Menggunakan DISTINCT agar nama kasir tidak double
        sql = "SELECT DISTINCT username_kasir FROM transaksi ORDER BY username_kasir"
        mycursor.execute(sql)
        # Mengembalikan list of strings: ['Ilham', 'Budi', ...]
        return [row[0] for row in mycursor.fetchall()]
    
    def get_riwayat_admin(self, username_filter, tgl_awal, tgl_akhir):
        """Mengambil detail transaksi (grup per nota) untuk admin (filter oleh kasir atau semua)."""
        
        # NOTE: Kita menggunakan GROUP BY di sini untuk menampilkan NOTA per baris (Kode Transaksi, Tanggal, Total Nota)
        # BUKAN detail item per baris.
        sql = """
        SELECT 
            t.id_transaksi,
            t.kode_transaksi,
            m.nama AS nama_menu,        -- Kolom 2: Nama Menu (dari JOIN)
            t.username_kasir,
            t.qty,
            t.harga_total,
            t.tanggal                   -- Kolom 6: Tanggal Lengkap
        FROM transaksi t
        JOIN menu m ON t.id_menu = m.id
        WHERE t.tanggal >= %s AND t.tanggal < %s
        """
        params = [tgl_awal, tgl_akhir]
        
        # Tambahkan filter username_kasir HANYA jika bukan "ALL"
        if username_filter != "ALL":
            sql += " AND t.username_kasir = %s"
            params.append(username_filter)
            
        sql += " ORDER BY t.tanggal DESC"
        
        mycursor.execute(sql, tuple(params))
        return mycursor.fetchall()


    def calculate_total_admin(self, username, tgl_awal, tgl_akhir):
        """Menghitung total keseluruhan transaksi (filter opsional)."""
        base_sql = "SELECT SUM(harga_total) FROM transaksi WHERE tanggal >= %s AND tanggal < %s"
        params = [tgl_awal, tgl_akhir]

        if username != "ALL":
            base_sql += " AND username_kasir = %s"
            params.append(username)
            
        mycursor.execute(base_sql, tuple(params))
        result = mycursor.fetchone()
        return result[0] or 0