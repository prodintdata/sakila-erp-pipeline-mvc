import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from models import CustomerRentalModel

def ejecutar_analisis_avanzado_sakila():
    print("======================================================================")
    print("         PRODINTDATA - COMPONENTE DE ANALÍTICA AVANZADA E INFERENCIAL  ")
    print("======================================================================")
    
    # 1. Extracción Completa de Datos a través del ORM Nativo
    print("STATUS: Solicitando universo transaccional al Modelo...")
    model = CustomerRentalModel()
    rentas = model.get_all(limit=16000) 
    
    # 2. Transformación a DataFrame incluyendo variables de tiempo
    data_list = []
    for r in rentas:
        if r.amount_paid is not None:
            # Cálculo del Lead Time en horas (Diferencia entre pago y renta)
            horas_recaudacion = 0.0
            if r.payment_date and r.rental_date:
                diferencia = r.payment_date - r.rental_date
                horas_recaudacion = diferencia.total_seconds() / 3600.0

            data_list.append({
                "customer_name": r.customer_name,
                "store_country": r.store_country,
                "amount_paid": float(r.amount_paid),
                "lead_time_horas": horas_recaudacion
            })
            
    df = pd.DataFrame(data_list)
    
    if df.empty:
        print("ERROR: No se encontraron datos financieros suficientes para el análisis.")
        return

    # ======================================================================
    #  TOP 10 CLIENTES QUE MÁS GASTARON POR TIENDA
    # ======================================================================
    print("\nANALISIS DE PARETO: TOP 10 CLIENTES CON MAYOR FACTURACIÓN POR PAÍS")
    print("----------------------------------------------------------------------")
    for pais, sub_df in df.groupby("store_country"):
        print(f"\nSUCURSAL: {pais.upper()}")
        top_10 = sub_df.groupby("customer_name")["amount_paid"].sum().reset_index()
        top_10 = top_10.sort_values(by="amount_paid", ascending=False).head(10)
        
        for idx, row in enumerate(top_10.itertuples(), 1):
            print(f"   [{idx:02d}] Cliente: {row.customer_name:<22} | Total Gastado: USD {row.amount_paid:.2f}")

    # Segmentación por sucursales para cálculos individuales
    df_canada = df[df["store_country"] == "Canada"]
    df_australia = df[df["store_country"] == "Australia"]

    pagos_canada = df_canada["amount_paid"]
    pagos_australia = df_australia["amount_paid"]

    # ======================================================================
    # ESTADÍSTICOS DESCRIPTIVOS DETALLADOS POR TIENDA
    # ======================================================================
    print("\nESTADÍSTICOS DESCRIPTIVOS BASE DE PRECIOS POR SUCURSAL")
    print("----------------------------------------------------------------------")
    for nombre, serie in [("CANADA", pagos_canada), ("AUSTRALIA", pagos_australia)]:
        # Cálculos estadísticos robustos
        media = serie.mean()
        mediana = serie.median()
        moda = serie.mode()[0] if not serie.mode().empty else np.nan
        desviacion = serie.std()
        cv = (desviacion / media) * 100 if media != 0 else 0
        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        
        print(f"SUCURSAL: {nombre}")
        print(f"   - Media (Promedio):      USD {media:.2f}")
        print(f"   - Mediana (Percentil 50): USD {mediana:.2f}")
        print(f"   - Moda (Precio Común):   USD {moda:.2f}")
        print(f"   - Cuartil 1 (25%):        USD {q1:.2f}")
        print(f"   - Cuartil 3 (75%):        USD {q3:.2f}")
        print(f"   - Desviación Estándar:   USD {desviacion:.2f}")
        print(f"   - Coeficiente Variación: {cv:.2f}% (Dispersión Relativa a la media)")
        print("-" * 40)

    # ======================================================================
    # AUDITORÍA DE EFICIENCIA OPERATIVA (LEAD TIME)
    # ======================================================================
    print("\nAUDITORÍA DE FLUJO DE CAJA: LEAD TIME DE RECAUDACIÓN (HORAS)")
    print("----------------------------------------------------------------------")
    print(f"Promedio global de tiempo transcurrido desde la renta hasta el pago:")
    print(f"   - Sucursal Canada:    {df_canada['lead_time_horas'].mean():.2f} horas de retraso promedio.")
    print(f"   - Sucursal Australia: {df_australia['lead_time_horas'].mean():.2f} horas de retraso promedio.")

    # ======================================================================
    # PRUEBAS DE NORMALIDAD (D'AGOSTINO-PEARSON)
    # ======================================================================
    print("\nEVALUACIÓN DE SUPUESTOS ESTADÍSTICOS (PRUEBA DE NORMALIDAD)")
    print("----------------------------------------------------------------------")
    stat_can, p_can = stats.normaltest(pagos_canada)
    stat_aus, p_aus = stats.normaltest(pagos_australia)
    
    normal_canada = p_can > 0.05
    normal_australia = p_aus > 0.05
    
    print(f"Tienda Canada    -> p-valor: {p_can:.5e} | ¿Es Normal? {'SÍ' if normal_canada else 'NO (Distribución No Paramétrica)'}")
    print(f"Tienda Australia -> p-valor: {p_aus:.5e} | ¿Es Normal? {'SÍ' if normal_australia else 'NO (Distribución No Paramétrica)'}")

    # ======================================================================
    # CONTRASTE DE HIPÓTESIS
    # ======================================================================
    print("\nINFERENCIA ESTADÍSTICA: PRUEBA DE HIPÓTESIS DE COMPARACIÓN")
    print("----------------------------------------------------------------------")
    print("H0: Los hábitos de pago en ambas sucursales son estadísticamente IGUALES.")
    print("H1: Los hábitos de pago en ambas sucursales son estadísticamente DIFERENTES.")
    
    ambas_normales = normal_canada and normal_australia
    
    if ambas_normales:
        print("CRITERIO: Datos Normales detectados. Aplicando Test t-Student para MEDIAS...")
        stat_test, p_test = stats.ttest_ind(pagos_canada, pagos_australia, equal_var=False)
        metrica_can, metrica_aus = pagos_canada.mean(), pagos_australia.mean()
        tipo_metrica = "Media"
    else:
        print("CRITERIO: Datos No Normales detectados. Aplicando Test U de Mann-Whitney para MEDIANAS...")
        stat_test, p_test = stats.mannwhitneyu(pagos_canada, pagos_australia, alternative='two-sided')
        metrica_can, metrica_aus = pagos_canada.median(), pagos_australia.median()
        tipo_metrica = "Mediana"
        
    print(f"\nResultados del Contraste:")
    print(f"   - {tipo_metrica} Canada: USD {metrica_can:.2f}")
    print(f"   - {tipo_metrica} Australia: USD {metrica_aus:.2f}")
    print(f"   - p-valor resultante: {p_test:.5f}")
    
    if p_test < 0.05:
        print(f"CONCLUSION: Se RECHAZA la hipótesis nula (H0) con un 95% de confianza.")
        print(f"   Las sucursales presentan un comportamiento de facturación significativamente DIFERENTE.")
    else:
        print(f"CONCLUSION: NO se rechaza la hipótesis nula (H0).")
        print(f"   Las diferencias observadas pertenecen al azar; comercialmente se comportan igual.")

    # ======================================================================
    #  GENERACIÓN DE TABLERO DE VISUALIZACIÓN GRÁFICA
    # ======================================================================

    sns.set_theme(style="whitegrid")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("PRODINTDATA - Diagnóstico Analítico y Estructural de Ingresos Sakila", fontsize=16, fontweight='bold')

    # Gráfico 1: Box Plot
    sns.boxplot(ax=axes[0, 0], data=df, x="store_country", y="amount_paid", hue="store_country", palette="Set2", legend=False)
    axes[0, 0].set_title("Análisis de Dispersión y Outliers (Box Plot)", fontweight='bold')
    axes[0, 0].set_xlabel("Sucursal")
    axes[0, 0].set_ylabel("Monto Pago (USD)")

    # Gráfico 2: Violin Plot
    sns.violinplot(ax=axes[0, 1], data=df, x="store_country", y="amount_paid", hue="store_country", palette="muted", inner="quartile", legend=False)
    axes[0, 1].set_title("Densidad y Cuartiles de Transacciones (Violin Plot)", fontweight='bold')
    axes[0, 1].set_xlabel("Sucursal")
    axes[0, 1].set_ylabel("Monto Pago (USD)")

    # Gráfico 3: Histograma General (Utilizando la Regla de Sturges)
    sns.histplot(ax=axes[1, 0], data=df, x="amount_paid", bins='sturges', kde=True, color="purple")
    axes[1, 0].set_title("Distribución Global de Precios (Histograma General)", fontweight='bold')
    axes[1, 0].set_xlabel("Monto Pago (USD)")
    axes[1, 0].set_ylabel("Frecuencia Absoluta")

    # Gráfico 4: Histograma comparativo por sucursal
    sns.histplot(ax=axes[1, 1], data=df, x="amount_paid", hue="store_country", bins='sturges', kde=True, multiple="dodge", palette="bright")
    axes[1, 1].set_title("Comparativa de Frecuencias de Precios por Sucursal", fontweight='bold')
    axes[1, 1].set_xlabel("Monto Pago (USD)")
    axes[1, 1].set_ylabel("Frecuencia Absoluta")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    ejecutar_analisis_avanzado_sakila()