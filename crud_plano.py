import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo oculto .env
load_dotenv()

def get_connection():
    """Establece y retorna la conexion fisica con la base de datos Sakila local de forma segura."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error critico de conexion a la base de datos: {e}")
        return None
# =====================================================================
# OPERACIONES CRUD: ENTIDAD COUNTRY (Pais)
# =====================================================================

def create_country(country_name):
    """Inserta un nuevo pais en la tabla country."""
    query = "INSERT INTO country (country) VALUES (%s)"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (country_name,))
            conn.commit()
            print(f"Country Creado: {country_name} (ID: {cursor.lastrowid})")
            return cursor.lastrowid
        except Error as e:
            print(f"Error al crear country: {e}")
        finally:
            cursor.close()
            conn.close()
    return None

def read_country(country_id):
    """Busca y retorna un pais especifico por su ID."""
    query = "SELECT country_id, country, last_update FROM country WHERE country_id = %s"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (country_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al leer country: {e}")
        finally:
            cursor.close()
            conn.close()
    return None

def update_country(country_id, new_name):
    """Actualiza el nombre de un pais existente."""
    query = "UPDATE country SET country = %s WHERE country_id = %s"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (new_name, country_id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Country ID {country_id} actualizado a {new_name}.")
                return True
        except Error as e:
            print(f"Error al actualizar country: {e}")
        finally:
            cursor.close()
            conn.close()
    return False

def delete_country(country_id):
    """Elimina un pais por su ID."""
    query = "DELETE FROM country WHERE country_id = %s"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (country_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Country ID {country_id} eliminado correctamente.")
                return True
        except Error as e:
            print(f"Error al eliminar country (Restriccion FK): {e}")
        finally:
            cursor.close()
            conn.close()
    return False


# =====================================================================
# OPERACIONES CRUD: ENTIDAD CITY (Ciudad)
# =====================================================================

def create_city(city_name, country_id):
    """Inserta una nueva ciudad vinculada a un pais existente."""
    query = "INSERT INTO city (city, country_id) VALUES (%s, %s)"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (city_name, country_id))
            conn.commit()
            print(f"City Creada: {city_name} asignada al Pais ID: {country_id} (ID Ciudad: {cursor.lastrowid})")
            return cursor.lastrowid
        except Error as e:
            print(f"Error al crear city: {e}")
        finally:
            cursor.close()
            conn.close()
    return None

def read_city(city_id):
    """Retorna una ciudad con el nombre de su pais mediante un JOIN."""
    query = """
        SELECT c.city_id, c.city, c.country_id, co.country AS country_name, c.last_update 
        FROM city c
        JOIN country co ON c.country_id = co.country_id
        WHERE c.city_id = %s
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (city_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al leer city: {e}")
        finally:
            cursor.close()
            conn.close()
    return None

def update_city(city_id, new_city_name, new_country_id):
    """Actualiza el nombre y/o el pais de una ciudad."""
    query = "UPDATE city SET city = %s, country_id = %s WHERE city_id = %s"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (new_city_name, new_country_id, city_id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"City ID {city_id} actualizada con exito.")
                return True
        except Error as e:
            print(f"Error al actualizar city: {e}")
        finally:
            cursor.close()
            conn.close()
    return False

def delete_city(city_id):
    """Elimina una ciudad por su ID."""
    query = "DELETE FROM city WHERE city_id = %s"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (city_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"City ID {city_id} eliminada correctamente.")
                return True
        except Error as e:
            print(f"Error al eliminar city: {e}")
        finally:
            cursor.close()
            conn.close()
    return False


# =====================================================================
# OPERACIONES CRUD: ENTIDAD FILM (Pelicula)
# =====================================================================

def create_film(title, description, release_year, language_id, rental_duration, rental_rate, replacement_cost):
    """Inserta una pelicula validando sus campos obligatorios e integridad."""
    query = """
        INSERT INTO film (title, description, release_year, language_id, rental_duration, rental_rate, replacement_cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (title, description, release_year, language_id, rental_duration, rental_rate, replacement_cost))
            conn.commit()
            print(f"Film Creada: {title} (ID Pelicula: {cursor.lastrowid})")
            return cursor.lastrowid
        except Error as e:
            print(f"Error al crear film: {e}")
        finally:
            cursor.close()
            conn.close()
    return None

def read_film(film_id):
    """Busca una pelicula especifica por su ID."""
    query = "SELECT film_id, title, description, release_year, rental_rate, replacement_cost FROM film WHERE film_id = %s"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (film_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al leer film: {e}")
        finally:
            cursor.close()
            conn.close()
    return None

def update_film(film_id, new_title, new_rental_rate):
    """Modifica el titulo y la tarifa de renta de una pelicula."""
    query = "UPDATE film SET title = %s, rental_rate = %s WHERE film_id = %s"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (new_title, new_rental_rate, film_id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Film ID {film_id} actualizada correctamente.")
                return True
        except Error as e:
            print(f"Error al actualizar film: {e}")
        finally:
            cursor.close()
            conn.close()
    return False

def delete_film(film_id):
    """Elimina una pelicula por su ID."""
    query = "DELETE FROM film WHERE film_id = %s"
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (film_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Film ID {film_id} eliminada correctamente.")
                return True
        except Error as e:
            print(f"Error al eliminar film: {e}")
        finally:
            cursor.close()
            conn.close()
    return False


# =====================================================================
# PRUEBAS UNITARIAS
# =====================================================================

""" if __name__ == "__main__":
    print("Iniciando Suite de Pruebas CRUD Integrado")
    print("----------------------------------------")
    
    id_pais = create_country("Dominican Republic Test")
    
    if id_pais:
        id_ciudad = create_city("Santo Domingo Centro", id_pais)
        
        if id_ciudad:
            ciudad_info = read_city(id_ciudad)
            print(f"Lectura de datos relacionales: {ciudad_info}")
            
            update_city(id_ciudad, "Santo Domingo Este", id_pais)
            delete_city(id_ciudad)
            
        delete_country(id_pais)
        print("----------------------------------------")
        
    id_pelicula = create_film(
        title="AUTOMATION PIPELINE DATA", 
        description="Industrial Optimization Overview", 
        release_year=2026, 
        language_id=1, 
        rental_duration=5, 
        rental_rate=4.99, 
        replacement_cost=19.99
    )
    
    if id_pelicula:
        film_info = read_film(id_pelicula)
        print(f"Datos de Pelicula en BD: {film_info}")
        
        update_film(id_pelicula, "AUTOMATION PIPELINE V2", 5.99)
        delete_film(id_pelicula)
        print("----------------------------------------")
        
    print("Suite de validacion en vivo finalizada.")"""

if __name__ == "__main__":
    print("Iniciando Suite de Pruebas CRUD Integrado")
    print("----------------------------------------")
    
    # 1. PASO DE INSERCIÓN: Crear un nuevo país de prueba
    id_pais = create_country("Dominican Republic Test")
    
    if id_pais:
        # 2. PASO DE AUDITORÍA INTERMEDIA: Buscar e imprimir el país antes de alterarlo
        print("\n[AUDITORÍA EN VIVO] Buscando país recién insertado...")
        pais_info = read_country(id_pais)
        print(f"-> EVIDENCIA EN BD (PAÍS): {pais_info}")
        print("----------------------------------------")
        
        # 3. PASO DE INSERCIÓN RELACIONAL: Crear la ciudad vinculada al país
        id_ciudad = create_city("Santo Domingo Centro", id_pais)
        
        if id_ciudad:
            # 4. PASO DE AUDITORÍA INTERMEDIA: Buscar e imprimir la ciudad con su JOIN relacional
            print("\n[AUDITORÍA EN VIVO] Buscando ciudad mediante JOIN relacional...")
            ciudad_info = read_city(id_ciudad)
            print(f"-> EVIDENCIA EN BD (CIUDAD): {ciudad_info}")
            print("----------------------------------------")
            
            # 5. PASO DE ACTUALIZACIÓN: Modificar datos y validar persistencia
            print("\nEjecutando actualización de datos...")
            update_city(id_ciudad, "Santo Domingo Este", id_pais)
            
            # Volver a leer para confirmar la actualización en pantalla
            ciudad_actualizada = read_city(id_ciudad)
            print(f"-> EVIDENCIA DE ACTUALIZACIÓN: {ciudad_actualizada}")
            print("----------------------------------------")
            
            # 6. PASO DE LIMPIEZA AUTOMÁTICA (CICLO SEGURO)
            print("\nIniciando remoción segura de registros de prueba...")
            delete_city(id_ciudad)
            
        delete_country(id_pais)
        print("----------------------------------------")
        
    # --- PRUEBA INDEPENDIENTE: ENTIDAD FILM ---
    id_pelicula = create_film(
        title="AUTOMATION PIPELINE DATA", 
        description="Industrial Optimization Overview", 
        release_year=2026, 
        language_id=1, 
        rental_duration=5, 
        rental_rate=4.99, 
        replacement_cost=19.99
    )
    
    if id_pelicula:
        print("\n[AUDITORÍA EN VIVO] Buscando película en el catálogo de inventario...")
        film_info = read_film(id_pelicula)
        print(f"-> EVIDENCIA EN BD (FILM): {film_info}")
        print("----------------------------------------")
        
        print("\nEjecutando actualización de tarifa...")
        update_film(id_pelicula, "AUTOMATION PIPELINE V2", 5.99)
        
        film_actualizada = read_film(id_pelicula)
        print(f"-> EVIDENCIA DE ACTUALIZACIÓN (FILM): {film_actualizada}")
        print("----------------------------------------")
        
        print("\nIniciando remoción segura de película de prueba...")
        delete_film(id_pelicula)
        print("----------------------------------------")
        
    print("Suite de validacion en vivo finalizada.")