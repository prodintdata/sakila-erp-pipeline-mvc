## pip install mysql-connector-python ##

import math
import mysql.connector
from mysql.connector import Error

# Reutilizamos la funcion de conexion desde el crud plano local
from crud_plano import get_connection

# =====================================================================
# ALGORITMOS ESTADISTICOS EN PYTHON PURO (Sin librerias externas)
# =====================================================================

def calc_mean(data):
    """Calcula la media aritmetica."""
    if not data: return 0
    return sum(data) / len(data)

def calc_range(data):
    """Calcula el rango (Maximo - Minimo)."""
    if not data: return 0
    return max(data) - min(data)

def calc_variance(data):
    """Calcula la varianza muestral (n - 1)."""
    if len(data) < 2: return 0
    mean = calc_mean(data)
    squared_deviations = sum((x - mean) ** 2 for x in data)
    return squared_deviations / (len(data) - 1)

def calc_std(data):
    """Calcula la desviacion estandar muestral."""
    return math.sqrt(calc_variance(data))

def calc_coefficient_of_variation(data):
    """Calcula el coeficiente de variacion en porcentaje."""
    if not data: return 0
    mean = calc_mean(data)
    if mean == 0: return 0  
    return (calc_std(data) / mean) * 100

def calc_covariance(x, y):
    """Calcula la covarianza muestral entre dos variables X e Y."""
    if len(x) != len(y) or len(x) < 2: return 0
    mean_x = calc_mean(x)
    mean_y = calc_mean(y)
    n = len(x)
    sum_cross_products = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    return sum_cross_products / (n - 1)

# --- NUEVOS ALGORITMOS SOLICITADOS ---

def calc_percentile(data, percentile):
    """Calcula un percentil especifico de forma lineal (Método estándar)."""
    if not data: return 0
    sorted_data = sorted(data)
    n = len(sorted_data)
    # Buscamos la posicion exacta indexada de forma flotante
    k = (n - 1) * (percentile / 100.0)
    floor_k = math.floor(k)
    ceil_k = math.ceil(k)
    
    if floor_k == ceil_k:
        return sorted_data[int(k)]
    
    # Interpolacion lineal si cae en medio de dos indices
    return sorted_data[floor_k] * (ceil_k - k) + sorted_data[ceil_k] * (k - floor_k)

def detect_outliers_iqr(data):
    """Identifica potenciales outliers usando las vallas de Tukey (Método IQR)."""
    if not data: return 0, 0, 0, []
    
    q1 = calc_percentile(data, 25)
    q3 = calc_percentile(data, 75)
    iqr = q3 - q1
    
    # Establecemos los límites industriales de control (Vallas de Tukey)
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    
    # Filtramos los valores que escapan de los límites
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    
    # Devolvemos valores unicos ordenados de outliers para no saturar la pantalla
    return q1, q3, iqr, sorted(list(set(outliers)))


# =====================================================================
# EJECUCION OPERATIVA Y EXTRACCION DE DATOS
# =====================================================================

def print_descriptive_report(table_name, column_name, data, unit=""):
    """Formatea e imprime el reporte estadistico con la jerarquia solicitada."""
    print(f"\n========================================================")
    print(f"TABLA:  {table_name.upper()}")
    print(f"COLUMNA: {column_name.lower()}")
    print(f"========================================================")
    print(f"Registros Analizados: {len(data)}")
    print(f"Media Aritmetica:     {calc_mean(data):.2f} {unit}")
    print(f"Rango Total:          {calc_range(data):.2f} {unit} (Min: {min(data):.2f} / Max: {max(data):.2f})")
    print(f"Varianza Muestral:    {calc_variance(data):.2f}")
    print(f"Desviacion Estandar:  {calc_std(data):.2f} {unit}")
    print(f"Coef. de Variacion:   {calc_coefficient_of_variation(data):.2f}%")
    
    # Procesamiento e integracion del IQR y Outliers
    q1, q3, iqr, outliers = detect_outliers_iqr(data)
    print(f"Primer Cuartil (Q1):  {q1:.2f} {unit}")
    print(f"Tercer Cuartil (Q3):  {q3:.2f} {unit}")
    print(f"Rango Intercuartil:   {iqr:.2f} {unit}")
    print(f"--------------------------------------------------------")
    print(f"DETECTANDO OUTLIERS (Prueba IQR 1.5x)...")
    if outliers:
        print(f"Alerta: Se detectaron {len(outliers)} valores atipicos unicos en BD:")
        print(f"Valores: {outliers[:15]} {'...' if len(outliers) > 15 else ''}")
    else:
        print("Proceso Controlado: No se detectaron outliers bajo el criterio IQR.")
    print(f"--------------------------------------------------------")


if __name__ == "__main__":
    print("PRODINTDATA - Modulo Integrado de Analitica Avanzada")
    print("========================================================")
    
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # --------------------------------------------------------
            # ANÁLISIS 1 Y RELACIONAL: TABLA FILM (LENGTH Y RENTAL_RATE)
            # --------------------------------------------------------
            cursor.execute("SELECT length, rental_rate, replacement_cost FROM film WHERE length IS NOT NULL")
            film_rows = cursor.fetchall()
            
            lengths = [row['length'] for row in film_rows]
            rates = [float(row['rental_rate']) for row in film_rows]
            replacement_costs = [float(row['replacement_cost']) for row in film_rows]
            
            # Reporte 1: Duracion
            print_descriptive_report("film", "length", lengths, "min")
            
            # Reporte 2: Costo de Reemplazo (Nueva Columna Adicional)
            print_descriptive_report("film", "replacement_cost", replacement_costs, "USD")
            
            # --------------------------------------------------------
            # ANÁLISIS 2: TABLA PAYMENT (AMOUNT) - Segunda Tabla Solicitada
            # --------------------------------------------------------
            cursor.execute("SELECT amount FROM payment WHERE amount IS NOT NULL")
            payment_rows = cursor.fetchall()
            
            amounts = [float(row['amount']) for row in payment_rows]
            
            # Reporte 3: Monto de Pago
            print_descriptive_report("payment", "amount", amounts, "USD")
            
            # --------------------------------------------------------
            # SECCIÓN RELACIONAL ORIGINAL
            # --------------------------------------------------------
            print("\n========================================================")
            print("ANALISIS RELACIONAL DE VARIABLES (CORRELACION COYUNTURAL)")
            print("========================================================")
            cov = calc_covariance(lengths, rates)
            print(f"Covarianza entre Duracion y Tarifa de Renta: {cov:.4f}")
            
            if cov > 0:
                print("Diagnostico: Covarianza POSITIVA. A mayor duracion, tiende a aumentar la tarifa de renta.")
            elif cov < 0:
                print("Diagnostico: Covarianza NEGATIVA. Peliculas mas largas tienen tarifas mas bajas.")
            else:
                print("Diagnostico: Sin relacion lineal aparente entre las variables.")
                
        except Error as e:
            print(f"Error operativo en la consulta: {e}")
        finally:
            cursor.close()
            conn.close()
            
    print("\n========================================================")
    print("Analisis estadistico industrial finalizado con exito.")
    print("========================================================")