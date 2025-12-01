import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restoran_uas"
)
mycursor = mydb.cursor()

class User:
    def __init__(self, username=None, nama=None, password=None, level=None):
        self.username = username
        self.nama = nama
        self.password = password
        self.level = level

    def login(self, username, password):
        sql = "SELECT level FROM user WHERE username = %s AND password = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result:
            return str(result[0])
        else:
            return "Gagal"

    def insert(self):
        sql = "INSERT INTO user (username, nama_user, password, level) VALUES (%s, %s, %s, %s)"
        val = (self.username, self.nama, self.password, self.level)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil ditambahkan...")

    def update(self, nama, password, level, username):
        sql = "UPDATE user SET nama_user = %s, password = %s, level = %s WHERE username = %s"
        val = (nama, password, level, username)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil diupdate.")

    def delete(self, username):
        sql = "DELETE FROM user WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil dihapus.")

    def select_all(self):
        sql = "SELECT username, nama_user, password, level FROM user"
        mycursor.execute(sql)
        return mycursor.fetchall()

    def select_by_id(self, username):
        sql = "SELECT nama_user, username, password, level FROM user WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        return mycursor.fetchone()

    def search(self, keyword):
        sql = """
            SELECT username, nama_user, password, level 
            FROM user 
            WHERE username LIKE %s 
               OR nama_user LIKE %s 
               OR level LIKE %s
        """
        val = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        mycursor.execute(sql, val)
        return mycursor.fetchall()
