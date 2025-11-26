import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restoran_uas"
)
mycursor = mydb.cursor()

class User:
    def __init__(self):
        pass

    def login(self, val1, val2): 
        sql = "SELECT level FROM user WHERE username = %s AND password = %s"
        val = (val1, val2)
        mycursor.execute(sql, val)
        level = mycursor.fetchone()
        if level:
            return str(level[0])
        else:
            return "Gagal" 
        
    def insert(self, val1, val2, val3, val4):
        sql = "INSERT INTO user (username, nama_user, password, level) VALUES (%s, %s, %s, %s)"
        val = (val1, val2, val3, val4)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil ditambahkan...")

    def update(val1, val2, val3, val4): 
        sql = "UPDATE user SET nama_user= %s, password= %s, level = %s WHERE username = %s"
        val = (val1, val2, val3, val4)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil diupdate.")

    def delete(val1):
        sql = "DELETE FROM user WHERE username = %s"
        value = (val1,)
        mycursor.execute(sql, value)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil dihapus")

    def select_all(self):
        sql = "SELECT username, password, nama_user, level FROM user"
        mycursor.execute(sql)
        return mycursor.fetchall()
    
    def select_by_id(val1):
        sql = "SELECT nama_user, username, password, level FROM user WHERE username = %s"
        val = (val1)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        return myresult

    def search(self, keyword):
        sql = """
            SELECT username, password, nama, level 
            FROM user WHERE 
                username LIKE %s OR
                nama_user LIKE %s OR
                level LIKE %s
        """
        val = ("%"+keyword+"%", "%"+keyword+"%", "%"+keyword+"%")
        mycursor.execute(sql, val)
        return mycursor.fetchall()
