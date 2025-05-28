from flask import Flask, request
import sqlite3
import hashlib 

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'credenciales.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def gestion_credenciales():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Faltan credenciales", 400
            
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", 
                         (username, password))
            conn.commit()
            return f"Usuario {username} registrado exitosamente", 201
        except sqlite3.IntegrityError:
            return "El usuario ya existe", 400
        finally:
            conn.close()
    
    return '''
        <h1>Sistema de Gestión de Credenciales</h1>
        <form method="POST">
            Usuario: <input type="text" name="username"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Registrar">
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Faltan credenciales", 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", 
                  (username, password))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario:
        return f"Bienvenido {username}", 200
    else:
        return "Credenciales inválidas", 401

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)