import sqlite3

conexao = sqlite3.connect("sistema.db")
cursor = conexao.cursor()

cursor.execute("SELECT * FROM usuarios")

for usuario in cursor.fetchall():
    print(usuario)

conexao.close()