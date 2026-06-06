# sakila-erp-pipeline-mvc
# Sistema ERP Sakila V2.0 - Arquitectura Nativa MVC/ORM

Componente de software industrial desarrollado por **ProdIntData** enfocado en la optimización de la persistencia de datos y análisis estadístico inferencial sobre la base de datos Sakila (MySQL).

## Estructura del Proyecto

* **Scripts_FaseI/**: Módulos de persistencia básica, operaciones CRUD planas, utilerías de entrada/salida masiva (CSV/JSON) y métricas analíticas descriptivas en Python puro.
* **Scripts_FaseII/**: Arquitectura avanzada utilizando el patrón de diseño Modelo-Vista-Controller (MVC) con un mapeador de objetos relacionales (ORM) nativo.
  * `main.py`: Punto de entrada unificado del sistema.
  * `dbcontext.py`: Manejador de contexto seguro para transacciones SQL.
  * `entities.py`: Objetos espejo de la base de datos.
  * `models.py`: Mapeador de datos a colecciones estructuradas (`List[CustomerRental]`).
  * `analytics_view.py`: Motor inferencial (Pruebas de normalidad D'Agostino-Pearson y contraste de hipótesis Mann-Whitney U) acoplado a visualizaciones.
  * `controllers.py`: Gestor de flujo y menús ejecutivos.

## Requisitos de Ejecución

1. Activar el entorno virtual: `.\.venv\Scripts\Activate.ps1`
2. Instalar dependencias: `pip install mysql-connector-python matplotlib seaborn pandas scipy python-dotenv`
3. Configurar el archivo `.env` con las credenciales locales de la base de datos.
4. Ejecutar el sistema: `cd Scripts_FaseII` y luego `python main.py`.
