import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# 1. Configuración dinámica y portable del entorno
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Subimos un nivel ("..") porque dbcontext.py está dentro de la subcarpeta Scripts_FaseII/
dotenv_path = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

class DbContext:
    """
    Componente centralizado de infraestructura de datos (ORM Nativo).
    Gestiona el ciclo de vida de las conexiones y transacciones a MySQL de forma segura.
    """
    def __init__(self) -> None:
        # Extraemos las credenciales del .env cargado dinámicamente
        self.host: str = os.getenv("DB_HOST", "localhost")
        self.user: str = os.getenv("DB_USER")
        self.password: str = os.getenv("DB_PASSWORD")
        self.database: str = os.getenv("DB_NAME", "sakila")
        self._connection = None

    def __enter__(self):
        """Inicializa la conexión al entrar al bloque 'with' (Context Manager)."""
        try:
            self._connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self
        except Error as e:
            print(f"Error crítico de infraestructura al conectar a la BD: {e}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Asegura el cierre de recursos al salir del bloque 'with', manejando transacciones."""
        if self._connection and self._connection.is_connected():
            if exc_type is not None:
                # Si hubo algún error en la ejecución del bloque, aplico un Rollback de seguridad
                print(f"Detectada anomalía en la ejecución. Aplicando Rollback de transacción...")
                self._connection.rollback()
            else:
                # Si todo fue exitoso, consolido los cambios en el disco (Commit)
                self._connection.commit()
            
            # Libero el puerto y cerramos la conexión de forma segura
            self._connection.close()
        
        # Devolvemos False para permitir que las excepciones fluyan si no fueron controladas antes
        return False

    def execute_query(self, sql: str, params: tuple = None) -> list:
        """Ejecuta consultas de lectura (SELECT) y devuelve un mapa estructurado de datos (Diccionario)."""
        if not self._connection or not self._connection.is_connected():
            raise Error("No hay una conexión activa con la base de datos.")
        
        cursor = self._connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
        finally:
            cursor.close()

    def execute_non_query(self, sql: str, params: tuple = None) -> int:
        """Ejecuta sentencias de escritura (INSERT, UPDATE, DELETE) y devuelve las filas afectadas."""
        if not self._connection or not self._connection.is_connected():
            raise Error("No hay una conexión activa con la base de datos.")
        
        cursor = self._connection.cursor()
        try:
            cursor.execute(sql, params or ())
            return cursor.rowcount
        finally:
            cursor.close()