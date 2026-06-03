import csv
import json
from crud_plano import get_connection

# =====================================================================
# UTILERÍA DE METADATOS (Mapeo de Columnas)
# =====================================================================

def get_table_columns(table_name):
    """Consulta la base de datos para obtener la lista de columnas de una tabla."""
    conn = get_connection()
    if not conn: return []
    
    columns = []
    try:
        cursor = conn.cursor()
        # Consultamos el esquema de información de la tabla seleccionada
        cursor.execute(f"DESCRIBE {table_name}")
        # El primer elemento de cada fila devuelta por DESCRIBE es el nombre de la columna
        columns = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error al obtener las columnas de la tabla '{table_name}': {e}")
    finally:
        cursor.close()
        conn.close()
    return columns

# =====================================================================
# MÓDULO EXPORTACIÓN (Base de Datos -> Archivo)
# =====================================================================

def export_table_to_csv(table_name, csv_filename):
    """Extrae el contenido de cualquier tabla de Sakila y lo exporta a un CSV."""
    conn = get_connection()
    if not conn: return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print(f"La tabla '{table_name}' está vacía o no tiene registros.")
            return False
            
        headers = list(rows[0].keys())
        
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
            
        print(f"Exportación Exitosa: Tabla '{table_name}' guardada en '{csv_filename}'")
        return True
    except Exception as e:
        print(f"Error al exportar a CSV la tabla '{table_name}': {e}")
    finally:
        cursor.close()
        conn.close()
    return False

def export_table_to_json(table_name, json_filename):
    """Extrae el contenido de cualquier tabla de Sakila y lo guarda en formato JSON."""
    conn = get_connection()
    if not conn: return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print(f"La tabla '{table_name}' está vacía o no tiene registros.")
            return False
            
        # Manejo de tipos de datos no serializables en JSON (Fechas, Decimales y Conjuntos)
        for row in rows:
            for key, value in row.items():
                if isinstance(value, set):  
                    row[key] = list(value)  
                elif hasattr(value, 'isoformat'): 
                    row[key] = value.isoformat()
                elif hasattr(value, 'to_eng_string') or type(value).__name__ == 'Decimal':
                    row[key] = float(value)
                    
        with open(json_filename, mode='w', encoding='utf-8') as file:
            json.dump(rows, file, indent=4, ensure_ascii=False)
            
        print(f"Exportación Exitosa: Tabla '{table_name}' guardada en '{json_filename}'")
        return True
    except Exception as e:
        print(f"Error al exportar a JSON la tabla '{table_name}': {e}")
    finally:
        cursor.close()
        conn.close()
    return False

# =====================================================================
# MÓDULO IMPORTACIÓN (Archivo -> Base de Datos)
# =====================================================================

def import_table_from_json(json_filename, table_name, column_name):
    """
    Lee un archivo JSON de forma genérica e inserta sus datos de forma masiva 
    en la tabla y columna indicadas por parámetros.
    """
    conn = get_connection()
    if not conn: return False
    
    try:
        with open(json_filename, mode='r', encoding='utf-8') as file:
            data_list = json.load(file)
            
        if not data_list:
            print(f"El archivo '{json_filename}' está vacío.")
            return False
            
        cursor = conn.cursor()
        query = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
        
        # Mapeo genérico leyendo la llave provista por parámetro desde el JSON
        data_to_insert = [(item[column_name],) for item in data_list if column_name in item]
        
        if not data_to_insert:
            print(f"No se encontraron campos con la columna '{column_name}' en el archivo JSON.")
            return False
            
        cursor.executemany(query, data_to_insert)
        conn.commit()
        print(f"Importación Completada: Se insertaron {cursor.rowcount} registros en la tabla '{table_name}' desde JSON.")
        return True
    except Exception as e:
        print(f"Error al importar masivamente a la tabla '{table_name}': {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        conn.close()
    return False

# =====================================================================
# INTERFAZ DE USUARIO INTERACTIVA EN CONSOLA (Poka-Yoke / Anti-Errores)
# =====================================================================

if __name__ == "__main__":
    print("========================================================")
    print("  PRODINTDATA - Módulo Interactivo de Entrada/Salida")
    print("========================================================")
    
    # 1. Menú interactivo de Exportación a CSV
    print("\n--- PASO 1: EXPORTACIÓN A CSV ---")
    tabla_csv = input("Ingrese el nombre de la tabla que desea exportar a CSV (ej. country, city, film): ").strip().lower()
    if tabla_csv:
        ruta_csv = f"data/{tabla_csv}_exported.csv"
        export_table_to_csv(tabla_csv, ruta_csv)
        
    # 2. Menú interactivo de Exportación a JSON
    print("\n--- PASO 2: EXPORTACIÓN A JSON ---")
    tabla_json = input("Ingrese el nombre de la tabla que desea exportar a JSON (ej. film, customer): ").strip().lower()
    if tabla_json:
        ruta_json = f"data/{tabla_json}_exported.json"
        export_table_to_json(tabla_json, ruta_json)
        
    # 3. Menú interactivo de Importación Genérica desde JSON (Con Selección Numérica)
    print("\n--- PASO 3: IMPORTACIÓN MASIVA DESDE JSON ---")
    ejecutar_import = input("¿Desea realizar una prueba de importación masiva desde un archivo JSON? (s/n): ").strip().lower()
    
    if ejecutar_import == 's':
        archivo_imp = input("Ingrese la ruta del archivo JSON a importar (ej. data/countries_to_import.json): ").strip()
        tabla_imp = input("¿A qué tabla de la base de datos se van a ingresar los datos? (ej. country, city): ").strip().lower()
        
        # Obtenemos dinámicamente las columnas reales de la tabla destino
        columnas_disponibles = get_table_columns(tabla_imp)
        
        if columnas_disponibles:
            print(f"\n Columnas disponibles en la tabla '{tabla_imp}':")
            # Enumeramos cada columna partiendo desde el índice 1
            for idx, col in enumerate(columnas_disponibles, start=1):
                print(f"  [{idx}] -> {col}")
                
            try:
                seleccion = int(input(f"\nSeleccione el número de la columna destino (1-{len(columnas_disponibles)}): "))
                
                # Validamos que el número ingresado esté en el rango correcto
                if 1 <= seleccion <= len(columnas_disponibles):
                    columna_final = columnas_disponibles[seleccion - 1]
                    print(f"✔️ Selección validada: Se utilizará la columna '{columna_final}'")
                    
                    # Ejecutamos la importación con los datos validados
                    import_table_from_json(archivo_imp, tabla_imp, columna_final)
                else:
                    print("Error: El número ingresado está fuera del rango de opciones.")
            except ValueError:
                print("Error: Debe ingresar un número entero válido.")
        else:
            print(f"No se pudieron recuperar columnas. Verifique que la tabla '{tabla_imp}' exista.")

    print("\n========================================================")
    print("  Operaciones finalizadas. Proceso bajo control.")
    print("========================================================")