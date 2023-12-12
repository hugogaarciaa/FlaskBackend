from flask import Flask, jsonify
import mysql.connector
from flask import request

app = Flask(__name__)

mysql = mysql.connector.connect(host="localhost", user="root", passwd="", database="jmh")
cursor = mysql.cursor()

@app.route('/usuarios', methods=['GET'])
def getUsuarios():
    global mysql

    cursor.execute("SELECT * FROM usuarios")
    result = cursor.fetchall()

    return jsonify({'usuarios': result})

@app.route('/usuarios/<int:id>', methods=['GET'])
def getUsuario(id):
    global mysql

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    result = cursor.fetchall()

    return jsonify({'usuario': result})

@app.route('/usuarios', methods=['POST'])
def addUsuario():
    global mysql

    ids = request.json['ids']
    nombre = request.json['nombre']
    passw = request.json['passw']

    cursor.execute("INSERT INTO usuarios (id, usuario, contrasena) VALUES (%s, %s, %s)", (ids, nombre, passw))
    mysql.commit()

    return jsonify({'status': 'Usuario agregado'})
@app.route('/usuarios/<int:id>', methods=['PUT'])
def updateUsuario(id):
    global mysql

    nombre = request.json['nombre']
    passw = request.json['passw']

    cursor.execute("UPDATE usuarios SET usuario = %s, contrasena = %s WHERE id = %s", (nombre, passw, id))
    mysql.commit()

    return jsonify({'status': 'Usuario actualizado'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deleteUsuario(id):
    global mysql

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    mysql.commit()

    return jsonify({'status': 'Usuario eliminado'})

@app.route('/login', methods=['POST'])
def login():
    global mysql

    nombre = request.json['nombre']
    passw = request.json['passw']

    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s", (nombre, passw))
    result = cursor.fetchall()

    if result:
        return jsonify({'status': 'Acceso concedido'})
    else:
        return jsonify({'status': 'Acceso denegado'})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
