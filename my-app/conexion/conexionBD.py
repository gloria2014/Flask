

# Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector


def connectionBD():
    try:
        # connection = mysql.connector.connect(
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            passwd="Estrella.23",
            database="clientealfa2db",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True

        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection


    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")


