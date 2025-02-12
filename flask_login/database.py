import sqlite3

def criar_tabela():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabela()
    print("Banco de dados criado!")
